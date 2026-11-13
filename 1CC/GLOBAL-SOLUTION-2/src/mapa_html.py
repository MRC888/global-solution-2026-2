# mapa_html.py
# Gera o mapa interativo a partir das ocorrências válidas da simulação.
# HTML, SVG e JavaScript locais: nenhuma API, instalação ou biblioteca externa.
# O JavaScript fica no modelo (painel/mapa_template.html); o Python só preenche os dados.

import os

import dados
from validacao import DIA_HOJE, LOCAIS, NOMES_CATEGORIAS, NOMES_STATUS, STATUS

MODELO = os.path.join(dados.PASTA_PAINEL, "mapa_template.html")

# Posições visuais FIXAS ([x, y], em % do desenho) para os quatro locais da simulação.
# Elas NÃO representam coordenadas reais. A sequência irregular
# foi aprovada como composição gráfica do bairro fictício.
POSICOES = {
    "Praça Central": [[10.5, 27], [29, 20], [39, 34], [18, 43], [31, 37],
                      [9, 35], [37, 18], [21, 25], [35, 46], [16, 18]],
    "Entorno da Escola": [[59.5, 26], [76, 19], [88.5, 36], [69, 41],
                          [83, 26], [63, 15], [79, 46], [91, 20], [71, 31]],
    "Ponto de Ônibus": [[12, 70], [28, 87], [40, 72], [18, 91], [36, 61],
                        [8, 83], [27, 66], [39, 89], [17, 78]],
    "Entorno da UBS": [[60, 76], [75, 67], [89, 84], [69, 89], [91, 64],
                       [79, 80], [63, 62], [82, 93], [73, 57]],
}

ICONES = {
    "iluminacao": '<path d="M7 10h10l-2-5H9l-2 5Z"></path><path d="M12 10v11M9 14h6"></path>',
    "acessibilidade": '<circle cx="12" cy="4" r="2"></circle><path d="M12 7v7l-4 2M8 10h7l3 5M6 17a6 6 0 1 0 11 1"></path>',
    "limpeza": '<path d="M5 7h14M9 7V4h6v3M7 7l1 14h8l1-14M10 11v7M14 11v7"></path>',
    "conservacao": '<path d="M15 4a5 5 0 0 0-5 7L4 17a2 2 0 0 0 3 3l6-6a5 5 0 0 0 7-6l-3 3-4-1-1-4 3-2Z"></path>',
}

CHAVES_LOCAIS = {
    "Praça Central": "PRACA",
    "Entorno da Escola": "ESCOLA",
    "Ponto de Ônibus": "ONIBUS",
    "Entorno da UBS": "UBS",
}


def escapar(texto):
    """Evita que dados de ocorrências sejam interpretados como código HTML."""
    texto = str(texto)
    return (texto.replace("&", "&amp;").replace("<", "&lt;")
                 .replace(">", "&gt;").replace('"', "&quot;"))


def pino(oc, x, y):
    """Monta um marcador clicável, com todos os dados vindo do sistema."""
    categoria = oc["categoria"]
    status = oc["status"]
    codigo = escapar(oc["id"])
    descricao = escapar(oc["descricao"])
    local = escapar(oc["local"])
    dia = escapar(oc["dia"])
    nome_categoria = escapar(NOMES_CATEGORIAS[categoria])
    nome_status = escapar(NOMES_STATUS[status])
    return (
        f'<a aria-label="Ocorrência {codigo}: {nome_categoria}, {descricao}. {local}. '
        f'Situação: {nome_status}. Exibir ficha." '
        f'class="mapa-pino mapa-pino--{categoria}" data-dia="{dia}" '
        f'data-id="{codigo}" data-local="{local}" data-status="{status}" '
        f'href="#mapa-ficha" role="button" '
        f'style="left:{x}%;top:{y}%">'
        '<svg aria-hidden="true" fill="none" stroke="currentColor" '
        'stroke-linecap="round" stroke-linejoin="round" stroke-width="2" '
        'viewBox="0 0 24 24">'
        + ICONES[categoria] + '</svg>'
        f'<span aria-hidden="true" class="mapa-status mapa-status--{status}"></span>'
        '<span aria-hidden="true" class="mapa-dica">'
        f'<b>#{codigo} · {nome_categoria}</b>'
        f'<small>{descricao}</small><em>{nome_status}</em>'
        '</span></a>\n'
    )


def gerar_mapa(sistema):
    """Preenche o modelo com marcadores e contagens dos registros VÁLIDOS.

    Devolve o texto HTML, ou None se o modelo não existir ou ficar incompleto.
    """
    if not os.path.isfile(MODELO):
        return None
    with open(MODELO, encoding="utf-8") as arquivo:
        html = arquivo.read()

    ocorrencias = sistema["ocorrencias"]
    por_local = {}
    for local in LOCAIS:
        por_local[local] = []
    por_status = {}
    for status in STATUS:
        por_status[status] = 0
    for oc in ocorrencias:
        if oc["local"] in por_local:
            por_local[oc["local"]].append(oc)
        por_status[oc["status"]] += 1

    html = html.replace("@@MAPA_TOTAL@@", str(len(ocorrencias)))
    html = html.replace("@@MAPA_DIA@@", str(DIA_HOJE))
    html = html.replace("@@MAPA_STATUS_TODAS@@", str(len(ocorrencias)))
    for status in STATUS:
        html = html.replace("@@MAPA_STATUS_" + status.upper() + "@@",
                            str(por_status[status]))

    marcadores = ""
    for local in LOCAIS:
        lista = por_local[local]
        quantidade = len(lista)
        unidade = "ocorrências"
        if quantidade == 1:
            unidade = "ocorrência"
        html = html.replace("@@MAPA_LOCAL_" + CHAVES_LOCAIS[local] + "@@ ocorrências",
                            str(quantidade) + " " + unidade)
        posicoes = POSICOES[local]
        limite = quantidade
        if limite > len(posicoes):
            limite = len(posicoes)
        for indice in range(limite):
            marcadores += pino(lista[indice], posicoes[indice][0], posicoes[indice][1])
        # Quando há muitos registros em uma mesma área, evita pino sobreposto
        # e informa quantos outros podem ser consultados na página Solicitações.
        excedente = quantidade - len(posicoes)
        if excedente > 0:
            marcadores += (
                f'<a class="mapa-excedentes" href="solicitacoes.html" target="_parent" '
                f'style="left:{posicoes[-1][0]}%;top:{posicoes[-1][1] + 5}%" '
                f'title="Mais {excedente} ocorrências neste local">'
                f'+{excedente} na lista</a>\n'
            )
    html = html.replace("@@MAPA_PINOS@@", marcadores)

    if "@@MAPA_" in html:
        return None   # o modelo tem um marcador que o Python não conhece
    return html


def secao_iframe_mapa():
    """Insere o mapa abaixo do menu e antes dos cinco indicadores."""
    return (
        '\n    <section class="secao-mapa-inicio" aria-label="Mapa interativo das ocorrências">\n'
        '        <iframe class="mapa-integrado" src="mapa.html" '
        'title="Mapa interativo da Vila Esperança: arraste, aplique zoom e consulte as ocorrências" '
        'loading="eager"></iframe>\n'
        '        <script src="script.js" defer></script>\n'
        '    </section>\n'
    )
