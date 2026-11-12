# Checklist do edital — Neighborhood Action Dashboard

Legenda: ✅ implementado com evidência no código · 🟡 em revisão, aguardando confirmação ou teste final · ⬜ pendente.
Coluna **Evidência**: arquivo, função ou teste que comprova o item.

> Situação em 12/11/2026, branch `aline/atualização`: revisão de integração do formulário, persistência e documentação. A execução de toda a suíte atualizada deve ser confirmada pela equipe antes da entrega. A `main` não recebe estas mudanças.

## Dados simulados
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| D1 | No mínimo 12 ocorrências com código único | ✅ | `data/ocorrencias.csv` (18 registros, 16 válidos); `teste_carga` |
| D2 | Categorias: iluminação, acessibilidade, limpeza e conservação de espaços coletivos | ✅ | 5 / 4 / 3 / 4; `teste_indicadores` |
| D3 | Cada ocorrência com categoria, descrição, localidade genérica, data simulada e status | ✅ | `docs/dados.md` (campos) |
| D4 | No mínimo 3 status, com o significado documentado | ✅ | `validacao.SIGNIFICADO_STATUS`; `docs/dados.md` |
| D5 | Histórico com pelo menos 8 atualizações ou eventos | ✅ | `data/historico.csv` (16 eventos) |
| D6 | Pelo menos 1 registro com campo ausente ou inconsistente, detectado e tratado | ✅ | 017 (sem categoria) e 018 (status `resolvido`); `validar_registro`; opção 11; `teste_correcao` |
| D7 | Sem informações pessoais (dados inventados) | ✅ | Só locais genéricos; o cadastro não pede nome nem endereço |

## Cadastro e interpretação
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| C1 | Ler ocorrências de CSV/TXT (formato explicado na documentação) | ✅ | `dados.ler_registros`; `docs/dados.md` |
| C2 | Campos obrigatórios definidos | ✅ | `docs/dados.md`; `validar_registro` |
| C3 | Identificadores e valores padronizados para categoria e status | ✅ | `validacao.CATEGORIAS`, `STATUS`, `LOCAIS` |
| C4 | Listagem legível: código, categoria, localidade e status | ✅ | Opção 1 (`interface.mostrar_tabela`) |
| C5 | Pelo menos uma validação lógica (sem categoria, status desconhecido…) | ✅ | `validar_registro` (6 regras); `verificar_transicao`; `teste_validacao` |

## Organização dos dados (com justificativa)
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| E1 | Lista: conjunto de ocorrências percorrível | ✅ | `sistema["ocorrencias"]` (`estruturas.py`) |
| E2 | Fila: demandas não examinadas, por ordem de registro | ✅ | `sistema["fila"]`; opção 5; `teste_triagem` |
| E3 | Pilha: últimas atualizações e eventos recentes | ✅ | `sistema["pilha"]`; opções 7 e 8; `teste_status_e_desfazer` |
| E4 | Dicionário: acesso pelo identificador | ✅ | `sistema["por_id"]`; `operacoes.buscar` |
| E5 | Hierarquia (bairro → categoria → ocorrências), explicada | ✅ | `sistema["hierarquia"]`; opção 9; README seção 3 |
| E6 | Matriz: quantidades por categoria × situação | ✅ | `sistema["matriz"]`; painel I4; `teste_estruturas` |

## Regras lógicas
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| R1 | `if` / `elif` / `else` em entradas, categorias e mudanças de status | ✅ | `validar_registro`, `verificar_transicao`, `menu_terminal` |
| R2 | `and`, `or` e `not` em pelo menos 3 condições distintas | ✅ | L1 (`or`), L2 (`not`/`or`), L3 (`or`/`and`), L5 (`and`/`not`), L6 (`not`) |
| R3 | Uma expressão booleana documentada no README | ✅ | README seção 4: L3 (`operacoes.filtrar`) com tabela-verdade |
| R4 | Explicação de por que cada condição gera cada mensagem/ação | ✅ | README seção 4 (tabela de regras) e comentários no código |

