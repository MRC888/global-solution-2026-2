# dados.py
# Leitura e gravação dos arquivos CSV.
#
# Formato dos arquivos: texto UTF-8, uma linha por registro, campos separados por ";".
# A primeira linha é o cabeçalho com o nome dos campos.

import os

# Os caminhos são montados a partir da pasta deste arquivo. Assim o programa
# acha os dados de qualquer pasta onde for executado.
PASTA_SRC = os.path.dirname(os.path.abspath(__file__))
PASTA_PROJETO = os.path.dirname(PASTA_SRC)                 # 1CC/GLOBAL-SOLUTION-2
PASTA_DADOS = os.path.join(PASTA_PROJETO, "data")
PASTA_SAIDA = os.path.join(PASTA_DADOS, "saida")

ARQUIVO_OCORRENCIAS = os.path.join(PASTA_DADOS, "ocorrencias.csv")
ARQUIVO_HISTORICO = os.path.join(PASTA_DADOS, "historico.csv")

# O painel HTML (bônus) fica na pasta "painel" na raiz do repositório.
PASTA_REPOSITORIO = os.path.dirname(os.path.dirname(PASTA_PROJETO))
PASTA_PAINEL = os.path.join(PASTA_REPOSITORIO, "painel")

# Ordem dos campos em cada arquivo.
CAMPOS_OCORRENCIA = ["id", "categoria", "descricao", "local", "dia", "status"]
CAMPOS_EVENTO = ["id", "dia", "anterior", "novo", "observacao"]

CABECALHO_OCORRENCIAS = "id;categoria;descricao;local;dia;status"
CABECALHO_HISTORICO = "id;dia;status_anterior;status_novo;observacao"


def ler_linhas(caminho):
    """Lê um arquivo de texto e devolve a lista de linhas não vazias.

    Devolve None se o arquivo não existir (o sistema avisa em vez de quebrar).
    """
    if not os.path.exists(caminho):
        return None
    linhas = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.rstrip("\r\n")
            if linha.strip() != "":
                linhas.append(linha)
    return linhas


def ler_registros(caminho, campos):
    """Lê um CSV e devolve uma lista de dicionários (um por linha, sem o cabeçalho).

    Todos os valores ficam como texto. A conversão do dia para número só
    acontece depois da validação.
    Se uma linha tiver campos a menos, os que faltam ficam vazios, e a
    validação aponta o problema.
    """
    linhas = ler_linhas(caminho)
    if linhas is None:
        return None
    registros = []
    for linha in linhas[1:]:            # [1:] pula o cabeçalho
        partes = linha.split(";")
        while len(partes) < len(campos):
            partes.append("")
        registro = {}
        for i in range(len(campos)):
            registro[campos[i]] = partes[i].strip()
        registros.append(registro)
    return registros


def ler_ocorrencias():
    """Lê data/ocorrencias.csv e devolve a lista de registros (ou None se o arquivo não existir)."""
    return ler_registros(ARQUIVO_OCORRENCIAS, CAMPOS_OCORRENCIA)


def ler_historico():
    """Lê data/historico.csv e devolve a lista de eventos (ou None se o arquivo não existir)."""
    return ler_registros(ARQUIVO_HISTORICO, CAMPOS_EVENTO)


def gravar_linhas(caminho, cabecalho, linhas):
    """Grava o cabeçalho e as linhas em um arquivo de texto."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(cabecalho + "\n")
        for linha in linhas:
            arquivo.write(linha + "\n")


def salvar_sessao(sistema):
    """Salva o estado atual em data/saida/, sem mexer nos arquivos originais (decisão D10).

    Assim o vídeo e os testes sempre partem dos mesmos dados.
    Devolve a lista com os caminhos gravados.
    """
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    linhas = []
    for oc in sistema["ocorrencias"]:
        linhas.append(oc["id"] + ";" + oc["categoria"] + ";" + oc["descricao"] + ";"
                      + oc["local"] + ";" + str(oc["dia"]) + ";" + oc["status"])
    # Os registros inconsistentes também são gravados, do jeito que vieram,
    # para nenhuma informação se perder.
    for item in sistema["inconsistentes"]:
        reg = item["registro"]
        linhas.append(reg["id"] + ";" + reg["categoria"] + ";" + reg["descricao"] + ";"
                      + reg["local"] + ";" + reg["dia"] + ";" + reg["status"])
    caminho_ocorrencias = os.path.join(PASTA_SAIDA, "ocorrencias_sessao.csv")
    gravar_linhas(caminho_ocorrencias, CABECALHO_OCORRENCIAS, linhas)

    linhas = []
    for ev in sistema["historico"]:
        linhas.append(ev["id"] + ";" + str(ev["dia"]) + ";" + ev["anterior"] + ";"
                      + ev["novo"] + ";" + ev["observacao"])
    caminho_historico = os.path.join(PASTA_SAIDA, "historico_sessao.csv")
    gravar_linhas(caminho_historico, CABECALHO_HISTORICO, linhas)

    return [caminho_ocorrencias, caminho_historico]
