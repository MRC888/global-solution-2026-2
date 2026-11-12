# validacao.py
# Regras do sistema: valores padronizados (categorias, status, locais),
# validação de registros e mudanças de status permitidas.
#
# Este arquivo não pede nada ao usuário e não imprime nada.
# Ele só responde perguntas do tipo "isto é válido?".


# ---------------------------------------------------------------
# Valores padronizados
# ---------------------------------------------------------------

BAIRRO = "Vila Esperança"   # bairro fictício do projeto

# O tempo é simulado em dias: do dia 1 ao dia 30. "Hoje" é o dia 30 (decisão D1).
DIA_INICIAL = 1
DIA_HOJE = 30

# Categorias: o código fica sem acento (é o que vai no CSV) e o nome é o que aparece na tela.
CATEGORIAS = ["iluminacao", "acessibilidade", "limpeza", "conservacao"]
NOMES_CATEGORIAS = {
    "iluminacao": "Iluminação",
    "acessibilidade": "Acessibilidade",
    "limpeza": "Limpeza",
    "conservacao": "Conservação",
}

# Status (situações) de uma ocorrência e o significado de cada um.
STATUS = ["aberta", "em_analise", "concluida"]
NOMES_STATUS = {
    "aberta": "Aberta",
    "em_analise": "Em análise",
    "concluida": "Concluída",
}
SIGNIFICADO_STATUS = {
    "aberta": "registrada e aguardando a primeira análise, na fila de triagem",
    "em_analise": "já foi examinada e a solução está em andamento",
    "concluida": "o problema foi resolvido; a ocorrência não muda mais",
}

# Locais genéricos do bairro (nunca endereço de uma pessoa).
LOCAIS = ["Entorno da UBS", "Entorno da Escola", "Praça Central", "Ponto de Ônibus"]

# Mudanças de status permitidas (decisão D4): só para a frente, um passo por vez.
# aberta -> em_analise -> concluida. Para corrigir um engano existe o "desfazer".
TRANSICOES = {
    "aberta": ["em_analise"],
    "em_analise": ["concluida"],
    "concluida": [],
}

# Peso de cada categoria no score de prioridade (decisão D12).
# Acessibilidade pesa mais porque impede pessoas de circular.
PESOS = {
    "acessibilidade": 3,
    "iluminacao": 2,
    "conservacao": 2,
    "limpeza": 1,
}

# Palavras que ajudam a sugerir a categoria a partir da descrição.
PALAVRAS_CHAVE = {
    "iluminacao": ["poste", "lâmpada", "lampada", "luminária", "luminaria", "escuro", "escura", "refletor", "luz"],
    "acessibilidade": ["rampa", "calçada", "calcada", "piso", "degrau", "corrimão", "corrimao", "cadeira de rodas"],
    "limpeza": ["lixo", "entulho", "sujeira", "mato", "restos", "caçamba", "cacamba"],
    "conservacao": ["banco", "brinquedo", "muro", "pintura", "pichado", "quebrado", "quebrada"],
}

# Tamanho máximo da descrição (evita textos enormes na tabela).
TAMANHO_MAXIMO_DESCRICAO = 120


# ---------------------------------------------------------------
# Funções de apoio
# ---------------------------------------------------------------

def campo_vazio(texto):
    """Devolve True se o texto estiver vazio ou só com espaços."""
    return texto.strip() == ""


def dia_valido(dia_texto):
    """Devolve True se o dia for um número inteiro entre 1 e 30.

    Regra L2 (usa NOT e OR):
        not dia_texto.isdigit() or int(dia_texto) < DIA_INICIAL or int(dia_texto) > DIA_HOJE
    O "or" para na primeira condição verdadeira. Por isso, quando o texto
    não é número, o int() nem chega a rodar e o programa não quebra.
    """
    dia_texto = dia_texto.strip()
    if not dia_texto.isdigit() or int(dia_texto) < DIA_INICIAL or int(dia_texto) > DIA_HOJE:
        return False
    return True


def eh_pendente(ocorrencia):
    """Regra L6 (usa NOT): uma ocorrência é pendente quando NÃO está concluída."""
    return not ocorrencia["status"] == "concluida"


# ---------------------------------------------------------------
# Validação de um registro (usada na carga do CSV, no cadastro e na correção)
# ---------------------------------------------------------------

