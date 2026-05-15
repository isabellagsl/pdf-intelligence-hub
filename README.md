# Intelligent PDF Data Extraction Pipeline

Este repositório é um projeto de estudo pessoal focado na extração de dados não estruturados de arquivos PDF. O objetivo é transformar documentos brutos em estruturas limpas e validadas para RAG (Retrieval-Augmented Generation) e Análise de Dados, aplicando padrões de Engenharia de Software.

## Stack Tecnológica e Arquitetura

O pipeline de extração utiliza ferramentas específicas para cada necessidade, garantindo velocidade e precisão:

- **PyMuPDF & pymupdf-layout**: Motores principais (High-performance extraction) para leitura rápida de textos brutos com análise inteligente de layout (blocos e colunas).
- **pdfplumber**: Utilizado especificamente para o *parsing* de tabelas (Grid-based extraction), dada sua precisão em geometrias complexas.
- **Pydantic**: Garante a integridade dos dados através de validação baseada em esquemas rigorosos (contratos de dados).
- **Loguru**: Observabilidade e rastreabilidade detalhada para facilitar o *debugging* de documentos complexos.
- **Pandas & Tabulate**: Utilizados para estruturação e conversão de dados tabulares para o formato Markdown.
- **Regex & langdetect**: Processamento de texto, normalização e detecção de idioma.
- **Poetry**: Gerenciamento de dependências e ambiente de forma determinística.

## Estrutura do Projeto

```plaintext
├── data/               # Arquivos PDF originais para extração
├── output/             # Resultados (Textos Markdown e Imagens)
├── src/
│   ├── extractors/     # Classes especialistas (Textos, Tabelas, Imagens)
│   ├── processors/     # Pipeline de limpeza e normalização Unicode
│   ├── models/         # Definições de Schemas Pydantic e IA
│   └── utils/          # Configuração de Logs e gerenciamento de IO
├── tests/              # Testes unitários da extração
└── pyproject.toml      # Configuração de dependências e build
```

## Como Executar

**Requisitos**: Python 3.13+ e Poetry.

```bash
# Clone o repositório
git clone https://github.com/isabellagsl/pdf-intelligence-hub.git

# Acesse o diretório
cd pdf-intelligence-hub

# Instale as dependências
poetry install

# Execute o pipeline passando o caminho do PDF
poetry run python -m src.main data/arquivo-exemplo.pdf
```

## Autora

Desenvolvido por **Isabella Gonçalves** como projeto de estudo pessoal em Engenharia de Dados e Inteligência Artificial.
