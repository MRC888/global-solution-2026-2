# testes.py
# Testes automáticos com assert: comparam o que o sistema calcula com os
# resultados calculados à mão (gabarito em docs/dados.md).
#
# Como rodar (dentro de 1CC/GLOBAL-SOLUTION-2):  python src/testes.py
# Se algum teste falhar, o Python para e mostra qual assert não bateu.

import tempfile

import dados
import estruturas
import operacoes
import indicadores
import painel_html
from validacao import validar_registro, verificar_transicao, dia_valido, sugerir_categoria

testes_ok = 0


def passou(nome):
    """Conta mais um teste aprovado e mostra o nome dele."""
    global testes_ok
    testes_ok = testes_ok + 1
    print("  ok  " + nome)


def sistema_novo():
    """Carrega os dados originais do zero, para cada teste partir do mesmo ponto."""
    sistema = estruturas.criar_sistema()
    estruturas.carregar_ocorrencias(sistema, dados.ler_ocorrencias())
    estruturas.carregar_historico(sistema, dados.ler_historico())
    return sistema


def teste_carga():
    """A carga lê os 18 registros e separa exatamente os 2 inconsistentes, com o motivo certo."""
    s = sistema_novo()
    assert s["lidos"] == 18
    assert len(s["ocorrencias"]) == 16
    assert len(s["inconsistentes"]) == 2
    assert s["inconsistentes"][0]["registro"]["id"] == "017"
    assert s["inconsistentes"][0]["problemas"] == [["categoria", "categoria ausente"]]
    assert s["inconsistentes"][1]["registro"]["id"] == "018"
    assert s["inconsistentes"][1]["problemas"] == [["status", "status desconhecido (resolvido)"]]
    assert len(s["historico"]) == 16
    assert s["avisos_carga"] == []
    passou("carga: 18 lidos, 16 válidos, 2 inconsistentes (017 e 018), 16 eventos")


def teste_estruturas():
    """Fila, dicionário, hierarquia e matriz montados como no gabarito."""
    s = sistema_novo()
    assert s["fila"] == ["005", "010", "013", "014", "015", "016"]
    assert s["pilha"] == []
    assert s["por_id"]["014"]["local"] == "Praça Central"
    assert s["hierarquia"]["Vila Esperança"]["acessibilidade"] == ["002", "003", "005", "007"]
    # linhas: iluminação, acessibilidade, limpeza, conservação | colunas: aberta, em análise, concluída
    assert s["matriz"] == [[2, 0, 3], [1, 2, 1], [1, 1, 1], [2, 1, 1]]
    passou("estruturas: fila, dicionário, hierarquia e matriz")


def teste_validacao():
    """Cada regra de validação aceita o que é válido e recusa o que não é."""
    vazio = {}
    ok = {"id": "050", "categoria": "limpeza", "descricao": "Lixo", "local": "Praça Central",
          "dia": "10", "status": "aberta"}
    assert validar_registro(ok, vazio) == []
    longa = dict(ok)
    longa["descricao"] = "x" * 121
    assert validar_registro(longa, vazio) == [["descricao", "descrição excede 120 caracteres"]]
    sem_categoria = dict(ok)
    sem_categoria["categoria"] = ""
    assert validar_registro(sem_categoria, vazio) == [["categoria", "categoria ausente"]]
    tudo_errado = {"id": "", "categoria": "x", "descricao": "", "local": "", "dia": "abc", "status": "resolvido"}
    assert len(validar_registro(tudo_errado, vazio)) == 6      # recebe TODOS os motivos
    assert dia_valido("30") and not dia_valido("31") and not dia_valido("0") and not dia_valido("dez")
    assert verificar_transicao("aberta", "em_analise")[0]
    assert not verificar_transicao("aberta", "concluida")[0]
    assert not verificar_transicao("concluida", "aberta")[0]
    assert not verificar_transicao("aberta", "aberta")[0]
    assert not verificar_transicao("aberta", "resolvido")[0]
    assert sugerir_categoria("Restos de obra e entulho jogados na esquina") == "limpeza"
    assert sugerir_categoria("Poste apagado") == "iluminacao"
    assert sugerir_categoria("nada a ver") == ""
    passou("validação: campos, dia, transições e sugestão de categoria")


