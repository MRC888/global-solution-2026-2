# interface.py
# Tudo o que aparece no terminal: menus, tabelas, perguntas e mensagens.
#
# As regras ficam em validacao.py e operacoes.py. Aqui só se pergunta,
# chama a regra e mostra o resultado.
#
# Modo acessível: sem cores nem símbolos, cada ocorrência vira uma frase
# completa (melhor para leitores de tela) e o sistema pede confirmação
# antes de cada ação que altera dados.

import dados
import operacoes
import indicadores
from validacao import (BAIRRO, CATEGORIAS, STATUS, LOCAIS, DIA_HOJE, NOMES_CATEGORIAS,
                       NOMES_STATUS, SIGNIFICADO_STATUS, TRANSICOES, TAMANHO_MAXIMO_DESCRICAO,
                       dia_valido, sugerir_categoria, mensagens_dos_problemas, campos_com_problema,
                       verificar_transicao)
from estruturas import descrever_inconsistencia

# Configuração da sessão. É um dicionário para poder ser alterado dentro das funções.
CONFIG = {"acessivel": False}

# Códigos ANSI: fazem o terminal mudar a cor do texto, sem precisar de biblioteca.
CORES = {
    "vermelho": "\033[31m",
    "amarelo": "\033[33m",
    "verde": "\033[32m",
    "azul": "\033[36m",
    "negrito": "\033[1m",
    "fim": "\033[0m",
}
COR_STATUS = {"aberta": "vermelho", "em_analise": "amarelo", "concluida": "verde"}

OPCOES_MENU = [
    " 1. Listar todas as ocorrências",
    " 2. Buscar por código",
    " 3. Filtrar por categoria e/ou status",
    " 4. Cadastrar nova ocorrência",
    " 5. Triagem: chamar a próxima da fila",
    " 6. Atualizar status",
    " 7. Desfazer a última alteração",
    " 8. Ver histórico e eventos recentes",
    " 9. Explorar o bairro (hierarquia)",
    "10. Painel de indicadores",
    "11. Inconsistências (ver e corrigir)",
    "12. Alternar modo acessível",
    " 0. Salvar e voltar ao início",
]


# ---------------------------------------------------------------
# Funções básicas de tela e de leitura
# ---------------------------------------------------------------

def colorir(texto, cor):
    """Pinta o texto com a cor pedida. No modo acessível, devolve o texto sem cor."""
    if CONFIG["acessivel"]:
        return texto
    return CORES[cor] + texto + CORES["fim"]


def titulo(texto):
    """Mostra o título de uma tela. No modo acessível vira uma frase simples, sem linhas de enfeite."""
    print()
    if CONFIG["acessivel"]:
        print("Tela: " + texto)
    else:
        print(colorir("=" * 64, "azul"))
        print(colorir("  " + texto, "negrito"))
        print(colorir("=" * 64, "azul"))


def mensagem_ok(texto):
    """Mostra uma mensagem de sucesso (verde no modo normal; com a palavra "Concluído" no acessível)."""
    if CONFIG["acessivel"]:
        print("Concluído: " + texto)
    else:
        print(colorir("[OK] " + texto, "verde"))


def mensagem_erro(texto):
    """Mostra uma mensagem de erro ou aviso (vermelha no modo normal; com a palavra "Atenção" no acessível)."""
    if CONFIG["acessivel"]:
        print("Atenção: " + texto)
    else:
        print(colorir("[!] " + texto, "vermelho"))


def pausar():
    """Espera o Enter, para a pessoa ler o resultado antes de o menu aparecer de novo."""
    input("\nPressione Enter para continuar...")


def ler_texto(pergunta):
    """Lê o que foi digitado e tira os espaços das pontas (" 14 " vira "14")."""
    return input(pergunta).strip()


def ler_sim_nao(pergunta):
    """Repete a pergunta até a resposta ser s ou n. Devolve True para "s"."""
    while True:
        resposta = ler_texto(pergunta + " (s/n): ").lower()
        if resposta == "s":
            return True
        elif resposta == "n":
            return False
        else:
            mensagem_erro("Responda só com s (sim) ou n (não).")


def confirmar_se_acessivel(pergunta):
    """No modo acessível, toda ação que altera dados pede confirmação antes."""
    if CONFIG["acessivel"]:
        return ler_sim_nao(pergunta)
    return True