## Consultas, filtros e atualização
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| Q1 | Cadastrar com verificação dos campos obrigatórios | ✅ | Opção 4; `operacoes.cadastrar`; `teste_cadastro` |
| Q2 | Buscar por código | ✅ | Opção 2 ("14" vira "014") |
| Q3 | Filtrar por categoria e/ou status | ✅ | Opção 3; `teste_consultas` |
| Q4 | Atualizar status e registrar no histórico | ✅ | Opção 6; `teste_status_e_desfazer` |
| Q5 | Mensagem clara para registro inexistente ou dado inválido | ✅ | "Ocorrência 999 não encontrada.", "Transição não permitida…" |

## Indicadores
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| I1 | Totais e proporções por categoria | ✅ | Opção 10 [I1/I2] |
| I2 | Totais e proporções por status | ✅ | Opção 10 [I3] |
| I3 | Indicador extra (tempo médio simulado ou pendências) | ✅ | Pendências, tempo médio (5,33 dias), dias em aberto e score |
| I4 | Dados de origem, fórmula e resultado em tabela/painel textual | ✅ | Opção 10 mostra os três para cada indicador |
| I5 | Conclusão curta interpretando os números | ✅ | `indicadores.gerar_conclusao` (frases por regra) |

## Regras técnicas
| # | Requisito | Situação | Evidência |
|---|---|---|---|
| T1 | Só conceitos das Fases 1, 2 e 3 | 🟡 | Sem `try/except`, sem classes. Equipe deve revisar |
| T2 | Sem pandas, numpy, sklearn, streamlit, web, banco de dados ou APIs | ✅ | Único `import` externo aos módulos: `os` |
| T3 | Sem bibliotecas externas | ✅ | Sistema: `os`; testes isolados: `tempfile`, ambos da biblioteca padrão |
| T4 | Executa com `python src/sistema.py` | 🟡 | Versão anterior testada com Python 3.14; reexecutar após alterações de persistência |

## README (estrutura obrigatória)
| # | Seção | Situação |
|---|---|---|
| M1 | Nome da equipe e RMs | 🟡 |
| M2 | Bairro, problema e público beneficiado | ✅ |
| M3 | Estruturas de dados e justificativas | ✅ |
| M4 | Regras lógicas principais | ✅ |
| M5 | Indicadores, fórmulas e interpretação | ✅ |
| M6 | Como executar | ✅ |
| M7 | Exemplo de cadastro, consulta, alteração e saída | ✅ |
| M8 | Acessibilidade, inclusão e privacidade | ✅ |
| M9 | Link do vídeo | ⬜ |
| M10 | Conclusões, limitações e aprendizados | 🟡 (texto-base de aprendizados inserido; equipe deve revisar e aprovar) |

## Entrega
| # | Item | Situação |
|---|---|---|
| F1 | Repositório GitHub público, no modelo da coordenação | 🟡 (criado privado; tornar público antes da entrega) |
| F2 | Vídeo no YouTube como "Não listado" | ⬜ |
| F3 | TXT na FIAP ON com só os dois links | ⬜ |
| F4 | Uso de IA documentado em `docs/uso_ia.md` | ✅ (registrar futuras alterações também) |
| F5 | Código sem erros nas operações demonstradas | 🟡 (11 testes escritos; execução final e ensaio do vídeo pendentes) |

## Revisão adicional da branch `aline/atualização`

| Item | Situação | Evidência |
|---|---|---|
| Formulário visual alinhado às regras do Python | ✅ | `painel/formulario.html`: categoria, descrição ≤120, local genérico e dia 1–30; sem envio de dados |
| RMs corrigidos na página Sobre | ✅ | `painel/sobre.html` |
| Continuidade entre execuções | 🟡 | `dados.py`, `sistema.py`, `interface.py`; autosalvamento e retomada implementados, aguardando execução final |
| Teste de persistência isolado | 🟡 | `src/testes.py`: grava/recupera com `tempfile` sem alterar dados do usuário; executar para validar |
| Revisão visual do painel HTML | ⬜ | A alinhar com a equipe; CSS e estrutura visual mantidos nesta etapa |
| Informações oficiais ainda faltantes | ⬜ | Nome oficial do grupo, tutor(a) e link do vídeo não listado |
| Publicação para correção | ⬜ | Manter privado até autorização da equipe; publicar e conferir link público antes da entrega |
