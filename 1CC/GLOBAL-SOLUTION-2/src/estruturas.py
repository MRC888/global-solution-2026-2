# estruturas.py
# Monta e mantém as estruturas de dados do sistema.
#
# Todas as estruturas ficam dentro de um dicionário chamado "sistema",
# que é passado para as funções que precisam dele.
#
#   LISTA        sistema["ocorrencias"]   todas as ocorrências válidas, na ordem de registro
#   DICIONÁRIO   sistema["por_id"]        código -> ocorrência (acesso direto, sem percorrer a lista)
#   FILA         sistema["fila"]          códigos ainda não examinados (status aberta), por ordem de chegada
#   PILHA        sistema["pilha"]         alterações de status desta sessão (o topo é a última)
#   HIERARQUIA   sistema["hierarquia"]    bairro -> categoria -> lista de códigos
#   MATRIZ       sistema["matriz"]        linha = categoria, coluna = status, célula = quantidade
#   LISTA        sistema["historico"]     todos os eventos de mudança de status, em ordem
#   LISTA        sistema["inconsistentes"] registros com problema + motivos
#
# A fila e a pilha são listas comuns:
#   fila  -> entra no fim com append() e sai do começo com pop(0)
#   pilha -> entra no topo com append() e sai do topo com pop()

from validacao import (BAIRRO, CATEGORIAS, STATUS, validar_registro,
                       dia_valido, mensagens_dos_problemas)


def criar_matriz_zerada():
    """Cria a matriz categorias x status com todas as células em zero."""
    matriz = []
    for categoria in CATEGORIAS:
        linha = []
        for status in STATUS:
            linha.append(0)
        matriz.append(linha)
    return matriz


def criar_hierarquia_vazia():
    """Cria a hierarquia bairro -> categoria -> lista de códigos (vazia)."""
    categorias = {}
    for categoria in CATEGORIAS:
        categorias[categoria] = []
    return {BAIRRO: categorias}


def criar_sistema():
    """Cria o dicionário com todas as estruturas vazias."""
    sistema = {
        "ocorrencias": [],
        "por_id": {},
        "fila": [],
        "pilha": [],
        "hierarquia": criar_hierarquia_vazia(),
        "matriz": criar_matriz_zerada(),
        "historico": [],
        "inconsistentes": [],
        "avisos_carga": [],
        "lidos": 0,
        "cadastros": 0,
        "mudancas": 0,
    }
    return sistema


def registro_para_ocorrencia(registro):
    """Converte um registro já validado (só textos) em ocorrência (dia vira número)."""
    return {
        "id": registro["id"].strip(),
        "categoria": registro["categoria"].strip(),
        "descricao": registro["descricao"].strip(),
        "local": registro["local"].strip(),
        "dia": int(registro["dia"]),
        "status": registro["status"].strip(),
    }


def somar_na_matriz(sistema, categoria, status, valor):
    """Soma valor (+1 ou -1) na célula [categoria][status] da matriz."""
    linha = CATEGORIAS.index(categoria)
    coluna = STATUS.index(status)
    sistema["matriz"][linha][coluna] = sistema["matriz"][linha][coluna] + valor


def mover_na_matriz(sistema, categoria, status_antigo, status_novo):
    """Uma ocorrência mudou de status: tira 1 da coluna antiga e soma 1 na nova."""
    somar_na_matriz(sistema, categoria, status_antigo, -1)
    somar_na_matriz(sistema, categoria, status_novo, 1)


def adicionar_ocorrencia(sistema, ocorrencia):
    """Coloca uma ocorrência válida em todas as estruturas de uma vez."""
    codigo = ocorrencia["id"]
    sistema["ocorrencias"].append(ocorrencia)                              # lista
    sistema["por_id"][codigo] = ocorrencia                                 # dicionário
    sistema["hierarquia"][BAIRRO][ocorrencia["categoria"]].append(codigo)  # hierarquia
    somar_na_matriz(sistema, ocorrencia["categoria"], ocorrencia["status"], 1)  # matriz
    if ocorrencia["status"] == "aberta":
        sistema["fila"].append(codigo)                                     # fila (entra no fim)


def carregar_ocorrencias(sistema, registros):
    """Valida cada registro lido do CSV e separa os válidos dos inconsistentes."""
    for registro in registros:
        sistema["lidos"] = sistema["lidos"] + 1
        problemas = validar_registro(registro, sistema["por_id"])
        if len(problemas) > 0:
            sistema["inconsistentes"].append({"registro": registro, "problemas": problemas})
        else:
            adicionar_ocorrencia(sistema, registro_para_ocorrencia(registro))


def carregar_historico(sistema, eventos):
    """Guarda os eventos do histórico, conferindo se cada um aponta para uma ocorrência válida."""
    for evento in eventos:
        codigo = evento["id"]
        if codigo in sistema["por_id"] and dia_valido(evento["dia"]) and evento["novo"] in STATUS:
            sistema["historico"].append({
                "id": codigo,
                "dia": int(evento["dia"]),
                "anterior": evento["anterior"],
                "novo": evento["novo"],
                "observacao": evento["observacao"],
            })
        else:
            sistema["avisos_carga"].append("evento do histórico ignorado (ocorrência " + codigo
                                           + ", dia " + evento["dia"] + "): não aponta para uma ocorrência válida")


def descrever_inconsistencia(item):
    """Texto curto com o código e os motivos de um registro inconsistente."""
    codigo = item["registro"]["id"]
    if codigo == "":
        codigo = "(sem código)"
    return codigo + ": " + mensagens_dos_problemas(item["problemas"])