def salvar_automaticamente(sistema):
    """Persiste a lista e o histórico após mudanças; preserva os CSVs originais."""
    dados.salvar_sessao(sistema)
    print("Sessão salva automaticamente em data/saida/.")


def escolher_da_lista(pergunta, nomes, permitir_vazio):
    """Mostra uma lista numerada e devolve o índice escolhido (começa em 0).

    Se permitir_vazio for True, apertar Enter devolve -1 (significa "todos" ou "voltar").
    """
    for i in range(len(nomes)):
        print(f"  {i + 1}. {nomes[i]}")
    while True:
        dica = " (Enter = todas)" if permitir_vazio else ""
        resposta = ler_texto(pergunta + dica + ": ")
        if resposta == "" and permitir_vazio:
            return -1
        elif resposta.isdigit() and 1 <= int(resposta) <= len(nomes):
            return int(resposta) - 1
        else:
            mensagem_erro(f"Digite um número de 1 a {len(nomes)}.")


def nomes_das_categorias():
    """Lista com os nomes das categorias como aparecem na tela (com acento)."""
    nomes = []
    for categoria in CATEGORIAS:
        nomes.append(NOMES_CATEGORIAS[categoria])
    return nomes


def nomes_dos_status():
    """Lista com os nomes dos status como aparecem na tela (com acento)."""
    nomes = []
    for status in STATUS:
        nomes.append(NOMES_STATUS[status])
    return nomes


def ler_dia(pergunta):
    """Pede o dia até receber um número de 1 a 30."""
    while True:
        resposta = ler_texto(pergunta)
        if dia_valido(resposta):
            return resposta
        mensagem_erro("O dia deve ser um número de 1 a 30.")


def ler_descricao():
    """Pede a descrição até ela ser válida: não vazia, sem ";" e com até 120 caracteres."""
    while True:
        descricao = ler_texto(f"Descrição do problema (até {TAMANHO_MAXIMO_DESCRICAO} caracteres): ")
        if descricao == "":
            mensagem_erro("A descrição é obrigatória.")
        elif ";" in descricao:
            mensagem_erro("A descrição não pode ter ponto e vírgula (;).")
        elif len(descricao) > TAMANHO_MAXIMO_DESCRICAO:
            mensagem_erro(f"A descrição tem {len(descricao)} caracteres; o máximo é {TAMANHO_MAXIMO_DESCRICAO}.")
        else:
            return descricao


# ---------------------------------------------------------------
# Exibição de ocorrências
# ---------------------------------------------------------------

def texto_status(status):
    """Nome do status, colorido no modo normal."""
    nome = NOMES_STATUS.get(status, status)
    if status in COR_STATUS:
        return colorir(nome, COR_STATUS[status])
    return nome


def mostrar_tabela(lista):
    """Listagem legível: código, categoria, local, dia e status."""
    if CONFIG["acessivel"]:
        for oc in lista:
            print(f"Ocorrência {oc['id']}: {NOMES_CATEGORIAS[oc['categoria']]}, {oc['local']}, "
                  f"aberta no dia {oc['dia']}, situação {NOMES_STATUS[oc['status']]}.")
        return
    print("Código  Categoria        Local                Dia  Status")
    print("-" * 64)
    for oc in lista:
        linha = (oc["id"].ljust(8) + NOMES_CATEGORIAS[oc["categoria"]].ljust(17)
                 + oc["local"].ljust(20) + str(oc["dia"]).rjust(4) + "  ")
        print(linha + texto_status(oc["status"]))


def descrever_evento(evento):
    """Texto de um evento do histórico: uma linha curta no modo normal, uma frase completa no acessível."""
    anterior = NOMES_STATUS.get(evento["anterior"], evento["anterior"])
    novo = NOMES_STATUS.get(evento["novo"], evento["novo"])
    if CONFIG["acessivel"]:
        return (f"No dia {evento['dia']}, a ocorrência {evento['id']} passou de {anterior} "
                f"para {novo}. Observação: {evento['observacao']}.")
    return f"Dia {str(evento['dia']).rjust(2)} | {evento['id']} | {anterior} -> {novo} | {evento['observacao']}"


