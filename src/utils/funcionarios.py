# src/utils/funcionarios.py

from typing import Dict, List

# Dicionário base: loja → lista de funcionários
FUNCIONARIOS_POR_LOJA: Dict[str, List[str]] = {
    "Diretoria": [
        "CLAUDIA SIQUEIRA GOMES ALVES",
        "TASSO GOMES ALVES",
        "ADEMIR RODRIGUES ALVES"
    ],
    "Betel": [
        "Cosme Nascimento dos Santos",
        "Vonivon Soares dos Santos",
        "Kléber Brito Moreira",
        "Cristiane Santos Guimarães",
        "Miranda de Almeida Santos",
        "Jeferson de Jesus Cruz",
        "Alisson Souza de Almeida",
        "Mirian Gonçalves dos Santos", 
        "Leandro Pereira Vieira",
        "Cleyton Santos Silva",
        "Jeferson Santos de Jesus",
        "Everaldo de Jesus Santos",
        "Daniel do Rosário Santos",
        "Ramon Pereria dos Santos", 
        "Larissa Santos Ferreira",
        "Alex Santos de Almeida",
        "Jacó Cruz dos Santos",
        "Maria Fernanda Nery Santos",
        "Nerisvaldo Soares dos Santos",
        "Joildes Nascimento do Carmo Júnio",
        "Diego Santana Ferreira",
        "Lindoilson Santos Costa",
        "Cleiton Santos de Almeida",
        "Fábio de Jesus dos Santos",
        "Lucas Nunes dos Santos",
        "Wellington de Almeida Reis",
        "Marcela Santos Santana",
        "Wemerson dos Santos Silva",
        "Cláudio Argolo dos Santos"
    ],
    "ACTT_Materiais": [
        "Juliano Silva Santana",
        "Egnailson Soares dos Santos",
        "Marcio Mauricio Luz Silva Júnior",
        "Deuslir de Andrade Viana"
    ],
    "ACTT_Madeiras": [
        "Maisa de Almeida Santos",
        "Lindomar Gusmão Lima",
        "Luis Fernando de Andrade Silva",
        "Amilton José dos Santos Júnior",
        "Célio Menezes de Oliveira"
    ]
    # Adicione mais lojas e nomes conforme necessário
}

# Mapeamento reverso: funcionário → loja principal
FUNCIONARIO_PARA_LOJA: Dict[str, str] = {
    nome: loja
    for loja, nomes in FUNCIONARIOS_POR_LOJA.items()
    for nome in nomes
}
