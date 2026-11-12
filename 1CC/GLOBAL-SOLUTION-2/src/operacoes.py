# operacoes.py
# As ações do sistema: buscar, filtrar, cadastrar, atualizar status,
# triagem, desfazer e corrigir inconsistências.
#
# Estas funções não usam input() nem print(). Elas recebem os dados prontos
# e devolvem o resultado. Quem conversa com o usuário é o interface.py.
# Assim as regras podem ser testadas sozinhas (ver testes.py).

from validacao import (DIA_HOJE, NOMES_STATUS, validar_registro, verificar_transicao)
from estruturas import (adicionar_ocorrencia, mover_na_matriz, registro_para_ocorrencia)


# ---------------------------------------------------------------
# Consultas
# ---------------------------------------------------------------

def completar_codigo(texto):
    """Completa o código com zeros à esquerda: "14" vira "014"."""
    texto = texto.strip()
    if texto.isdigit():
        return texto.zfill(3)
    return texto


def buscar(sistema, codigo_texto):
    """Acha uma ocorrência pelo código usando o dicionário (sem percorrer a lista).

    Devolve a ocorrência, ou None se o código não existir.
    """
    codigo = completar_codigo(codigo_texto)
    if codigo in sistema["por_id"]:
        return sistema["por_id"][codigo]
    return None


def eventos_da_ocorrencia(sistema, codigo):
    """Percorre o histórico e devolve só os eventos de uma ocorrência."""
    eventos = []
    for evento in sistema["historico"]:
        if evento["id"] == codigo:
            eventos.append(evento)
    return eventos


def filtrar(sistema, categoria, status):
    """Devolve as ocorrências que passam no filtro. Texto vazio = "todas".

    Regra L3 (usa OR e AND):
        (categoria == "" or oc["categoria"] == categoria) and (status == "" or oc["status"] == status)
    Cada parêntese é verdadeiro quando aquele filtro não foi usado OU quando o valor bate.
    O "and" exige que os dois filtros passem ao mesmo tempo.
    """
    resultado = []
    for oc in sistema["ocorrencias"]:
        if (categoria == "" or oc["categoria"] == categoria) and (status == "" or oc["status"] == status):
            resultado.append(oc)
    return resultado


# ---------------------------------------------------------------
# Cadastro
# ---------------------------------------------------------------

def proximo_codigo(sistema):
    """Gera o próximo código: maior código existente + 1, com 3 dígitos (decisão D5).

    Olha também os registros inconsistentes, para nunca repetir um código.
    """
    maior = 0
    for codigo in sistema["por_id"]:
        if int(codigo) > maior:
            maior = int(codigo)
    for item in sistema["inconsistentes"]:
        codigo = item["registro"]["id"]
        if codigo.isdigit() and int(codigo) > maior:
            maior = int(codigo)
    return str(maior + 1).zfill(3)


def possiveis_duplicadas(sistema, categoria, local):
    """Procura ocorrências que podem ser o mesmo problema já registrado.

    Regra L5 (usa AND e NOT): mesma categoria E mesmo local E NÃO concluída.
    """
    encontradas = []
    for oc in sistema["ocorrencias"]:
        if oc["categoria"] == categoria and oc["local"] == local and not oc["status"] == "concluida":
            encontradas.append(oc)
    return encontradas


def cadastrar(sistema, categoria, descricao, local, dia_texto):
    """Valida e cadastra uma ocorrência nova. Toda ocorrência nova começa "aberta".

    Devolve [True, [], ocorrencia] se deu certo,
    ou [False, lista_de_problemas, None] se algum campo estiver inválido.
    """
    registro = {
        "id": proximo_codigo(sistema),
        "categoria": categoria,
        "descricao": descricao.strip(),
        "local": local.strip(),
        "dia": dia_texto.strip(),
        "status": "aberta",
    }
    problemas = validar_registro(registro, sistema["por_id"])
    if len(problemas) > 0:
        return [False, problemas, None]
    ocorrencia = registro_para_ocorrencia(registro)
    adicionar_ocorrencia(sistema, ocorrencia)      # entra na lista, no dicionário, na hierarquia, na matriz e no fim da fila
    sistema["cadastros"] = sistema["cadastros"] + 1
    return [True, [], ocorrencia]


# ---------------------------------------------------------------
# Atualização de status
# ---------------------------------------------------------------

