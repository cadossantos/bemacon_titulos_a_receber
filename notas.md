## Implementações necessárias

### Dicionário com nome de funcionários
Para especificar quem é funcionário e a qual loja o funcionário pertence... algo como:

funcionarios = {
    "diretoria": ["CLAUDIA SIQUEIRA GOMES ALVES", "TASSO GOMES ALVES", "ADEMIR RODRIGUES ALVES"]
    "matriz": ["ALEX SANTOS DE ALMEIDA", "EGNAILSON SOARES DOS SANTOS"]
    "actt_madeiras": ["ALEX SANTOS DE ALMEIDA", "EGNAILSON SOARES DOS SANTOS"]
    "actt_materiais": ["ALEX SANTOS DE ALMEIDA", "EGNAILSON SOARES DOS SANTOS"]
    "itacare": ["ALEX SANTOS DE ALMEIDA", "EGNAILSON SOARES DOS SANTOS"]
}

A necessidade dessa estrutura é para poder filtrar separadamente quem é funcionário que possui títulos a cobrar e poder destacar qual a loja que ele pertence.

### Atrasados

Esse filtro (checkbox) permite selecionar somente os títulos que já estão atrasdos.
Quando habilitado, ele chama dois outros filtros:
    - uma sidebar.slider para selecionar os dados com base em tempo de atraso. Ex: 1 ano, 11 meses, 10 meses
    - mais um checkbox com o nome "mês corrente"
        - se o checkbox "mes corrente for habilitado, o sidebar.slider passa a trabalhar com intervalos menores de tempo (semanas)
    - já cobrados
    - a cobrar

### Cobranças futuras

Esse filtro carrega apenas os títulos que devem ser cobrados nos próximos 30 dias.
Quando habilitado, ele carrega um slider para selecionar intervalos de tempo de 30, 21, 14 e 7 dias.

## Banco de Dados

### Necessário?

Minha supervisora deseja poder a dicionar informações aos dados carregados. Isso implica que não estaremos mais visualizando dados, mas interagindo e alterando com os mesmos.
Ela deseja poder adicionar observações como:
    - já foi cobrado (acho que vale também a possibilidade de adicionar quantas cobranças já foram feitas)
    - ação judicial (acho que faz sentido que após muitas cobranças e algum tempo sem que o pagamento tenha ocorrido, seja sinalizado que aquele cliente pode ser acionado judicialmente)
    - vale também poder adicionar qual o acordo comercial vigente com o cliente (paga a cada semana, quinzena ou mês)
    - adicionar diretório para digitalizar cupons de cobrança?


Será que seria a hora de já migrar para o django?
Será que o stramlit pode me permitir fazer essas alterações com estabilidade e segunrança?
Se sim, eu prefiro manter esse app no streamlit para ter menos tempo na entrega.
Já que temos um campo para upload e os dados serão carregados novamente quando o arquivo for adicionado... como podemos garantir a persistencia dos dados que poderemos adicionar manualmente?


### Como automatizar cobranças?

Podemos a partir do csv, subir uma task para um agente de IA enviar mensagens de cobranças para todos os clientes em atraso.
Precisa descobrir se é seguro fazer isso com evolution API se for o caso.

### Possibilidades Futuras

* Suporte a múltiplos uploads com histórico
* Visualizações gráficas por cliente, período ou valor
* Campo de busca textual livre
* Exportação em Excel com formatação e sumário
* Ordenação interativa de colunas


