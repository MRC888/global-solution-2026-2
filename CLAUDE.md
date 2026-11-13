# Global Solution 2026.2 — Neighborhood Action Dashboard (CitizenTech)

Regras gerais: [[Regras do Claude — todos os projetos]] (Obsidian). Contexto do curso: `FIAP — Como funciona o curso`. Nota do projeto: `Projetos/FIAP/FIAP — Global Solution 2026.2.md`.

## Objetivo
Protótipo em Python, no terminal, para cadastrar e acompanhar ocorrências comunitárias de um bairro fictício. O sistema usa lista, fila, pilha, dicionário, hierarquia e matriz e calcula indicadores simples.

## Estrutura (modelo oficial da coordenação)
Este repositório é o **portfólio** no formato de `equipe1ccon/FIAP-PORTFOLIO-1CCON`. O projeto fica em `1CC/GLOBAL-SOLUTION-2/`:
- `data/` CSVs de ocorrências e histórico;
- `docs/` `checklist.md` (requisito → evidência) e `uso_ia.md`;
- `src/` código; execução com `python src/sistema.py` a partir da pasta da GS;
- `painel/` painel HTML de demonstração (bônus), com os dados originais. O caminho 2 grava o painel da sessão em `data/saida/painel/` (ignorado pelo Git).

## Regras que não podem ser violadas
- Só conceitos das Fases 1 a 3. Módulos e `import` entre arquivos **foram ensinados** (Fase 3, Cap 3). `try/except` **não foi**: validar entradas com `if` (por exemplo, `.isdigit()`).
- Só a biblioteca padrão. Fora `csv` e `os`, qualquer biblioteca precisa da aprovação do Marcelo. Nada de pandas, numpy, sklearn, streamlit, web, banco de dados ou APIs.
- Código e comentários em português, em estilo iniciante a intermediário, sem truques que a equipe não saiba explicar.
- Dados inventados, sem informações pessoais.
- Atualizar `docs/checklist.md` e `docs/uso_ia.md` a cada bloco.

### Exceções autorizadas para o painel complementar
Autorizadas pelo líder Marcelo (confirmado por ele em 13/11/2026):
- `base64` (biblioteca padrão) está liberado **somente** para incorporar a logo FIAP aos arquivos HTML gerados. `pathlib` também foi liberado, mas o código atual não precisa dele.
- `tempfile` (biblioteca padrão) está liberado **somente** em testes de persistência com diretórios temporários isolados, sem alterar os CSVs originais.
- JavaScript **local** está liberado para o mapa interativo bônus (pinos, ficha, filtros, arraste e botões de zoom), sem requisições de rede, APIs, servidor ou dependências externas. Os dados e indicadores continuam sendo processados em Python.
- Essas exceções não autorizam outras bibliotecas ou integrações sem nova aprovação. O código deve continuar compreensível e explicável pela equipe.

## Equipe
| Pessoa | Papel |
|---|---|
| Marcelo Santos (RM 576131), líder | Arquitetura, estruturas, integração, README |
| Douglas Goltz (RM 574439) | Código do sistema, validações, regras, indicadores e painel HTML |
| Alice Brenda (RM 574916) | Visual, modo acessível e vídeo |

## Repositório
[MRC888/global-solution-2026-2](https://github.com/MRC888/global-solution-2026-2), **público desde 13/11/2026**, branch `main`, remote `origin`. O rascunho do Claude (`gs2026-claude`) foi descartado: a branch e o remote locais foram apagados em 13/11; o repositório no GitHub só falta excluir (precisa do `gh auth refresh -h github.com -s delete_repo` do Marcelo). Nada dele faltava na `main`: os dados de lá eram versões antigas.

## ⏰ LEMBRETE DA ENTREGA (pedido do Marcelo, 13/11/2026)
Quando o Marcelo for entregar, **lembrar** que:
1. ele vai pedir uma **revisão final** completa antes (rodar testes, sistema, painel no navegador, conferir README, links e repositório público);
2. o vídeo (Alice) precisa estar no YouTube como **"Não listado"**, com o link na seção 9 do README;
3. a entrega na FIAP ON é **um `.TXT` com os dois links**: repositório GitHub público e vídeo.

## Estado e próximas tarefas (13/11/2026)
- [x] Sistema completo, mapa da Alice, correções da auditoria, 14 testes e CI, tudo na `main`.
- [x] README: equipe Mugiwaras, sem tutor, aprendizados de cada um (escritos pelo Claude a partir do que cada um fez; a equipe revisa).
- [x] Repositório público; rascunho apagado (falta só excluir o `gs2026-claude` no GitHub).
- [ ] Vídeo (Alice) e link na seção 9 do README.
- [ ] Revisão final a pedido do Marcelo.
- [ ] `.TXT` com os dois links e entrega.
