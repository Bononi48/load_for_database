"""Importação de arquivos CSV/XLSX para SQL Server.

Módulo independente, compatível com o padrão de conexão de load_data.py.
Dependências: pandas, sqlalchemy, pyodbc, openpyxl (para XLSX).
"""
from pathlib import Path
import time
import urllib.parse

import pandas as pd
from sqlalchemy import create_engine, inspect


def load_file(
    file_path,
    table_name,
    schema,
    server,
    database,
    user,
    password,
    *,
    sheet_name=0,
    if_exists="append",
    driver="ODBC Driver 17 for SQL Server",
    chunksize=1000,
    csv_sep=",",
    csv_encoding="utf-8-sig",
    csv_decimal=".",
    csv_dtype=None,
    dtype=None,
    confirm_replace=False,
):
    """Lê CSV/XLSX e grava em tabela SQL Server.

    if_exists: 'fail' (não sobrescreve), 'append' (cria se não existir),
               'replace' (remove/recria tabela; exige confirm_replace=True).
    dtype: mapeamento opcional {coluna: sqlalchemy.types.*} para controlar tipos SQL.
    csv_dtype: tipos opcionais para pd.read_csv (ex.: {'CPF': 'string'}).

    Observação: inferência de tipos é feita pelo Pandas e pode não preservar
    zeros à esquerda, precisão de decimais ou formatos especiais; configure
    csv_dtype/dtype ou prepare os dados antes para colunas críticas.
    """
    inicio = time.perf_counter()
    path = Path(file_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    if not table_name or not schema:
        raise ValueError("table_name e schema são obrigatórios.")
    if if_exists not in ("fail", "append", "replace"):
        raise ValueError("if_exists deve ser 'fail', 'append' ou 'replace'.")
    if if_exists == "replace" and not confirm_replace:
        raise ValueError("'replace' apaga e recria a tabela. Confirme com confirm_replace=True.")
    if not isinstance(chunksize, int) or chunksize <= 0:
        raise ValueError("chunksize deve ser inteiro positivo.")

    ext = path.suffix.lower()
    if ext in (".xlsx", ".xlsm"):
        df = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    elif ext == ".csv":
        df = pd.read_csv(
            path, sep=csv_sep, encoding=csv_encoding,
            decimal=csv_decimal, dtype=csv_dtype, low_memory=False
        )
    else:
        raise ValueError("Formato não suportado. Use .csv, .xlsx ou .xlsm.")

    if not isinstance(df, pd.DataFrame):
        raise ValueError("Selecione apenas uma aba com sheet_name.")
    if df.columns.isna().any() or any(not str(c).strip() for c in df.columns):
        raise ValueError("Existem nomes de colunas vazios na planilha.")
    df.columns = [str(c) for c in df.columns]
    if df.columns.duplicated().any():
        raise ValueError("Existem nomes de colunas duplicados.")

    params = urllib.parse.quote_plus(
        f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={user};PWD={password}"
    )
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    try:
        with engine.begin() as conn:
            exists = inspect(conn).has_table(table_name, schema=schema)
            if exists and if_exists == "fail":
                raise ValueError(f"A tabela {schema}.{table_name} já existe.")
            df.to_sql(
                name=table_name, con=conn, schema=schema,
                if_exists=if_exists, index=False,
                chunksize=chunksize, dtype=dtype
            )
    finally:
        engine.dispose()

    result = {
        "table": f"{schema}.{table_name}",
        "rows": len(df),
        "columns": len(df.columns),
        "mode": if_exists,
        "seconds": round(time.perf_counter() - inicio, 2),
    }
    print(f"Carga concluída: {result['rows']} linhas em {result['table']} ({result['seconds']}s).")
    return result
