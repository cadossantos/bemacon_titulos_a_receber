# Documentação Técnica — Relatório de Títulos a Receber

## Visão Geral

Este aplicativo desenvolvido em Python com Streamlit tem como objetivo facilitar a visualização e análise de relatórios financeiros no formato PDF, especificamente relatórios de títulos a receber. A aplicação permite o upload de relatórios em PDF, extrai os dados relevantes com um parser personalizado e oferece uma interface interativa com filtros para análise detalhada.

---

## Estrutura do Projeto

```
pdf_relatorio/
├── app.py                       # Código principal da aplicação Streamlit
├── parser/
│   ├── __init__.py
│   └── parser.py               # Funções responsáveis pela extração e estruturação dos dados
├── media/                      # Diretório onde os arquivos PDF são salvos
├── parser/relatorio.csv        # CSV gerado a partir da extração dos dados do PDF
```

---

## Tecnologias Utilizadas

* Python 3.11
* Streamlit
* pandas
* pdfplumber
* pathlib

---

## Funcionalidades

### Upload de Arquivo PDF

* O usuário pode fazer upload de um arquivo PDF com os dados dos títulos.
* O arquivo é salvo localmente em `media/`.
* O conteúdo é processado com a função `processar_pdf`, que extrai os dados relevantes e salva em `parser/relatorio.csv`.

### Extração e Estruturação de Dados

O parser percorre linha a linha o conteúdo do PDF e extrai informações como:

* Cliente
* Status
* Título
* Fatura
* Local
* Espécie
* Vencimento
* Conta Corrente
* Acres/Descontos
* Juros/Multa
* Valor Original
* Valor Total

Os valores são convertidos e padronizados para facilitar a leitura e cálculos.

### Filtros Interativos

A interface lateral permite os seguintes filtros:

* Cliente: selectbox com todos os clientes únicos
* Título: selectbox com todos os títulos extraídos
* Vencimento: seleção separada de data inicial e data final, com validação do intervalo
* Valor total: slider para filtrar por faixa de valor

### Apresentação dos Dados

* Tabela dinâmica com os dados filtrados
* Total de registros encontrados
* Valor total em aberto
* Datas formatadas no padrão `dd/mm/aaaa`
* Valores monetários no padrão brasileiro: `1.234,56`

### Exportação

O DataFrame filtrado pode ser baixado como CSV via botão de download.

---

## Tratamento de Erros

* A aplicação exibe mensagens claras quando nenhum dado é carregado
* O filtro de datas impede erros ao selecionar apenas uma data
* O slider de valor se ajusta automaticamente para não quebrar quando há apenas um valor possível

---