def mostrar_ficha(sistema, oc):
    """Ficha completa de uma ocorrência e o histórico dela."""
    print(f"Código:     {oc['id']}")
    print(f"Categoria:  {NOMES_CATEGORIAS[oc['categoria']]}")
    print(f"Descrição:  {oc['descricao']}")
    print(f"Local:      {oc['local']} ({BAIRRO})")
    print(f"Abertura:   dia {oc['dia']}")
    print(f"Status:     {texto_status(oc['status'])} ({SIGNIFICADO_STATUS[oc['status']]})")
    eventos = operacoes.eventos_da_ocorrencia(sistema, oc["id"])
    print("Histórico:")
    if len(eventos) == 0:
        print("  nenhuma mudança de status registrada")
    for evento in eventos:
        print("  " + descrever_evento(evento))


# ---------------------------------------------------------------
# Abertura e escolha do caminho
# ---------------------------------------------------------------

def mostrar_abertura():
    """Mostra o cabeçalho do sistema ao abrir o programa."""
    print()
    print("=" * 64)
    print("  NEIGHBORHOOD ACTION DASHBOARD")
    print(f"  Painel comunitário de ocorrências · {BAIRRO} (bairro fictício)")
    print("  Global Solution 2026.2 · FIAP · projeto acadêmico")
    print("=" * 64)


def mostrar_relatorio_carga(sistema):
    """Mostra o resultado da leitura dos arquivos e os problemas encontrados."""
    validos = len(sistema["ocorrencias"])
    inconsistentes = len(sistema["inconsistentes"])
    print(f"\nCarga dos dados: {sistema['lidos']} registros lidos, {validos} válidos, "
          f"{inconsistentes} inconsistentes, {len(sistema['historico'])} eventos no histórico.")
    for item in sistema["inconsistentes"]:
        print("  - registro " + descrever_inconsistencia(item) + " (corrija pela opção 11 do terminal)")
    for aviso in sistema["avisos_carga"]:
        print("  - " + aviso)


def escolher_origem_dados():
    """Pergunta se deve retomar uma sessão existente ou usar a base demonstrativa."""
    print("\nEncontrei uma sessão anterior salva em data/saida/.")
    print("  1 - Continuar do ponto em que parei")
    print("  2 - Recomeçar com os dados fictícios originais")
    print("A opção 2 não apaga os arquivos originais. Ao alterar ou salvar,")
    print("a nova sessão substitui a sessão salva anterior.")
    while True:
        resposta = ler_texto("Escolha 1 ou 2: ")
        if resposta == "1":
            return True
        elif resposta == "2":
            return False
        else:
            mensagem_erro("Digite 1 para continuar ou 2 para recomeçar.")


def escolher_caminho():
    """Os dois caminhos do sistema. Devolve "1", "2" ou "0"."""
    print()
    print("Como você quer usar o sistema?")
    print("  1 - Terminal: sistema completo (cadastro, consultas, status e indicadores)")
    print("  2 - Painel HTML (bônus): gera uma página com os indicadores para abrir no navegador")
    print("  0 - Sair")
    while True:
        opcao = ler_texto("Escolha 1, 2 ou 0: ")
        if opcao == "1" or opcao == "2" or opcao == "0":
            return opcao
        print("Opção inválida. Digite 1 (terminal), 2 (painel HTML) ou 0 (sair).")


def perguntar_modo_acessivel():
    """Pergunta se a pessoa quer o modo acessível e guarda a resposta em CONFIG (decisão D9)."""
    CONFIG["acessivel"] = ler_sim_nao("\nUsar o modo acessível? Sem cores nem símbolos, com frases "
                                      "completas e confirmação antes de cada ação.")


def mostrar_painel_gerado(caminhos):
    """Mostra onde as páginas do painel foram gravadas e como abri-las."""
    if caminhos is None:
        print("\nNão encontrei a pasta 'painel' na raiz do repositório, então o painel não foi gerado.")
        return
    print("\nPainel HTML gerado com os dados atuais da sessão:")
    for caminho in caminhos:
        print("  " + caminho)
    print("Abra o painel.html no navegador (dois cliques nele, ou arraste para uma aba).")
    print("Ele mostra os mesmos indicadores da opção 10 do terminal.")


# ---------------------------------------------------------------
# Telas do menu do terminal
# ---------------------------------------------------------------

def tela_listar(sistema):
    """Opção 1: percorre a LISTA de ocorrências e mostra todas em uma tabela."""
    titulo("Todas as ocorrências")
    if len(sistema["ocorrencias"]) == 0:
        print("Nenhuma ocorrência cadastrada.")
    else:
        mostrar_tabela(sistema["ocorrencias"])
        print(f"\nTotal exibido: {len(sistema['ocorrencias'])} ocorrências.")
    pausar()


