# Global Solution 2026.2 — Neighborhood Action Dashboard (CitizenTech)

Regras gerais: [[Regras do Claude — todos os projetos]] (Obsidian). Contexto do curso: `FIAP — Como funciona o curso`. Nota do projeto: `Projetos/FIAP/FIAP — Global Solution 2026.2.md`.

## Objetivo
Protótipo em Python, no terminal, para cadastrar e acompanhar ocorrências comunitárias de um bairro fictício. O sistema usa lista, fila, pilha, dicionário, hierarquia e matriz e calcula indicadores simples.

## Estrutura (modelo oficial da coordenação)
Este repositório é o **portfólio** no formato de `equipe1ccon/FIAP-PORTFOLIO-1CCON`. O projeto fica em `1CC/GLOBAL-SOLUTION-2/`:
- `data/` CSVs de ocorrências e histórico;
- `docs/` `checklist.md` (requisito → evidência) e `uso_ia.md`;
- `src/` código; execução com `python src/sistema.py` a partir da pasta da GS.

## Regras que não podem ser violadas
- Só conceitos das Fases 1 a 3. Módulos e `import` entre arquivos **foram ensinados** (Fase 3, Cap 3). `try/except` **não foi**: validar entradas com `if` (por exemplo, `.isdigit()`).
- Só a biblioteca padrão. Fora `csv` e `os`, qualquer biblioteca precisa da aprovação do Marcelo. Nada de pandas, numpy, sklearn, streamlit, web, banco de dados ou APIs.
- Código e comentários em português, em estilo iniciante a intermediário, sem truques que a equipe não saiba explicar.
- Dados inventados, sem informações pessoais.
- Atualizar `docs/checklist.md` e `docs/uso_ia.md` a cada bloco.

## Equipe
| Pessoa | Papel |
|---|---|
| Marcelo Santos (RM 576131), líder | Arquitetura, estruturas, integração, README |
| Integrante 2 (a confirmar) | Validações, regras, score, indicadores |
| Integrante 3 (a confirmar) | Interface do terminal, modo acessível, identidade do bairro, vídeo |

## Repositórios (os dois privados)
| Repositório | Branch local | Remote | O que tem |
|---|---|---|---|
| [MRC888/global-solution-2026-2](https://github.com/MRC888/global-solution-2026-2) | `main` | `origin` | **Oficial da equipe.** Só a primeira etapa: estrutura, README em branco, checklist zerada, `algoritmo_v1.md` |
| [MRC888/gs2026-claude](https://github.com/MRC888/gs2026-claude) | `rascunho-claude` | `rascunho` | **Rascunho do Claude**, temporário: tudo o que foi adiantado, incluindo `data/*.csv` e `docs/dados.md` (dados da Vila Esperança e gabarito dos indicadores conferido por script) |

Para consultar o rascunho sem trocar de branch: `git show rascunho-claude:1CC/GLOBAL-SOLUTION-2/docs/dados.md`.

## ⏰ LEMBRETE OBRIGATÓRIO (pedido do Marcelo, 10/11/2026)
No fim do projeto, antes da entrega, **lembrar o Marcelo** de:
1. unir ao `main` o que for aproveitado do `rascunho-claude`;
2. excluir o repositório `MRC888/gs2026-claude`, a branch `rascunho-claude` e o remote `rascunho`;
3. tornar público o `global-solution-2026-2` (o edital exige repositório público).

## Estado e próximas tarefas
- [x] Primeira etapa: estrutura do portfólio, checklist, uso de IA e `docs/algoritmo_v1.md` (14 decisões, D1–D14, para a reunião)
- [ ] **Código parado até a reunião fechar o algoritmo** (pedido do Marcelo, 10/11/2026). Depois da reunião: aplicar as anotações, criar a v2 e só então começar o código.
- [ ] Pendências: prazo, nome da equipe e RMs, turma (o modelo usa pastas por turma, como `1CC-AGO/1CCOR/1CCOA`; aqui foi usado `1CC/`, como no README do modelo)
- [x] Convites de colaborador (escrita) no repositório oficial enviados a `Douglasgbm` e `alicebessag` em 10/11/2026; aceitar em https://github.com/MRC888/global-solution-2026-2/invitations. O rascunho `gs2026-claude` continua só com o Marcelo.
