# painel_html.py
# Caminho 2 (bônus): gera as páginas HTML do painel a partir dos dados do sistema.
#
# COMO FUNCIONA
# Uma página HTML é só um arquivo de texto. Então o Python monta esse texto
# pedaço por pedaço (strings, laços e if) e grava em um arquivo, do mesmo jeito
# que grava um CSV. Não há biblioteca, servidor nem JavaScript: o navegador
# só abre o arquivo pronto.
#
# PÁGINAS GERADAS (na pasta "painel", na raiz do repositório)
#   painel.html        Início: resumo (cartões, matriz, barras e conclusão)
#   solicitacoes.html  Detalhes: tempos, prioridade, lista, histórico e inconsistências
#
# As duas usam o mesmo style.css das páginas feitas à mão (Sobre e Formulário),
# por isso o visual é o mesmo. Para atualizar os números, basta rodar o sistema
# de novo e escolher o caminho 2: as páginas são reescritas com os dados atuais.

import os

import dados
import indicadores
from validacao import (BAIRRO, CATEGORIAS, STATUS, DIA_HOJE, NOMES_CATEGORIAS,
                       NOMES_STATUS, SIGNIFICADO_STATUS)
from estruturas import descrever_inconsistencia

# Onde cada página é gravada.
ARQUIVO_INICIO = os.path.join(dados.PASTA_PAINEL, "painel.html")
ARQUIVO_SOLICITACOES = os.path.join(dados.PASTA_PAINEL, "solicitacoes.html")

# Classe do CSS de cada status: define a cor do cartão e do pedaço da barra empilhada.
CLASSE_STATUS = {"aberta": "aberta", "em_analise": "analise", "concluida": "concluida"}

# Rótulo de cada status nos cartões do resumo (no plural, como na página original).
ROTULO_CARTAO = {"aberta": "Abertas", "em_analise": "Em análise", "concluida": "Concluídas"}


# ---------------------------------------------------------------
# Funções de apoio
# ---------------------------------------------------------------

def escapar(texto):
    """Troca os caracteres especiais do HTML por códigos seguros.

    Por quê: se uma descrição tivesse "<b>", o navegador entenderia como
    código e mudaria a página. Escapando, o texto aparece exatamente como
    foi digitado. O "&" tem de ser trocado primeiro, senão estragaria os
    códigos criados nas trocas seguintes.
    """
    texto = str(texto)
    texto = texto.replace("&", "&amp;")
    texto = texto.replace("<", "&lt;")
    texto = texto.replace(">", "&gt;")
    texto = texto.replace('"', "&quot;")
    return texto


def largura_css(porcentagem):
    """Escreve a largura de uma barra para o CSS, por exemplo "31.25%".

    Atenção: no CSS o decimal é com PONTO. Com vírgula ("31,25%") o navegador
    ignora a largura e a barra some. Por isso aqui não se usa formatar_numero.
    rstrip tira os zeros desnecessários: 25.00 vira "25%".
    """
    return f"{porcentagem:.2f}".rstrip("0").rstrip(".") + "%"


def cabecalho_pagina(titulo_aba):
    """Início de toda página: <head>, banner e menu (iguais aos das páginas feitas à mão)."""
    return f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{titulo_aba}</title>
    <link rel="stylesheet" href="style.css">
    <link rel="icon" href="../assets/logo-fiap.png" type="image/png">
</head>
<body>
    <!-- Página gerada automaticamente por 1CC/GLOBAL-SOLUTION-2/src/painel_html.py.
         Não edite à mão: rode "python src/sistema.py", caminho 2, para gerar de novo. -->
    <header id="banner" class="banner">
        <h1>Neighborhood Action Dashboard</h1>
    </header>

<nav class="nav">
    <ul>
        <li><a href="painel.html">Inicio</a></li>
        <li><a href="sobre.html">Sobre</a></li>
        <li><a href="formulario.html">Formulario</a></li>
        <li><a href="solicitacoes.html">Solicitações</a></li>
    </ul>
</nav>

<main class="conteudo">
"""


def rodape_pagina():
    """Fim de toda página: rodapé com a logo e o aviso de trabalho acadêmico."""
    return """
</main>

<footer class="footer">
    <img src="../assets/logo-fiap.png" alt="FIAP" class="footer-logo">
    <p>Projeto acadêmico da Global Solution 2026.2 · Graduação em Ciência da Computação · FIAP</p>
    <p class="footer-aviso">
        Trabalho de faculdade, sem vínculo com prefeituras, órgãos públicos ou qualquer outra instituição.
        As ocorrências exibidas são fictícias e nenhuma solicitação é encaminhada ou atendida de verdade.
    </p>