def tela_buscar(sistema):
    """Opção 2: busca uma ocorrência pelo código usando o DICIONÁRIO por_id."""
    titulo("Buscar por código")
    codigo = ler_texto("Código da ocorrência (ex.: 14 ou 014): ")
    if codigo == "":
        mensagem_erro("Nenhum código digitado.")
    else:
        oc = operacoes.buscar(sistema, codigo)
        if oc is None:
            mensagem_erro(f"Ocorrência {operacoes.completar_codigo(codigo)} não encontrada.")
        else:
            print()
            mostrar_ficha(sistema, oc)
    pausar()


def tela_filtrar(sistema):
    """Opção 3: filtra por categoria e/ou status. Enter em um filtro significa "todas" (regra L3)."""
    titulo("Filtrar ocorrências")
    print("Categoria:")
    i = escolher_da_lista("Escolha a categoria", nomes_das_categorias(), True)
    categoria = "" if i == -1 else CATEGORIAS[i]
    print("Status:")
    i = escolher_da_lista("Escolha o status", nomes_dos_status(), True)
    status = "" if i == -1 else STATUS[i]

    nome_categoria = "todas" if categoria == "" else NOMES_CATEGORIAS[categoria]
    nome_status = "todos" if status == "" else NOMES_STATUS[status]
    print(f"\nFiltro: categoria = {nome_categoria}; status = {nome_status}\n")
    resultado = operacoes.filtrar(sistema, categoria, status)
    if len(resultado) == 0:
        print("Nenhuma ocorrência com esses filtros.")
    else:
        mostrar_tabela(resultado)
        print(f"\n{len(resultado)} ocorrência(s) encontrada(s).")
    pausar()


def tela_cadastrar(sistema):
    """Opção 4: pede cada campo, valida na hora e cadastra a ocorrência nova.

    Ordem: descrição -> sugestão de categoria -> categoria -> local -> dia ->
    aviso de possível duplicada (regra L5) -> cadastro. Cada campo é pedido de
    novo até ficar válido, então a pessoa só redigita o que errou."""
    titulo("Cadastrar nova ocorrência")
    print(f"O código será gerado automaticamente: {operacoes.proximo_codigo(sistema)}")
    print("Toda ocorrência nova começa com o status Aberta e entra no fim da fila de triagem.\n")

    descricao = ler_descricao()

    categoria = ""
    sugestao = sugerir_categoria(descricao)
    if sugestao != "":
        print(f"\nPela descrição, parece ser da categoria {NOMES_CATEGORIAS[sugestao]}.")
        if ler_sim_nao("Usar essa categoria?"):
            categoria = sugestao
    if categoria == "":
        print("\nCategoria:")
        categoria = CATEGORIAS[escolher_da_lista("Escolha a categoria", nomes_das_categorias(), False)]

    print("\nLocal (genérico, nunca o endereço de uma pessoa):")
    local = LOCAIS[escolher_da_lista("Escolha o local", LOCAIS, False)]

    dia = ler_dia(f"\nDia de abertura (1 a {DIA_HOJE}; hoje é o dia {DIA_HOJE}): ")

    duplicadas = operacoes.possiveis_duplicadas(sistema, categoria, local)
    if len(duplicadas) > 0:
        print("\nAtenção: já existe ocorrência não concluída da mesma categoria neste local:")
        mostrar_tabela(duplicadas)
        if not ler_sim_nao("Pode ser o mesmo problema. Cadastrar mesmo assim?"):
            print("Cadastro cancelado.")
            pausar()
            return

    if not confirmar_se_acessivel(f"Confirmar o cadastro de {NOMES_CATEGORIAS[categoria]} em {local}?"):
        print("Cadastro cancelado.")
        pausar()
        return

    resultado = operacoes.cadastrar(sistema, categoria, descricao, local, dia)
    if resultado[0]:
        nova = resultado[2]
        mensagem_ok(f"Ocorrência {nova['id']} cadastrada e colocada na fila "
                    f"(posição {len(sistema['fila'])} de {len(sistema['fila'])}).")
        salvar_automaticamente(sistema)
    else:
        mensagem_erro("Cadastro recusado: " + mensagens_dos_problemas(resultado[1]))
    pausar()