def teste_consultas():
    """Busca por código (com e sem zeros à esquerda) e filtro com as combinações da regra L3."""
    s = sistema_novo()
    assert operacoes.buscar(s, "14")["id"] == "014"
    assert operacoes.buscar(s, "999") is None
    assert operacoes.buscar(s, "017") is None                   # inconsistente não entra nas consultas
    assert len(operacoes.filtrar(s, "", "")) == 16
    assert len(operacoes.filtrar(s, "iluminacao", "")) == 5
    assert len(operacoes.filtrar(s, "", "aberta")) == 6
    assert len(operacoes.filtrar(s, "iluminacao", "aberta")) == 2
    assert len(operacoes.filtrar(s, "iluminacao", "em_analise")) == 0
    passou("consultas: busca por código e filtro (regra L3)")


def teste_indicadores():
    """Todos os indicadores batem com o gabarito calculado à mão em docs/dados.md."""
    s = sistema_novo()
    oc = s["ocorrencias"]
    assert indicadores.contar_por_categoria(oc) == {"iluminacao": 5, "acessibilidade": 4, "limpeza": 3, "conservacao": 4}
    assert indicadores.contar_por_status(oc) == {"aberta": 6, "em_analise": 4, "concluida": 6}
    assert indicadores.formatar_numero(indicadores.proporcao(5, 16)) == "31,25"
    assert indicadores.formatar_numero(indicadores.proporcao(3, 16)) == "18,75"
    assert indicadores.proporcao(1, 0) == 0.0
    assert indicadores.contar_pendencias(oc) == 10
    tempo = indicadores.tempo_ate_conclusao(s)
    assert tempo["soma"] == 32 and tempo["quantidade"] == 6
    assert indicadores.formatar_numero(tempo["media"]) == "5,33"
    dias = indicadores.dias_em_aberto_por_categoria(s)
    assert indicadores.formatar_numero(dias["acessibilidade"]["media"]) == "24,67"
    assert indicadores.formatar_numero(dias["iluminacao"]["media"]) == "8,00"
    assert indicadores.formatar_numero(dias["limpeza"]["media"]) == "13,00"
    assert indicadores.formatar_numero(dias["conservacao"]["media"]) == "10,67"
    ranking = indicadores.ranking_prioridade(s)
    assert len(ranking) == 10
    assert ranking[0]["id"] == "003" and ranking[0]["score"] == 81
    assert ranking[1]["id"] == "005" and ranking[2]["id"] == "007"
    conclusao = indicadores.gerar_conclusao(s)
    assert "Acessibilidade (24,67 dias em média)" in conclusao[2]
    assert "Entorno da UBS" in conclusao[2]
    passou("indicadores: I1 a I7, ranking e conclusão batem com o gabarito")


def teste_cadastro():
    """O cadastro gera o código, entra em todas as estruturas e recusa registro inválido."""
    s = sistema_novo()
    resultado = operacoes.cadastrar(s, "iluminacao", "Lâmpada queimada", "Praça Central", "30")
    assert resultado[0]
    nova = resultado[2]
    assert nova["id"] == "019"                 # 018 é o maior código (mesmo inconsistente)
    assert nova["status"] == "aberta"
    assert s["fila"][-1] == "019"              # entra no fim da fila
    assert s["matriz"][0] == [3, 0, 3]
    assert "019" in s["hierarquia"]["Vila Esperança"]["iluminacao"]
    falhou = operacoes.cadastrar(s, "", "Sem categoria", "Praça Central", "5")
    assert not falhou[0] and falhou[1] == [["categoria", "categoria ausente"]]
    assert len(s["ocorrencias"]) == 17         # o inválido não entrou
    dup = operacoes.possiveis_duplicadas(s, "iluminacao", "Praça Central")
    assert len(dup) == 2                       # 013 e a 019 recém-criada (L5)
    passou("cadastro: código automático, fila, matriz e recusa de inválido")


def teste_status_e_desfazer():
    """Mudança de status atualiza histórico, pilha, matriz e fila, e o desfazer volta tudo."""
    s = sistema_novo()
    r = operacoes.atualizar_status(s, "14", "em_analise", "teste")
    assert r[0]
    assert s["por_id"]["014"]["status"] == "em_analise"
    assert "014" not in s["fila"]
    assert s["matriz"][2] == [0, 2, 1]
    assert len(s["pilha"]) == 1 and len(s["historico"]) == 17
    assert not operacoes.atualizar_status(s, "14", "aberta", "")[0]       # não volta sem desfazer
    assert not operacoes.atualizar_status(s, "999", "concluida", "")[0]   # não existe
    r = operacoes.desfazer(s)
    assert r[0]
    assert s["por_id"]["014"]["status"] == "aberta"
    assert s["fila"][0] == "014"               # volta para o começo da fila
    assert s["matriz"][2] == [1, 1, 1]
    assert len(s["pilha"]) == 0
    assert len(s["historico"]) == 18           # o desfazer também fica registrado
    assert not operacoes.desfazer(s)[0]        # pilha vazia
    passou("atualização de status, pilha e desfazer")