def atualizar_status(sistema, codigo_texto, status_novo, observacao):
    """Muda o status de uma ocorrência e registra a mudança no histórico e na pilha.

    Devolve [True, mensagem] ou [False, mensagem explicando o problema].
    """
    ocorrencia = buscar(sistema, codigo_texto)
    if ocorrencia is None:
        return [False, "Ocorrência " + completar_codigo(codigo_texto) + " não encontrada."]

    resultado = verificar_transicao(ocorrencia["status"], status_novo)
    if not resultado[0]:
        return [False, resultado[1]]

    codigo = ocorrencia["id"]
    status_antigo = ocorrencia["status"]
    observacao = observacao.replace(";", ",").strip()   # ";" quebraria o CSV
    if observacao == "":
        observacao = "sem observação"

    ocorrencia["status"] = status_novo
    evento = {"id": codigo, "dia": DIA_HOJE, "anterior": status_antigo,
              "novo": status_novo, "observacao": observacao}
    sistema["historico"].append(evento)    # histórico: guarda tudo, para sempre
    sistema["pilha"].append(evento)        # pilha: só desta sessão, para poder desfazer
    mover_na_matriz(sistema, ocorrencia["categoria"], status_antigo, status_novo)

    # Se saiu de "aberta", já foi examinada: sai da fila.
    if status_antigo == "aberta" and codigo in sistema["fila"]:
        sistema["fila"].remove(codigo)

    sistema["mudancas"] = sistema["mudancas"] + 1
    return [True, codigo + ": " + NOMES_STATUS[status_antigo] + " -> "
            + NOMES_STATUS[status_novo] + ". Registrado no histórico."]


def desfazer(sistema):
    """Desfaz a última mudança de status desta sessão (tira o topo da pilha).

    O histórico não perde nada: a volta é registrada como um novo evento "desfeito" (decisão D6).
    Se a ocorrência voltou para "aberta", ela volta para o COMEÇO da fila (decisão D7).
    """
    if len(sistema["pilha"]) == 0:
        return [False, "Nada para desfazer: nenhuma mudança de status foi feita nesta sessão."]

    evento = sistema["pilha"].pop()        # sai o topo: a última mudança
    ocorrencia = sistema["por_id"][evento["id"]]
    status_atual = ocorrencia["status"]
    status_volta = evento["anterior"]

    ocorrencia["status"] = status_volta
    mover_na_matriz(sistema, ocorrencia["categoria"], status_atual, status_volta)
    if status_volta == "aberta":
        sistema["fila"].insert(0, ocorrencia["id"])

    sistema["historico"].append({"id": ocorrencia["id"], "dia": DIA_HOJE, "anterior": status_atual,
                                 "novo": status_volta, "observacao": "desfeito (mudança anterior cancelada)"})
    sistema["mudancas"] = sistema["mudancas"] + 1
    return [True, "Desfeito: " + ocorrencia["id"] + " voltou para " + NOMES_STATUS[status_volta] + "."]


# ---------------------------------------------------------------
# Triagem (fila)
# ---------------------------------------------------------------

def chamar_proximo(sistema):
    """Tira o primeiro código da fila (quem chegou primeiro é atendido primeiro).

    Devolve o código, ou None se a fila estiver vazia.
    """
    if len(sistema["fila"]) == 0:
        return None
    return sistema["fila"].pop(0)


def devolver_para_fila(sistema, codigo):
    """A ocorrência não foi examinada agora: volta para o começo da fila (decisão D7)."""
    sistema["fila"].insert(0, codigo)


# ---------------------------------------------------------------
# Correção de inconsistências
# ---------------------------------------------------------------

def corrigir_inconsistente(sistema, indice, registro_corrigido):
    """Valida de novo um registro inconsistente já corrigido pelo usuário.

    Se ficou válido, sai da lista de inconsistentes e entra nas estruturas, como um cadastro.
    Devolve [True, mensagem] ou [False, lista_de_problemas].
    """
    problemas = validar_registro(registro_corrigido, sistema["por_id"])
    if len(problemas) > 0:
        sistema["inconsistentes"][indice]["registro"] = registro_corrigido
        sistema["inconsistentes"][indice]["problemas"] = problemas
        return [False, problemas]
    sistema["inconsistentes"].pop(indice)
    adicionar_ocorrencia(sistema, registro_para_ocorrencia(registro_corrigido))
    return [True, "Registro " + registro_corrigido["id"] + " corrigido e incluído no sistema."]