def pedir_mudanca(sistema, codigo, status_novo):
    """Pede a observação, confirma (modo acessível) e aplica a mudança de status."""
    observacao = ler_texto("Observação curta (opcional, Enter para pular): ")
    if not confirmar_se_acessivel(f"Confirmar a mudança da ocorrência {codigo} para {NOMES_STATUS[status_novo]}?"):
        print("Mudança cancelada.")
        return False
    resultado = operacoes.atualizar_status(sistema, codigo, status_novo, observacao)
    if resultado[0]:
        mensagem_ok(resultado[1])
        salvar_automaticamente(sistema)
    else:
        mensagem_erro(resultado[1])
    return resultado[0]


def tela_triagem(sistema):
    """Opção 5: tira a primeira ocorrência da FILA (a mais antiga) e pergunta se ela vai para análise.

    Se a resposta for não, a ocorrência volta para o começo da fila (decisão D7)."""
    titulo("Triagem: próxima da fila")
    codigo = operacoes.chamar_proximo(sistema)
    if codigo is None:
        print("Nenhuma ocorrência aguardando triagem.")
        pausar()
        return
    print(f"Próxima da fila (ainda aguardam depois dela: {len(sistema['fila'])}):\n")
    mostrar_ficha(sistema, sistema["por_id"][codigo])
    print()
    if ler_sim_nao("Marcar como Em análise?"):
        if not pedir_mudanca(sistema, codigo, "em_analise"):
            operacoes.devolver_para_fila(sistema, codigo)
            print(f"A ocorrência {codigo} voltou para o começo da fila.")
    else:
        operacoes.devolver_para_fila(sistema, codigo)
        print(f"A ocorrência {codigo} voltou para o começo da fila.")
    pausar()


def tela_atualizar(sistema):
    """Opção 6: muda o status de uma ocorrência, respeitando as transições permitidas."""
    titulo("Atualizar status")
    codigo = ler_texto("Código da ocorrência: ")
    oc = operacoes.buscar(sistema, codigo)
    if oc is None:
        mensagem_erro(f"Ocorrência {operacoes.completar_codigo(codigo)} não encontrada.")
        pausar()
        return
    print(f"\nOcorrência {oc['id']}: {oc['descricao']}")
    print(f"Status atual: {texto_status(oc['status'])}")
    permitidos = TRANSICOES[oc["status"]]
    if len(permitidos) == 0:
        print("Esta ocorrência está concluída e não muda mais de status.")
        pausar()
        return
    print(f"Próximo status permitido: {NOMES_STATUS[permitidos[0]]}\n")
    print("Novo status:")
    status_novo = STATUS[escolher_da_lista("Escolha o novo status", nomes_dos_status(), False)]
    # Confere a regra ANTES de pedir a observação: se a mudança é proibida, avisa na hora.
    resultado = verificar_transicao(oc["status"], status_novo)
    if resultado[0]:
        pedir_mudanca(sistema, oc["id"], status_novo)
    else:
        mensagem_erro(resultado[1])
    pausar()


def tela_desfazer(sistema):
    """Opção 7: mostra o topo da PILHA (a última mudança desta sessão) e desfaz essa mudança."""
    titulo("Desfazer a última alteração")
    if len(sistema["pilha"]) == 0:
        print("Nada para desfazer: nenhuma mudança de status foi feita nesta sessão.")
        pausar()
        return
    topo = sistema["pilha"][-1]          # só olha o topo, sem tirar
    print("Última alteração desta sessão:")
    print("  " + descrever_evento(topo))
    if confirmar_se_acessivel("Desfazer essa alteração?"):
        resultado = operacoes.desfazer(sistema)
        if resultado[0]:
            mensagem_ok(resultado[1])
            salvar_automaticamente(sistema)
        else:
            mensagem_erro(resultado[1])
    else:
        print("Nada foi desfeito.")
    pausar()


