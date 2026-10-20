# Relatório de recuperação

**Origem:** pacote instalado em ambiente virtual, recebido como `ld.zip`.
**Versão encontrada:** 0.3.0.

Arquivos de código-fonte recuperados, sem alterações:
- `load_for_database/load_data.py`
- `load_for_database/__init__.py`

Arquivos recriados para permitir instalação/publicação do projeto:
- `pyproject.toml`
- `README.md`
- `.gitignore`
- `RECUPERACAO.md`

Os arquivos `*.dist-info` e `__pycache__` foram omitidos: são artefatos de instalação, não código-fonte necessário ao repositório.

Este projeto é uma reconstrução funcional da fonte instalada e não uma recuperação do histórico de commits do Git.

**Alteração posterior:** `load_data_upsert` renomeada para `load_data_insert_new`, mantendo o nome anterior como alias. Sem mudança na lógica de inserção.
