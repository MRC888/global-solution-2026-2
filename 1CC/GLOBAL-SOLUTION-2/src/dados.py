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
ARQUIVO_OCORRENCIAS_SALVAS = os.path.join(PASTA_SAIDA, "ocorrencias_sessao.csv")
ARQUIVO_HISTORICO_SALVO = os.path.join(PASTA_SAIDA, "historico_sessao.csv")

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


def ha_sessao_salva(pasta_saida=None):
    """Confere se existem os DOIS arquivos necessários para continuar uma sessão.

    A pasta opcional permite testar sem tocar nos dados reais do usuário.
    """
    if pasta_saida is None:
        pasta_saida = PASTA_SAIDA
    ocorrencias = os.path.join(pasta_saida, "ocorrencias_sessao.csv")
    historico = os.path.join(pasta_saida, "historico_sessao.csv")
    return os.path.isfile(ocorrencias) and os.path.isfile(historico)


def ler_ocorrencias(usar_sessao=False, pasta_saida=None):
    """Lê os dados originais ou a versão salva, conforme a escolha do usuário."""
    if usar_sessao:
        if pasta_saida is None:
            caminho = ARQUIVO_OCORRENCIAS_SALVAS
        else:
            caminho = os.path.join(pasta_saida, "ocorrencias_sessao.csv")
    else:
        caminho = ARQUIVO_OCORRENCIAS
    return ler_registros(caminho, CAMPOS_OCORRENCIA)


def ler_historico(usar_sessao=False, pasta_saida=None):
    """Lê o histórico original ou o salvo; mantém o mesmo formato CSV."""
    if usar_sessao:
        if pasta_saida is None:
            caminho = ARQUIVO_HISTORICO_SALVO
        else:
            caminho = os.path.join(pasta_saida, "historico_sessao.csv")
    else:
        caminho = ARQUIVO_HISTORICO
    return ler_registros(caminho, CAMPOS_EVENTO)


def gravar_linhas(caminho, cabecalho, linhas):
    """Grava o cabeçalho e as linhas em um arquivo de texto."""
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(cabecalho + "\n")
        for linha in linhas:
            arquivo.write(linha + "\n")


def salvar_sessao(sistema, pasta_saida=None):
    """Salva o estado atual em CSV sem alterar os dados fictícios originais.

    É chamada após cada alteração bem-sucedida e na saída do terminal.
    pasta_saida permite que o teste use uma pasta isolada.
    """
    if pasta_saida is None:
        pasta_saida = PASTA_SAIDA
    os.makedirs(pasta_saida, exist_ok=True)

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
    caminho_ocorrencias = os.path.join(pasta_saida, "ocorrencias_sessao.csv")
    gravar_linhas(caminho_ocorrencias, CABECALHO_OCORRENCIAS, linhas)

    linhas = []
    for ev in sistema["historico"]:
        linhas.append(ev["id"] + ";" + str(ev["dia"]) + ";" + ev["anterior"] + ";"
                      + ev["novo"] + ";" + ev["observacao"])
    caminho_historico = os.path.join(pasta_saida, "historico_sessao.csv")
    gravar_linhas(caminho_historico, CABECALHO_HISTORICO, linhas)

    return [caminho_ocorrencias, caminho_historico]