def tela_historico(sistema):
    """Opção 8: mostra os eventos mais recentes do histórico e a PILHA desta sessão, do topo para a base."""
    titulo("Histórico e eventos recentes")
    historico = sistema["historico"]
    print("Os 8 eventos mais recentes (do mais novo para o mais antigo):")
    indice = len(historico) - 1
    mostrados = 0
    while indice >= 0 and mostrados < 8:
        print("  " + descrever_evento(historico[indice]))
        indice = indice - 1
        mostrados = mostrados + 1
    if len(historico) == 0:
        print("  nenhum evento registrado")

    print(f"\nPilha de alterações desta sessão ({len(sistema['pilha'])}), do topo para a base:")
    if len(sistema["pilha"]) == 0:
        print("  vazia (nenhuma mudança feita nesta sessão)")
    indice = len(sistema["pilha"]) - 1
    while indice >= 0:
        print("  " + descrever_evento(sistema["pilha"][indice]))
        indice = indice - 1

    codigo = ler_texto("\nDigite um código para ver o histórico completo dele (Enter para voltar): ")
    if codigo != "":
        oc = operacoes.buscar(sistema, codigo)
        if oc is None:
            mensagem_erro(f"Ocorrência {operacoes.completar_codigo(codigo)} não encontrada.")
        else:
            print()
            mostrar_ficha(sistema, oc)
        pausar()


def tela_explorar(sistema):
    """Navega pela hierarquia bairro -> categoria -> ocorrência. 0 volta um nível."""
    hierarquia = sistema["hierarquia"][BAIRRO]
    while True:
        titulo(f"Explorar o bairro: {BAIRRO}")
        for i in range(len(CATEGORIAS)):
            categoria = CATEGORIAS[i]
            print(f"  {i + 1}. {NOMES_CATEGORIAS[categoria]} ({len(hierarquia[categoria])} ocorrências)")
        print("  0. Voltar ao menu")
        opcao = ler_texto("Escolha uma categoria: ")
        if opcao == "0":
            return
        elif opcao.isdigit() and 1 <= int(opcao) <= len(CATEGORIAS):
            categoria = CATEGORIAS[int(opcao) - 1]
            explorar_categoria(sistema, categoria, hierarquia[categoria])
        else:
            mensagem_erro(f"Digite um número de 0 a {len(CATEGORIAS)}.")


def explorar_categoria(sistema, categoria, codigos):
    """Segundo nível da HIERARQUIA: mostra as ocorrências de uma categoria e abre a ficha de uma delas."""
    while True:
        titulo(f"{BAIRRO} > {NOMES_CATEGORIAS[categoria]}")
        if len(codigos) == 0:
            print("Nenhuma ocorrência nesta categoria.")
            pausar()
            return
        lista = []
        for codigo in codigos:
            lista.append(sistema["por_id"][codigo])
        mostrar_tabela(lista)
        codigo = ler_texto("\nDigite um código para ver a ficha (0 para voltar): ")
        if codigo == "0":
            return
        codigo = operacoes.completar_codigo(codigo)
        if codigo in codigos:
            print()
            mostrar_ficha(sistema, sistema["por_id"][codigo])
            pausar()
        else:
            mensagem_erro("Esse código não está nesta categoria.")


def barra(porcentagem):
    """Barra em texto: cada # vale 5%. No modo acessível, não há barra (só números)."""
    if CONFIG["acessivel"]:
        return ""
    quantidade = int(porcentagem / 5)
    return colorir("#" * quantidade, "azul")


