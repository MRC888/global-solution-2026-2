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

## Repositórios (os dois privados)
| Repositório | Branch local | Remote | O que tem |
|---|---|---|---|
| [MRC888/global-solution-2026-2](https://github.com/MRC888/global-solution-2026-2) | `main` | `origin` | **Oficial da equipe.** Sistema completo do Douglas, dados, testes, README, painel HTML e roteiro do vídeo |
| [MRC888/gs2026-claude](https://github.com/MRC888/gs2026-claude) | `rascunho-claude` | `rascunho` | **Rascunho do Claude**, temporário: tudo o que foi adiantado, incluindo `data/*.csv` e `docs/dados.md` (dados da Vila Esperança e gabarito dos indicadores conferido por script) |

Para consultar o rascunho sem trocar de branch: `git show rascunho-claude:1CC/GLOBAL-SOLUTION-2/docs/dados.md`.

## ⏰ LEMBRETE OBRIGATÓRIO (pedido do Marcelo, 10/11/2026)
No fim do projeto, antes da entrega, **lembrar o Marcelo** de:
1. unir ao `main` o que for aproveitado do `rascunho-claude`;
2. excluir o repositório `MRC888/gs2026-claude`, a branch `rascunho-claude` e o remote `rascunho`;
3. tornar público o `global-solution-2026-2` (o edital exige repositório público).

## Estado e próximas tarefas (13/11/2026)
- [x] Sistema completo na `main` (Douglas, 12/11), revisado sem alterações; roteiro do vídeo em `docs/roteiro_video.md`.
- [ ] Douglas corrige os pontos da revisão (ver nota do Obsidian, 12/11).
- [x] README: nome da equipe (= nome do projeto, o edital só pede "nome da equipe"), sem tutor, aprendizados de cada um (escritos pelo Claude a partir do que cada um fez; a equipe revisa).
- [ ] Link do vídeo no README (seção 9).
- [ ] Gravar o vídeo (Alice, "Não listado") e montar o `.TXT` com os dois links.
- [x] Mapa interativo bônus (Alice), auditado e corrigido pelo Marcelo com o Claude em 13/11 e unido à `main`; 14 testes passando, CI a cada push.
- [ ] Conferir navegação no navegador antes da entrega (feita em 13/11; repetir depois de qualquer mudança).
- [ ] Lembrete acima: tornar público, apagar o rascunho.
