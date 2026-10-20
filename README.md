# load-for-database

Restaurado a partir da instalação local de `load-for-database` versão 0.3.0.

Biblioteca Python para carregar arquivos XLSX em tabelas SQL Server.

## Instalação local

```bash
python -m pip install .
```

## Uso

```python
from load_for_database.load_data import load_data, load_data_insert_new

load_data(
    path_folder="C:/dados",
    file_name="exemplo.xlsx",
    table_name="TabelaDestino",
    schema="dbo",
    server="MEU_SERVIDOR",
    database="MeuBanco",
    user="MEU_USUARIO",
    password="MINHA_SENHA",
    sheet_name="Planilha1",
)
```

`load_data` acrescenta as linhas à tabela. `load_data_insert_new` **não faz UPDATE**: apenas insere linhas cujas chaves ainda não constam na tabela. A função utiliza `primary_key="id"` por padrão. O nome antigo `load_data_upsert` continua disponível como alias para compatibilidade.

## Dependências

- pandas
- sqlalchemy
- pyodbc
- openpyxl
- Driver Microsoft ODBC para SQL Server instalado no sistema (padrão no código: Driver 17)

## Observações

A lógica da versão 0.3.0 foi preservada; a função foi renomeada e recebeu um alias de compatibilidade. As funções capturam erros e os imprimem sem relançá-los. A configuração `pyproject.toml` e este README foram reconstruídos, não recuperados da instalação original.

Não armazene credenciais reais no repositório. Use variáveis de ambiente ou um gerenciador de segredos nos seus scripts.