def tela_painel(sistema):
    """Opção 10: mostra cada indicador com os dados de origem, a fórmula e o resultado, e no fim a conclusão."""
    titulo("Painel de indicadores")
    ocorrencias = sistema["ocorrencias"]
    total = len(ocorrencias)
    if total == 0:
        print("Não há ocorrências para calcular indicadores.")
        pausar()
        return

    print(f"Dados de origem: {total} ocorrências válidas de {BAIRRO} (hoje = dia {DIA_HOJE}).")
    print(f"Registros inconsistentes ({len(sistema['inconsistentes'])}) ficam fora dos números.\n")

    # I1 e I2
    print("[I1/I2] Ocorrências por categoria")
    print("Fórmula: proporção = total da categoria ÷ total geral × 100")
    contagem = indicadores.contar_por_categoria(ocorrencias)
    for categoria in CATEGORIAS:
        pct = indicadores.proporcao(contagem[categoria], total)
        print(f"  {NOMES_CATEGORIAS[categoria].ljust(15)} {str(contagem[categoria]).rjust(3)}  "
              f"{indicadores.formatar_numero(pct).rjust(6)}%  {barra(pct)}")

    # I3
    print("\n[I3] Ocorrências por status")
    contagem = indicadores.contar_por_status(ocorrencias)
    for status in STATUS:
        pct = indicadores.proporcao(contagem[status], total)
        print(f"  {NOMES_STATUS[status].ljust(15)} {str(contagem[status]).rjust(3)}  "
              f"{indicadores.formatar_numero(pct).rjust(6)}%  {barra(pct)}")

    # I4
    print("\n[I4] Matriz categoria × status (cada célula = quantidade)")
    cabecalho = "  " + "".ljust(15)
    for status in STATUS:
        cabecalho = cabecalho + NOMES_STATUS[status].rjust(12)
    print(cabecalho + "Total".rjust(8))
    matriz = sistema["matriz"]
    for linha in range(len(CATEGORIAS)):
        texto = "  " + NOMES_CATEGORIAS[CATEGORIAS[linha]].ljust(15)
        total_linha = 0
        for coluna in range(len(STATUS)):
            texto = texto + str(matriz[linha][coluna]).rjust(12)
            total_linha = total_linha + matriz[linha][coluna]
        print(texto + str(total_linha).rjust(8))

    # I5
    pendentes = indicadores.contar_pendencias(ocorrencias)
    print(f"\n[I5] Pendências = abertas + em análise = {pendentes} de {total} "
          f"({indicadores.formatar_numero(indicadores.proporcao(pendentes, total))}%)")

    # I6
    tempo = indicadores.tempo_ate_conclusao(sistema)
    print("\n[I6] Tempo médio até a conclusão")
    print("Fórmula: soma de (dia da conclusão − dia de abertura) ÷ número de concluídas")
    for item in tempo["detalhes"]:
        print(f"  {item['id']}: aberta no dia {item['abertura']}, concluída no dia {item['conclusao']} "
              f"-> {item['dias']} dias")
    if tempo["quantidade"] > 0:
        print(f"  Resultado: {tempo['soma']} ÷ {tempo['quantidade']} = "
              f"{indicadores.formatar_numero(tempo['media'])} dias")
    else:
        print("  Nenhuma ocorrência concluída com data no histórico.")
    if len(tempo["sem_registro"]) > 0:
        print("  Fora da média (concluídas sem data no histórico): " + ", ".join(tempo["sem_registro"]))

    # I7
    print(f"\n[I7] Dias em aberto das pendentes, por categoria")
    print(f"Fórmula: soma de ({DIA_HOJE} − dia de abertura) ÷ número de pendentes da categoria")
    dias = indicadores.dias_em_aberto_por_categoria(sistema)
    for categoria in CATEGORIAS:
        item = dias[categoria]
        print(f"  {NOMES_CATEGORIAS[categoria].ljust(15)} {item['soma']} ÷ {item['quantidade']} = "
              f"{indicadores.formatar_numero(item['media'])} dias")

    # Score de prioridade
    print("\n[Extra] As 5 pendências mais urgentes")
    print("Score = dias em aberto × peso (acessibilidade 3, iluminação 2, conservação 2, limpeza 1)")
    posicao = 1
    for item in indicadores.ranking_prioridade(sistema)[:5]:
        print(f"  {posicao}º {item['id']} {NOMES_CATEGORIAS[item['categoria']].ljust(15)} "
              f"{item['local'].ljust(18)} {item['dias']} × {item['peso']} = {item['score']}")
        posicao = posicao + 1

    # Conclusão
    print("\nConclusão:")
    for frase in indicadores.gerar_conclusao(sistema):
        print("  " + frase)
    pausar()


def tela_inconsistencias(sistema):
    """Opção 11: lista os registros separados na carga e deixa escolher um para corrigir (decisão D8)."""
    titulo("Registros inconsistentes")
    while True:
        lista = sistema["inconsistentes"]
        if len(lista) == 0:
            print("Nenhum registro inconsistente.")
            pausar()
            return
        print("Estes registros foram separados na carga e não entram nos números:")
        for i in range(len(lista)):
            reg = lista[i]["registro"]
            print(f"  {i + 1}. {descrever_inconsistencia(lista[i])}")
            print(f"     dados: categoria='{reg['categoria']}', descrição='{reg['descricao']}', "
                  f"local='{reg['local']}', dia='{reg['dia']}', status='{reg['status']}'")
        opcao = ler_texto("\nNúmero do registro para corrigir (0 para voltar): ")
        if opcao == "0":
            return
        elif opcao.isdigit() and 1 <= int(opcao) <= len(lista):
            corrigir(sistema, int(opcao) - 1)
        else:
            mensagem_erro(f"Digite um número de 0 a {len(lista)}.")