def validar_registro(registro, por_id):
    """Confere todos os campos de um registro.

    registro: dicionário com textos (id, categoria, descricao, local, dia, status).
    por_id: dicionário das ocorrências já aceitas, para achar código repetido.

    Devolve uma lista de problemas. Cada problema é uma lista [campo, mensagem].
    Lista vazia = registro válido. Todas as regras rodam, para o registro
    receber TODOS os motivos, e não só o primeiro.
    """
    problemas = []

    # Regra 1: código
    codigo = registro["id"].strip()
    if campo_vazio(codigo):
        problemas.append(["id", "código ausente"])
    elif not codigo.isdigit():
        problemas.append(["id", "código deve ter só números"])
    elif codigo in por_id:
        problemas.append(["id", "código repetido (" + codigo + " já existe)"])

    # Regra 2: categoria precisa ser uma das quatro padronizadas
    categoria = registro["categoria"].strip()
    if campo_vazio(categoria):
        problemas.append(["categoria", "categoria ausente"])
    elif categoria not in CATEGORIAS:
        problemas.append(["categoria", "categoria desconhecida (" + categoria + ")"])

    # Regra 3: status precisa ser um dos três padronizados
    status = registro["status"].strip()
    if campo_vazio(status):
        problemas.append(["status", "status ausente"])
    elif status not in STATUS:
        problemas.append(["status", "status desconhecido (" + status + ")"])

    # Regra 4 (L1, usa OR): descrição vazia OU local vazio -> inválido
    descricao = registro["descricao"]
    local = registro["local"]
    if campo_vazio(descricao) or campo_vazio(local):
        if campo_vazio(descricao):
            problemas.append(["descricao", "descrição vazia"])
        if campo_vazio(local):
            problemas.append(["local", "local vazio"])

    # Regra 5: o ponto e vírgula separa os campos no CSV, então não pode aparecer no texto
    if ";" in descricao or ";" in local:
        problemas.append(["descricao", "o texto não pode ter ponto e vírgula (;)"])

    # Regra 6 (L2, usa NOT e OR): dia precisa ser número de 1 a 30
    if not dia_valido(registro["dia"]):
        problemas.append(["dia", "dia fora do período (deve ser de 1 a 30)"])

    return problemas


def mensagens_dos_problemas(problemas):
    """Transforma a lista de problemas em um texto só, separado por ponto e vírgula."""
    mensagens = []
    for problema in problemas:
        mensagens.append(problema[1])
    return "; ".join(mensagens)


def campos_com_problema(problemas):
    """Lista os campos que têm problema, sem repetir."""
    campos = []
    for problema in problemas:
        if problema[0] not in campos:
            campos.append(problema[0])
    return campos


# ---------------------------------------------------------------
# Mudança de status
# ---------------------------------------------------------------

def verificar_transicao(status_atual, status_novo):
    """Decide se uma ocorrência pode passar de status_atual para status_novo.

    Devolve [True, ""] se pode, ou [False, mensagem explicando por quê].
    A ordem dos testes importa: cada elif só roda se os anteriores falharam.
    """
    if status_novo not in STATUS:
        return [False, "Status desconhecido. Use: aberta, em análise ou concluída."]
    elif status_novo == status_atual:
        return [False, "A ocorrência já está nesse status."]
    elif status_atual == "concluida":
        return [False, "Ocorrência concluída não pode mudar de status."]
    elif status_novo not in TRANSICOES[status_atual]:
        permitido = NOMES_STATUS[TRANSICOES[status_atual][0]]
        return [False, "Transição não permitida: de " + NOMES_STATUS[status_atual]
                + " só é possível ir para " + permitido + "."]
    else:
        return [True, ""]


# ---------------------------------------------------------------
# Sugestão de categoria (diferencial)
# ---------------------------------------------------------------

def sugerir_categoria(descricao):
    """Procura palavras-chave na descrição e devolve a categoria com mais acertos.

    Devolve "" quando nenhuma palavra conhecida aparece.
    Em caso de empate, fica a categoria que aparece primeiro em CATEGORIAS.
    """
    texto = descricao.lower()
    melhor_categoria = ""
    maior_acertos = 0
    for categoria in CATEGORIAS:
        acertos = 0
        for palavra in PALAVRAS_CHAVE[categoria]:
            if palavra in texto:
                acertos = acertos + 1
        if acertos > maior_acertos:
            maior_acertos = acertos
            melhor_categoria = categoria
    return melhor_categoria
