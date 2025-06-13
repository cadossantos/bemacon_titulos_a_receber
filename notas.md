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






Perfeito, Cláudio. Vamos focar nos filtros **Atrasados** e **Cobranças Futuras**, mantendo a estrutura modular e enxuta que você já implementou.

---

## **Etapa 1: Planejamento dos Filtros**

### **Filtro: Títulos Atrasados**
- `checkbox_atrasados`: ativa ou desativa esse filtro
- Se ativado:
  - `slider_tempo_atraso`: define o tempo de atraso (em meses ou semanas)
  - `checkbox_mes_corrente`: altera a granularidade para semanas
  - `checkbox_ja_cobrado`
  - `checkbox_a_cobrar`

**Critérios de seleção:**
- Atraso = `Vencimento < hoje`
- Tempo de atraso = diferença entre hoje e vencimento
- Se `mes_corrente` estiver ativado: slider opera em semanas
- `já cobrados` e `a cobrar` precisarão de campo específico (podemos deixar como placeholder por enquanto)

---

### **Filtro: Cobranças Futuras**
- `checkbox_cobrancas_futuras`: ativa ou desativa esse filtro
- `slider_dias_futuros`: seleção entre 7, 14, 21, 30 dias

**Critério de seleção:**
- `hoje < vencimento <= hoje + N dias`

---

## **Etapa 2: Proposta de Implementação Modular**

### A. **Adicionar campos ao `FiltroRelatorio`**

```python
# src/config.py
@dataclass
class FiltroRelatorio:
    ...
    atrasados: bool = False
    tempo_atraso: int = None
    mes_corrente: bool = False
    ja_cobrados: bool = False
    a_cobrar: bool = False

    cobrancas_futuras: bool = False
    dias_futuros: int = None
```

---

### B. **Construir os filtros na sidebar**

Sugiro criarmos dois novos métodos em `SidebarComponents`:
```python
# src/ui/sidebar.py

@staticmethod
def filtro_atrasados() -> Tuple[bool, Optional[int], bool, bool, bool]:
    atrasados = st.sidebar.checkbox("Mostrar apenas títulos atrasados")
    tempo = None
    mes_corrente = False
    ja_cobrado = False
    a_cobrar = False

    if atrasados:
        mes_corrente = st.sidebar.checkbox("Mês corrente (slider em semanas)")
        tempo = st.sidebar.slider(
            "Tempo de atraso",
            min_value=1,
            max_value=12 if not mes_corrente else 4,
            step=1,
            format="%d " + ("mês(es)" if not mes_corrente else "semana(s)")
        )
        ja_cobrado = st.sidebar.checkbox("Já cobrados")
        a_cobrar = st.sidebar.checkbox("A cobrar")

    return atrasados, tempo, mes_corrente, ja_cobrado, a_cobrar

@staticmethod
def filtro_cobrancas_futuras() -> Tuple[bool, Optional[int]]:
    futuras = st.sidebar.checkbox("Cobranças futuras")
    dias = None
    if futuras:
        dias = st.sidebar.select_slider(
            "Próximos dias",
            options=[7, 14, 21, 30],
            value=30
        )
    return futuras, dias
```

---

### C. **Integrar à `construir_sidebar`**

Após coletar os filtros normais:

```python
atrasados, tempo_atraso, mes_corrente, ja_cobrado, a_cobrar = SidebarComponents.filtro_atrasados()
futuras, dias_futuros = SidebarComponents.filtro_cobrancas_futuras()
```

E passar isso ao `FiltroRelatorio`:

```python
filtros = FiltroRelatorio(
    ...
    atrasados=atrasados,
    tempo_atraso=tempo_atraso,
    mes_corrente=mes_corrente,
    ja_cobrados=ja_cobrado,
    a_cobrar=a_cobrar,
    cobrancas_futuras=futuras,
    dias_futuros=dias_futuros
)
```

---

### D. **Aplicar a lógica no `DataFilterService`**

Você pode adicionar, ao final do `aplicar_filtros`, blocos como:

```python
# Atrasados
if filtros.atrasados and filtros.tempo_atraso:
    hoje = pd.Timestamp.today()
    fator = 7 if filtros.mes_corrente else 30
    dias_limite = filtros.tempo_atraso * fator
    df = df[df["Vencimento"] < hoje]
    df = df[(hoje - df["Vencimento"]).dt.days <= dias_limite]

# Futuras cobranças
if filtros.cobrancas_futuras and filtros.dias_futuros:
    hoje = pd.Timestamp.today()
    limite = hoje + pd.Timedelta(days=filtros.dias_futuros)
    df = df[(df["Vencimento"] > hoje) & (df["Vencimento"] <= limite)]
```

---

### Etapa 3: Proponho começarmos por...

1. Adicionar os campos ao `FiltroRelatorio`
2. Criar os dois métodos de filtro na sidebar
3. Integrar esses campos no `construir_sidebar`
4. Implementar a lógica base de filtragem (sem considerar "já cobrados" ainda, pois dependerá do banco)

**Quer começar por qual parte? Posso te mandar apenas a primeira etapa se preferir seguir incrementalmente.**