</footer>
</body>
</html>
"""


def introducao(titulo, texto):
    """Título da página e um parágrafo dizendo de onde vêm os números."""
    return (f"\n    <h2>{titulo}</h2>\n"
            f"    <p>{texto} Dados do bairro fictício {BAIRRO}, dia simulado {DIA_HOJE}. "
            "Gerado pelo sistema em Python: para atualizar, rode o sistema e escolha o caminho 2.</p>\n")


# ---------------------------------------------------------------
# Seções da página Início (resumo)
# ---------------------------------------------------------------

def secao_cartoes(sistema):
    """Cartões com os totais: geral, um por status e pendências.

    Cada cartão recebe a classe do status (aberta, analise, concluida), que
    no style.css define a cor da borda.
    """
    ocorrencias = sistema["ocorrencias"]
    por_status = indicadores.contar_por_status(ocorrencias)
    html = '\n    <section class="cartoes">\n'
    html += (f'        <div class="cartao"><span class="numero">{len(ocorrencias)}</span>'
             '<span class="rotulo">Total</span></div>\n')
    for status in STATUS:
        html += (f'        <div class="cartao {CLASSE_STATUS[status]}"><span class="numero">{por_status[status]}</span>'
                 f'<span class="rotulo">{ROTULO_CARTAO[status]}</span></div>\n')
    html += (f'        <div class="cartao"><span class="numero">{indicadores.contar_pendencias(ocorrencias)}</span>'
             '<span class="rotulo">Pendências</span></div>\n')
    html += "    </section>\n"
    return html


def secao_matriz(sistema):
    """Tabela da MATRIZ categoria × status, com os totais de cada linha e coluna.

    Percorre a matriz com dois laços (linha = categoria, coluna = status),
    escrevendo uma célula <td> por valor e somando os totais no caminho.
    """
    matriz = sistema["matriz"]
    html = "\n    <section>\n        <h2>Ocorrências por categoria e status</h2>\n"
    html += '        <table class="tabela">\n'
    html += "            <caption>Matriz categoria × status: cada célula é a quantidade de ocorrências</caption>\n"
    html += '            <thead><tr><th scope="col">Categoria</th>'
    for status in STATUS:
        html += f'<th scope="col">{NOMES_STATUS[status]}</th>'
    html += '<th scope="col">Total</th></tr></thead>\n            <tbody>\n'

    totais_coluna = []                       # um total por status, começando em zero
    for status in STATUS:
        totais_coluna.append(0)

    for linha in range(len(CATEGORIAS)):
        html += f'                <tr><th scope="row">{NOMES_CATEGORIAS[CATEGORIAS[linha]]}</th>'
        total_linha = 0
        for coluna in range(len(STATUS)):
            valor = matriz[linha][coluna]
            total_linha = total_linha + valor
            totais_coluna[coluna] = totais_coluna[coluna] + valor
            html += f"<td>{valor}</td>"
        html += f"<td>{total_linha}</td></tr>\n"

    html += '            </tbody>\n            <tfoot><tr><th scope="row">Total</th>'
    total_geral = 0
    for valor in totais_coluna:
        total_geral = total_geral + valor
        html += f"<td>{valor}</td>"
    html += f"<td>{total_geral}</td></tr></tfoot>\n        </table>\n    </section>\n"
    return html


def secao_barras(sistema):
    """Gráfico de barras por categoria e barra empilhada por status, só com CSS.

    Cada barra é uma <div> com largura em porcentagem dentro de um "trilho"
    cinza: 5 de 16 ocorrências = 31,25%, então a barra ocupa 31,25% do trilho.
    O número também aparece escrito, para a informação não depender só da cor.
    """
    ocorrencias = sistema["ocorrencias"]
    total = len(ocorrencias)
    contagem = indicadores.contar_por_categoria(ocorrencias)
    html = "\n    <section>\n        <h2>Proporção por categoria</h2>\n"
    html += "        <p>Fórmula: total da categoria ÷ total geral × 100.</p>\n"
    html += '        <div class="grafico">\n'
    for categoria in CATEGORIAS:
        pct = indicadores.proporcao(contagem[categoria], total)
        html += ('            <div class="linha">\n'
                 f'                <span class="nome">{NOMES_CATEGORIAS[categoria]}</span>\n'
                 f'                <div class="trilho"><div class="barra" style="width: {largura_css(pct)}"></div></div>\n'
                 f'                <span class="valor">{contagem[categoria]} ({indicadores.formatar_numero(pct)}%)</span>\n'
                 '            </div>\n')
    html += "        </div>\n    </section>\n"

    por_status = indicadores.contar_por_status(ocorrencias)
    html += "\n    <section>\n        <h2>Situação geral</h2>\n"
    html += '        <div class="empilhada">\n'
    for status in STATUS:
        if por_status[status] > 0:      # status com zero não desenha pedaço vazio
            pct = indicadores.proporcao(por_status[status], total)
            html += (f'            <div class="{CLASSE_STATUS[status]}" style="width: {largura_css(pct)}">'
                     f'{NOMES_STATUS[status]} {por_status[status]}</div>\n')
    html += "        </div>\n        <ul>\n"
    for status in STATUS:
        html += f"            <li><strong>{NOMES_STATUS[status]}:</strong> {SIGNIFICADO_STATUS[status]}.</li>\n"
    html += "        </ul>\n    </section>\n"
    return html


def secao_conclusao(sistema):
    """As frases da conclusão, geradas por regras em indicadores.gerar_conclusao."""
    html = "\n    <section>\n        <h2>O que os números sugerem</h2>\n"
    for frase in indicadores.gerar_conclusao(sistema):
        html += f"        <p>{escapar(frase)}</p>\n"
    # A classe "botao-link" (definida no style.css) faz o link parecer um botão.
    # A seta fica em um <span aria-hidden>, para o leitor de tela não ler "seta".
    html += ('        <p><a class="botao-link" href="solicitacoes.html">Ver todas as solicitações '
             'e o detalhe de cada indicador <span aria-hidden="true">→</span></a></p>\n'
             "    </section>\n")
    return html


# ---------------------------------------------------------------
# Seções da página Solicitações (detalhes)
# ---------------------------------------------------------------

def secao_tempos(sistema):
    """Tempo médio até a conclusão (I6) e dias em aberto por categoria (I7), com as fórmulas."""
    tempo = indicadores.tempo_ate_conclusao(sistema)
    html = "\n    <section>\n        <h2>Tempo de acompanhamento</h2>\n"
    html += (f"        <p><strong>Tempo médio até a conclusão: {indicadores.formatar_numero(tempo['media'])} dias</strong> "
             f"(soma de {tempo['soma']} dias ÷ {tempo['quantidade']} concluídas). "
             "Fórmula: média de (dia da conclusão − dia de abertura).</p>\n")
    if len(tempo["sem_registro"]) > 0:
        html += ("        <p>Concluídas sem data de conclusão no histórico (fora da média): "
                 + escapar(", ".join(tempo["sem_registro"])) + ".</p>\n")

    dias = indicadores.dias_em_aberto_por_categoria(sistema)
    html += '        <table class="tabela">\n'
    html += f"            <caption>Dias em aberto das pendentes, por categoria (hoje = dia {DIA_HOJE})</caption>\n"
    html += ('            <thead><tr><th scope="col">Categoria</th><th scope="col">Pendentes</th>'
             '<th scope="col">Soma dos dias</th><th scope="col">Média de dias</th></tr></thead>\n            <tbody>\n')
    for categoria in CATEGORIAS:
        item = dias[categoria]
        html += (f'                <tr><th scope="row">{NOMES_CATEGORIAS[categoria]}</th><td>{item["quantidade"]}</td>'
                 f'<td>{item["soma"]}</td><td>{indicadores.formatar_numero(item["media"])}</td></tr>\n')
    html += "            </tbody>\n        </table>\n    </section>\n"
    return html


def secao_prioridade(sistema):
    """As 5 pendências mais urgentes pelo score (dias em aberto × peso), com o cálculo de cada uma."""
    ranking = indicadores.ranking_prioridade(sistema)
    html = "\n    <section>\n        <h2>Prioridade das pendências</h2>\n"
    html += "        <p>Score = dias em aberto × peso da categoria (acessibilidade 3, iluminação 2, conservação 2, limpeza 1).</p>\n"
    html += '        <table class="tabela">\n            <caption>As 5 pendências mais urgentes</caption>\n'
    html += ('            <thead><tr><th scope="col">Posição</th><th scope="col">Código</th><th scope="col">Categoria</th>'
             '<th scope="col">Local</th><th scope="col">Cálculo</th><th scope="col">Score</th></tr></thead>\n            <tbody>\n')
    posicao = 1
    for item in ranking[:5]:                 # [:5] pega só os 5 primeiros do ranking
        html += (f'                <tr><td>{posicao}º</td><th scope="row">{item["id"]}</th>'
                 f'<td>{NOMES_CATEGORIAS[item["categoria"]]}</td><td>{escapar(item["local"])}</td>'
                 f'<td>{item["dias"]} × {item["peso"]}</td><td>{item["score"]}</td></tr>\n')
        posicao = posicao + 1
    html += "            </tbody>\n        </table>\n    </section>\n"
    return html


def secao_lista(sistema):
    """Tabela com todas as ocorrências válidas, percorrendo a LISTA na ordem de registro."""
    html = "\n    <section>\n        <h2>Todas as ocorrências</h2>\n"
    html += '        <table class="tabela">\n            <caption>Lista completa, na ordem de registro</caption>\n'
    html += ('            <thead><tr><th scope="col">Código</th><th scope="col">Categoria</th><th scope="col">Descrição</th>'
             '<th scope="col">Local</th><th scope="col">Dia</th><th scope="col">Status</th></tr></thead>\n            <tbody>\n')
    for oc in sistema["ocorrencias"]:
        html += (f'                <tr><th scope="row">{oc["id"]}</th><td>{NOMES_CATEGORIAS[oc["categoria"]]}</td>'
                 f'<td>{escapar(oc["descricao"])}</td><td>{escapar(oc["local"])}</td><td>{oc["dia"]}</td>'
                 f'<td>{NOMES_STATUS[oc["status"]]}</td></tr>\n')
    html += "            </tbody>\n        </table>\n    </section>\n"
    return html


def secao_historico(sistema):
    """Os 8 eventos mais recentes do histórico, lendo a lista de trás para a frente."""
    historico = sistema["historico"]
    html = "\n    <section>\n        <h2>Últimas atualizações</h2>\n"
    html += '        <table class="tabela">\n            <caption>Os 8 eventos mais recentes do histórico, do mais novo para o mais antigo</caption>\n'
    html += ('            <thead><tr><th scope="col">Dia</th><th scope="col">Código</th><th scope="col">De</th>'
             '<th scope="col">Para</th><th scope="col">Observação</th></tr></thead>\n            <tbody>\n')
    indice = len(historico) - 1              # começa no último evento (o mais novo)
    mostrados = 0
    while indice >= 0 and mostrados < 8:
        ev = historico[indice]
        anterior = NOMES_STATUS.get(ev["anterior"], ev["anterior"])
        html += (f'                <tr><td>{ev["dia"]}</td><th scope="row">{ev["id"]}</th><td>{escapar(anterior)}</td>'
                 f'<td>{NOMES_STATUS[ev["novo"]]}</td><td>{escapar(ev["observacao"])}</td></tr>\n')
        indice = indice - 1
        mostrados = mostrados + 1
    html += "            </tbody>\n        </table>\n    </section>\n"
    return html


def secao_inconsistencias(sistema):
    """Registros separados pela validação, com o motivo (eles não entram nos números)."""
    html = "\n    <section>\n        <h2>Registros com problema</h2>\n"
    if len(sistema["inconsistentes"]) == 0:
        html += "        <p>Nenhum registro inconsistente.</p>\n"
    else:
        html += "        <p>Estes registros foram separados pela validação e não entram nos números:</p>\n        <ul>\n"
        for item in sistema["inconsistentes"]:
            html += f"            <li>{escapar(descrever_inconsistencia(item))}</li>\n"
        html += "        </ul>\n"
    html += "    </section>\n"
    return html


# ---------------------------------------------------------------
# Montagem e gravação das páginas
# ---------------------------------------------------------------

def gerar_html_inicio(sistema):
    """Monta a página Início (resumo) e devolve o texto HTML."""
    html = cabecalho_pagina("Painel")
    html += introducao("Resumo das ocorrências", "Visão geral das demandas registradas no bairro.")
    html += secao_cartoes(sistema)
    html += secao_matriz(sistema)
    html += secao_barras(sistema)
    html += secao_conclusao(sistema)
    html += rodape_pagina()
    return html


def gerar_html_solicitacoes(sistema):
    """Monta a página Solicitações (detalhes) e devolve o texto HTML."""
    html = cabecalho_pagina("Solicitações")
    html += introducao("Solicitações e indicadores detalhados",
                       "Todas as ocorrências, o histórico e o cálculo de cada indicador.")
    html += secao_tempos(sistema)
    html += secao_prioridade(sistema)
    html += secao_lista(sistema)
    html += secao_historico(sistema)
    html += secao_inconsistencias(sistema)
    html += rodape_pagina()
    return html


def gravar(caminho, texto):
    """Grava o texto em um arquivo, em UTF-8 (para os acentos aparecerem certos)."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(texto)


def salvar_painel(sistema):
    """Gera e grava as duas páginas. Devolve a lista de caminhos, ou None se a pasta "painel" não existir."""
    if not os.path.isdir(dados.PASTA_PAINEL):
        return None
    gravar(ARQUIVO_INICIO, gerar_html_inicio(sistema))
    gravar(ARQUIVO_SOLICITACOES, gerar_html_solicitacoes(sistema))
    return [ARQUIVO_INICIO, ARQUIVO_SOLICITACOES]
