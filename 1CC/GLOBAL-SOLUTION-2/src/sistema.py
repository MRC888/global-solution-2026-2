# sistema.py
# Ponto de entrada do Neighborhood Action Dashboard.
#
# Como executar (dentro da pasta 1CC/GLOBAL-SOLUTION-2):
#     python src/sistema.py
#
# Ao abrir, o sistema lê os CSVs, valida os registros, monta as estruturas
# e oferece dois caminhos:
#     1 - Terminal: o sistema completo, com menu
#     2 - Painel HTML (bônus): gera painel/solicitacoes.html com os indicadores
# Os dois caminhos usam os mesmos dados da sessão: o que for cadastrado ou
# alterado no terminal aparece no painel gerado depois.

import dados
import estruturas
import interface
import painel_html


def carregar_sistema():
    """Lê os arquivos e monta todas as estruturas. Devolve None se faltar um arquivo."""
    registros = dados.ler_ocorrencias()
    eventos = dados.ler_historico()
    if registros is None or eventos is None:
        return None
    sistema = estruturas.criar_sistema()
    estruturas.carregar_ocorrencias(sistema, registros)
    estruturas.carregar_historico(sistema, eventos)
    return sistema


def main():
    """Abre o programa: carrega os dados, mostra o relatório da carga e oferece os dois caminhos.

    O while repete a escolha do caminho até a pessoa digitar 0. Assim dá para
    usar o terminal, depois gerar o painel com as mudanças feitas, e só então sair."""
    interface.mostrar_abertura()
    sistema = carregar_sistema()
    if sistema is None:
        print("\nNão encontrei os arquivos de dados:")
        print("  " + dados.ARQUIVO_OCORRENCIAS)
        print("  " + dados.ARQUIVO_HISTORICO)
        print("Confira se a pasta data/ está junto da pasta src/.")
        return
    interface.mostrar_relatorio_carga(sistema)

    while True:
        caminho = interface.escolher_caminho()
        if caminho == "1":
            interface.perguntar_modo_acessivel()
            interface.menu_terminal(sistema)
        elif caminho == "2":
            arquivo = painel_html.salvar_painel(sistema)
            interface.mostrar_painel_gerado(arquivo)
        else:
            print("\nAté logo! Obrigado por usar o Neighborhood Action Dashboard.")
            return


if __name__ == "__main__":
    main()
