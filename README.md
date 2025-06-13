Documentação Técnica — Relatório de Títulos a Receber
Visão Geral
Este aplicativo, desenvolvido em Python com Streamlit, tem como objetivo facilitar a análise de relatórios financeiros no formato PDF, especificamente focado em títulos a receber. A aplicação permite o upload de arquivos, realiza extração estruturada dos dados e oferece uma interface rica em filtros para facilitar a tomada de decisão.

Estrutura do Projeto
graphql
Copiar
Editar
pdf_relatorio/
├── app.py                     # Arquivo principal da aplicação
├── media/                     # Armazena arquivos PDF enviados
├── parser/                    # Parser de dados PDF → CSV
│   ├── parser.py              # Implementação antiga
│   ├── relatorio.csv          # CSV gerado a partir do último PDF processado
├── src/                       # Núcleo da aplicação modular
│   ├── config.py              # Configurações globais e filtros
│   ├── services/              # Lógica de negócios
│   │   ├── data_filter.py     # Aplicação dos filtros
│   │   ├── pdf_parser.py      # Parser novo de PDF com validações
│   │   └── pdf_processor.py   # Pipeline de upload, parse e persistência
│   ├── ui/                    # Interface com o usuário
│   │   ├── main_view.py       # Componentes da visualização principal
│   │   └── sidebar.py         # Componentes da barra lateral (filtros)
│   └── utils/
│       └── formatters.py      # Formatação de datas e valores
Tecnologias Utilizadas
Python 3.11

Streamlit 1.45+

pandas 2.3+

pdfplumber

pathlib

poetry

Funcionalidades
Upload de Arquivo PDF
Upload realizado via sidebar.

Arquivo salvo localmente em media/.

Pipeline de processamento (PDFProcessorService) extrai os dados e salva como CSV.

Extração e Estruturação de Dados
O parser percorre o conteúdo do PDF e extrai:

Cliente

Status

Título

Fatura

Local

Espécie

Vencimento

Conta Corrente

Acres/Descontos

Juros/Multa

Valor Original

Valor Total

Os dados são validados e convertidos para tipos numéricos ou de data para garantir integridade.

Interface Interativa com Filtros
A sidebar da aplicação oferece os seguintes filtros:

Cliente (selectbox)

Título (selectbox)

Intervalo de vencimento (data inicial e final)

Valor total (slider com faixa dinâmica)

Filtro de Atrasados:

Checkbox para ativar

Slider para atraso em meses ou semanas

Opções: "Já cobrados", "A cobrar"

Filtro de Cobranças Futuras:

Checkbox para ativar

Slider com intervalos de 7, 14, 21 e 30 dias

Apresentação dos Dados
Título da aplicação e mensagens de status

Subtítulo com total de registros encontrados

Tabela com os dados filtrados

Valor total em aberto (métrica)

Exportação como CSV com botão de download

Formatação:

Datas: dd/mm/aaaa

Valores: 1.234,56

Tratamento de Erros
Mensagens claras para arquivos ausentes ou dados vazios

Validação de intervalos de datas

Slider de valor adaptativo para evitar quebras

Possibilidades Futuras
Campo de busca textual livre

Visualizações gráficas por cliente ou período

Exportação com formatação para Excel

Anotações persistentes por cliente/título (via banco de dados)

Automatização de mensagens de cobrança (via API)