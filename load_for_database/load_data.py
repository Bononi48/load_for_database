import pandas as pd
import urllib
from sqlalchemy import create_engine


def load_data(path_folder, file_name, table_name, schema, server, database, user, password, sheet_name='',
              driver="ODBC Driver 17 for SQL Server"):
    """
    Loads data from an XLSX file into a table in a SQL Server database.

    parameters:
    - path_folder: Path to the folder where the XLSX file is located.
    - file_name: Name of the XLSX file to be loaded.
    - table_name: Name of the target table in the database.
    - schema: Schema of the table in the database.
    - server: Name or address of the SQL server.
    - database: Name of the database.
    - user: Username for connecting to the database.
    - password: Password for connecting to the database.
    - driver: (Opcional) Driver ODBC a ser utilizado. Padrão: "ODBC Driver 17 for SQL Server".
    """
    try:
        # Build the full file path
        caminho_arquivo = f"{path_folder}/{file_name}"

        if sheet_name:
            df = pd.read_excel(caminho_arquivo, sheet_name=sheet_name)
        else:
            # Read XLSX file into a DataFrame
            df = pd.read_excel(caminho_arquivo)

        # Build the connection string
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}")
        conn_str = f"mssql+pyodbc:///?odbc_connect={params}"

        # Create the connection engine
        engine = create_engine(conn_str)

        # Load the data into the table in the database
        df.to_sql(name=table_name, con=engine, schema=schema, if_exists="append", index=False)

        print(f"Data successfully loaded into the table {schema}.{table_name}.")

    except Exception as e:
        print(f"An error occurred while loading data: {e}")


def load_data_insert_new(path_folder, file_name, table_name, schema, server, database, user, password,
                     driver="ODBC Driver 17 for SQL Server", primary_key="id"):
    """
    Loads data from an XLSX file to a table in a SQL Server database, inserting only records whose primary key is not yet in the destination table.

    Parâmetros:
    - path_folder: Path to the folder where the XLSX file is located.
    - file_name: Name of the XLSX file to be loaded.
    - table_name: Name of the target table in the database.
    - schema: Schema of the table in the database.
    - server: Name or address of the SQL server.
    - database: Name of the database.
    - user: Username for connecting to the database.
    - password: Password for connecting to the database.
    - driver: (Optional) ODBC driver to be used. Default: "ODBC Driver 17 for SQL Server".
    - primary_key: Name of the column that is the primary key in the table (used to check if the record already exists).
    """
    try:
        # Build the full file path
        caminho_arquivo = f"{path_folder}/{file_name}"

        # Read XLSX file into a DataFrame
        df = pd.read_excel(caminho_arquivo)

        # Build the connection string
        params = urllib.parse.quote_plus(
            f"DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}")
        conn_str = f"mssql+pyodbc:///?odbc_connect={params}"

        # Create the connection engine
        engine = create_engine(conn_str)

        # Get the primary keys already existing in the table
        query = f"SELECT {primary_key} FROM {schema}.{table_name}"
        existing_keys = pd.read_sql(query, con=engine)[primary_key].tolist()

        # Filter the DataFrame to keep only new records
        df_novos = df[~df[primary_key].isin(existing_keys)]

        # If there are new records, insert them into the table
        if not df_novos.empty:
            df_novos.to_sql(name=table_name, con=engine, schema=schema, if_exists="append", index=False)
            print(f"{len(df_novos)} new records successfully loaded into the table {schema}.{table_name}.")
        else:
            print("No new records found to insert.")

    except Exception as e:
        print(f"An error occurred while loading data: {e}")


# Alias mantido para compatibilidade com scripts escritos na versão 0.3.0.
load_data_upsert = load_data_insert_new