def corrigir(sistema, indice):
    """Pede de novo só os campos com problema e valida outra vez."""
    item = sistema["inconsistentes"][indice]
    registro = dict(item["registro"])          # cópia: o original só muda se a correção for aceita
    campos = campos_com_problema(item["problemas"])
    print(f"\nCorrigindo o registro {registro['id']}. Campos com problema: {', '.join(campos)}")

    if "id" in campos:
        registro["id"] = operacoes.proximo_codigo(sistema)
        print(f"Novo código gerado: {registro['id']}")
    if "descricao" in campos:
        registro["descricao"] = ler_descricao()
    if "categoria" in campos:
        categoria = ""
        sugestao = sugerir_categoria(registro["descricao"])
        if sugestao != "":
            print(f"Pela descrição, parece ser da categoria {NOMES_CATEGORIAS[sugestao]}.")
            if ler_sim_nao("Usar essa categoria?"):
                categoria = sugestao
        if categoria == "":
            categoria = CATEGORIAS[escolher_da_lista("Escolha a categoria", nomes_das_categorias(), False)]
        registro["categoria"] = categoria
    if "local" in campos:
        registro["local"] = LOCAIS[escolher_da_lista("Escolha o local", LOCAIS, False)]
    if "dia" in campos:
        registro["dia"] = ler_dia("Dia de abertura (1 a 30): ")
    if "status" in campos:
        print(f"O status '{registro['status']}' não existe. Escolha um dos padronizados:")
        registro["status"] = STATUS[escolher_da_lista("Escolha o status", nomes_dos_status(), False)]

    if not confirmar_se_acessivel("Confirmar a correção?"):
        print("Correção cancelada.")
        return
    resultado = operacoes.corrigir_inconsistente(sistema, indice, registro)
    if resultado[0]:
        mensagem_ok(resultado[1])
        salvar_automaticamente(sistema)
    else:
        mensagem_erro("Ainda há problemas: " + mensagens_dos_problemas(resultado[1]))


def tela_salvar(sistema):
    """Opção 0: confirma o estado salvo em data/saida/ e mostra as mudanças desta execução."""
    titulo("Salvar e voltar ao início")
    caminhos = dados.salvar_sessao(sistema)
    print(f"Nesta sessão: {sistema['cadastros']} cadastro(s) e {sistema['mudancas']} mudança(s) de status.")
    print("Estado salvo em:")
    for caminho in caminhos:
        print("  " + caminho)
    print("Os arquivos originais em data/ não foram alterados.")
    print("Na próxima execução, será possível continuar esta sessão.")


# ---------------------------------------------------------------
# Menu do terminal (caminho 1)
# ---------------------------------------------------------------

def menu_terminal(sistema):
    """Caminho 1: mostra o menu principal e chama a tela escolhida, até a pessoa escolher 0.

    O if/elif compara a opção digitada com cada número. Qualquer outra coisa cai
    no else e mostra "Opção inválida": o programa nunca fecha por erro de digitação."""
    while True:
        titulo("Menu principal")
        modo = "ligado" if CONFIG["acessivel"] else "desligado"
        print(f"Fila de triagem: {len(sistema['fila'])} · Pendências: "
              f"{indicadores.contar_pendencias(sistema['ocorrencias'])} · Modo acessível: {modo}\n")
        for opcao in OPCOES_MENU:
            print(opcao)
        opcao = ler_texto("\nEscolha uma opção: ")
        if opcao == "1":
            tela_listar(sistema)
        elif opcao == "2":
            tela_buscar(sistema)
        elif opcao == "3":
            tela_filtrar(sistema)
        elif opcao == "4":
            tela_cadastrar(sistema)
        elif opcao == "5":
            tela_triagem(sistema)
        elif opcao == "6":
            tela_atualizar(sistema)
        elif opcao == "7":
            tela_desfazer(sistema)
        elif opcao == "8":
            tela_historico(sistema)
        elif opcao == "9":
            tela_explorar(sistema)
        elif opcao == "10":
            tela_painel(sistema)
        elif opcao == "11":
            tela_inconsistencias(sistema)
        elif opcao == "12":
            CONFIG["acessivel"] = not CONFIG["acessivel"]
            print("Modo acessível " + ("ligado." if CONFIG["acessivel"] else "desligado."))
        elif opcao == "0":
            tela_salvar(sistema)
            return
        else:
            mensagem_erro("Opção inválida, digite um número de 0 a 12.")