def teste_triagem():
    """A fila atende por ordem de chegada, e quem não é examinado volta para o começo."""
    s = sistema_novo()
    assert operacoes.chamar_proximo(s) == "005"
    operacoes.devolver_para_fila(s, "005")
    assert s["fila"][0] == "005"
    codigo = operacoes.chamar_proximo(s)
    operacoes.atualizar_status(s, codigo, "em_analise", "")
    assert s["fila"] == ["010", "013", "014", "015", "016"]
    passou("triagem: fila por ordem de chegada")


def teste_correcao():
    """Um registro inconsistente corrigido sai da lista de problemas e entra no sistema."""
    s = sistema_novo()
    registro = dict(s["inconsistentes"][0]["registro"])
    registro["categoria"] = "limpeza"
    r = operacoes.corrigir_inconsistente(s, 0, registro)
    assert r[0]
    assert len(s["inconsistentes"]) == 1 and len(s["ocorrencias"]) == 17
    assert s["fila"][-1] == "017"
    passou("correção de inconsistência")


def teste_painel_html():
    """As duas páginas do painel saem com os números dos dados, sem JavaScript."""
    s = sistema_novo()
    inicio = painel_html.gerar_html_inicio(s)
    detalhes = painel_html.gerar_html_solicitacoes(s)
    for html in [inicio, detalhes]:
        assert "<!DOCTYPE html>" in html
        assert "Gerado pelo sistema em Python" in html
        assert "<script" not in html.lower()   # o painel é só HTML e CSS
    # Início: os números vêm dos dados (16 no total), e não dos 12 de exemplo
    assert '<span class="numero">16</span><span class="rotulo">Total' in inicio
    assert 'style="width: 31.25%"' in inicio   # CSS usa ponto, não vírgula
    assert "Acessibilidade (24,67 dias em média)" in inicio
    # Solicitações: lista completa e inconsistências
    assert "Pintura da faixa de pedestres apagada" in detalhes
    assert "017: categoria ausente" in detalhes
    assert painel_html.escapar("<b>&") == "&lt;b&gt;&amp;"
    passou("painel HTML: Início e Solicitações com os números dos dados")


def teste_persistencia():
    """Salva e recarrega cadastro, status e histórico, sem tocar nos CSVs originais.

    Usa uma pasta temporária isolada, que é apagada ao encerrar o teste.
    """
    with tempfile.TemporaryDirectory() as pasta:
        assert not dados.ha_sessao_salva(pasta)
        s = sistema_novo()
        assert operacoes.cadastrar(s, "iluminacao", "Poste apagado", "Praça Central", "30")[0]
        assert operacoes.atualizar_status(s, "014", "em_analise", "Equipe avisada")[0]
        caminhos = dados.salvar_sessao(s, pasta)
        assert len(caminhos) == 2
        assert dados.ha_sessao_salva(pasta)

        novo = estruturas.criar_sistema()
        estruturas.carregar_ocorrencias(novo, dados.ler_ocorrencias(True, pasta))
        estruturas.carregar_historico(novo, dados.ler_historico(True, pasta))

        assert len(novo["ocorrencias"]) == 17
        assert len(novo["inconsistentes"]) == 2
        assert novo["por_id"]["019"]["status"] == "aberta"
        assert novo["por_id"]["014"]["status"] == "em_analise"
        assert len(novo["historico"]) == 17
        assert novo["historico"][-1]["id"] == "014"
        assert novo["historico"][-1]["novo"] == "em_analise"
        assert "019" in novo["fila"] and "014" not in novo["fila"]
        assert novo["matriz"][2] == [0, 2, 1]
        assert dados.ler_ocorrencias()[13]["status"] == "aberta"
    passou("persistência: grava e retoma cadastro, status e histórico em pasta isolada")


teste_carga()
teste_estruturas()
teste_validacao()
teste_consultas()
teste_indicadores()
teste_cadastro()
teste_status_e_desfazer()
teste_triagem()
teste_correcao()
teste_painel_html()
teste_persistencia()
print(f"\n{testes_ok} testes passaram.")
