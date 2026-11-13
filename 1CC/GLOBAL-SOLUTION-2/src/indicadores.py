# indicadores.py
# Cálculo dos indicadores com operações simples e laços (sem bibliotecas de análise).
#
# I1/I2  total e proporção por categoria
# I3     total e proporção por status
# I4     matriz categoria x status (montada em estruturas.py)
# I5     pendências = abertas + em análise
# I6     tempo médio até a conclusão
# I7     dias em aberto das pendentes, por categoria
# Extra  score de prioridade e conclusão escrita por regras

from validacao import (CATEGORIAS, STATUS, DIA_HOJE, PESOS, NOMES_CATEGORIAS, eh_pendente)


def formatar_numero(valor):
    """Escreve o número com 2 casas e vírgula, no padrão brasileiro: 5.333 -> "5,33"."""
    texto = f"{valor:.2f}"
    return texto.replace(".", ",")


def proporcao(parte, total):
    """Porcentagem: parte ÷ total × 100. Se o total for zero, devolve 0 (não divide por zero)."""
    if total == 0:
        return 0.0
    return parte / total * 100


def contar_por_categoria(ocorrencias):
    """I1: conta quantas ocorrências existem em cada categoria."""
    contagem = {}
    for categoria in CATEGORIAS:
        contagem[categoria] = 0
    for oc in ocorrencias:
        contagem[oc["categoria"]] = contagem[oc["categoria"]] + 1
    return contagem


def contar_por_status(ocorrencias):
    """I3: conta quantas ocorrências existem em cada status."""
    contagem = {}
    for status in STATUS:
        contagem[status] = 0
    for oc in ocorrencias:
        contagem[oc["status"]] = contagem[oc["status"]] + 1
    return contagem


def contar_pendencias(ocorrencias):
    """I5: pendência = toda ocorrência que NÃO está concluída (regra L6)."""
    total = 0
    for oc in ocorrencias:
        if eh_pendente(oc):
            total = total + 1
    return total


def dia_de_conclusao(historico, codigo):
    """Procura no histórico o dia em que a ocorrência foi concluída (o último evento que levou a "concluida")."""
    dia = None
    for evento in historico:
        if evento["id"] == codigo and evento["novo"] == "concluida":
            dia = evento["dia"]
    return dia


def tempo_ate_conclusao(sistema):
    """I6: tempo médio = soma de (dia da conclusão − dia de abertura) ÷ número de concluídas.

    Devolve um dicionário com a soma, a quantidade, a média, o detalhe de cada
    ocorrência (dados de origem) e os códigos concluídos sem registro no histórico.
    """
    detalhes = []
    sem_registro = []
    soma = 0
    for oc in sistema["ocorrencias"]:
        if oc["status"] == "concluida":
            dia_fim = dia_de_conclusao(sistema["historico"], oc["id"])
            if dia_fim is None:
                sem_registro.append(oc["id"])
            else:
                dias = dia_fim - oc["dia"]
                soma = soma + dias
                detalhes.append({"id": oc["id"], "abertura": oc["dia"], "conclusao": dia_fim, "dias": dias})
    quantidade = len(detalhes)
    if quantidade > 0:
        media = soma / quantidade
    else:
        media = 0.0
    return {"soma": soma, "quantidade": quantidade, "media": media,
            "detalhes": detalhes, "sem_registro": sem_registro}


def dias_em_aberto_por_categoria(sistema):
    """I7: para as pendentes de cada categoria, média de (dia de hoje − dia de abertura)."""
    resultado = {}
    for categoria in CATEGORIAS:
        resultado[categoria] = {"soma": 0, "quantidade": 0, "media": 0.0}
    for oc in sistema["ocorrencias"]:
        if eh_pendente(oc):
            item = resultado[oc["categoria"]]
            item["soma"] = item["soma"] + (DIA_HOJE - oc["dia"])
            item["quantidade"] = item["quantidade"] + 1
    for categoria in CATEGORIAS:
        item = resultado[categoria]
        if item["quantidade"] > 0:
            item["media"] = item["soma"] / item["quantidade"]
    return resultado


def score_prioridade(ocorrencia):
    """Score = dias em aberto × peso da categoria. Quanto maior, mais urgente."""
    return (DIA_HOJE - ocorrencia["dia"]) * PESOS[ocorrencia["categoria"]]


def ranking_prioridade(sistema):
    """Ordena as pendentes do maior score para o menor, por ordenação por inserção.

    Cada item novo anda pela lista até achar o primeiro score menor que o dele
    e é inserido ali. Em caso de empate, quem foi registrado antes fica na frente.
    """
    ranking = []
    for oc in sistema["ocorrencias"]:
        if eh_pendente(oc):
            item = {"id": oc["id"], "categoria": oc["categoria"], "local": oc["local"],
                    "dias": DIA_HOJE - oc["dia"], "peso": PESOS[oc["categoria"]],
                    "score": score_prioridade(oc)}
            posicao = 0
            while posicao < len(ranking) and ranking[posicao]["score"] >= item["score"]:
                posicao = posicao + 1
            ranking.insert(posicao, item)
    return ranking


def local_mais_comum(ocorrencias):
    """Devolve o local que mais aparece na lista (o primeiro, em caso de empate)."""
    contagem = {}
    ordem = []
    for oc in ocorrencias:
        if oc["local"] not in contagem:
            contagem[oc["local"]] = 0
            ordem.append(oc["local"])
        contagem[oc["local"]] = contagem[oc["local"]] + 1
    melhor = ""
    maior = 0
    for local in ordem:
        if contagem[local] > maior:
            maior = contagem[local]
            melhor = local
    return melhor


def gerar_conclusao(sistema):
    """Escreve a interpretação dos números usando regras com if (decisão D11).

    Devolve uma lista de frases.
    """
    ocorrencias = sistema["ocorrencias"]
    total = len(ocorrencias)
    if total == 0:
        return ["Não há ocorrências cadastradas para analisar."]

    frases = []

    # 1) Quanto ainda está pendente?
    pendentes = contar_pendencias(ocorrencias)
    porcentagem = proporcao(pendentes, total)
    if porcentagem > 50:
        frases.append("Mais da metade das ocorrências (" + formatar_numero(porcentagem)
                      + "%) ainda está pendente: o bairro tem demandas acumuladas.")
    elif porcentagem > 0:
        frases.append(formatar_numero(porcentagem) + "% das ocorrências ainda estão pendentes.")
    else:
        frases.append("Todas as ocorrências foram concluídas.")

    # 2) Qual categoria tem mais registros?
    contagem = contar_por_categoria(ocorrencias)
    mais_frequente = CATEGORIAS[0]
    for categoria in CATEGORIAS:
        if contagem[categoria] > contagem[mais_frequente]:
            mais_frequente = categoria
    frases.append("A categoria com mais registros é " + NOMES_CATEGORIAS[mais_frequente] + " ("
                  + str(contagem[mais_frequente]) + " de " + str(total) + ").")

    # 3) Qual categoria espera há mais tempo?
    dias = dias_em_aberto_por_categoria(sistema)
    pior = ""
    for categoria in CATEGORIAS:
        if dias[categoria]["quantidade"] > 0:
            if pior == "" or dias[categoria]["media"] > dias[pior]["media"]:
                pior = categoria
    if pior != "":
        pendentes_da_categoria = []
        for oc in ocorrencias:
            if oc["categoria"] == pior and eh_pendente(oc):
                pendentes_da_categoria.append(oc)
        frases.append("A categoria com mais tempo em aberto é " + NOMES_CATEGORIAS[pior] + " ("
                      + formatar_numero(dias[pior]["media"]) + " dias em média), e a maior parte "
                      + "dessas pendências fica em: " + local_mais_comum(pendentes_da_categoria) + ".")
        if pior == "acessibilidade":
            frases.append("Isso sugere priorizar acessibilidade, que afeta quem tem mobilidade reduzida.")

    # 4) Quanto tempo leva para resolver?
    tempo = tempo_ate_conclusao(sistema)
    if tempo["quantidade"] > 0:
        frases.append("As ocorrências concluídas levaram em média " + formatar_numero(tempo["media"])
                      + " dias para serem resolvidas.")

    return frases
