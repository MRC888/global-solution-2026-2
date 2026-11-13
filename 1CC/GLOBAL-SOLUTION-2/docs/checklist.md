# Evidências de atendimento ao desafio — Global Solution 2026.2

Projeto e equipe: **Neighborhood Action Dashboard**. Cenário simulado: **Vila Esperança**.

Este documento relaciona os requisitos do desafio às implementações presentes no repositório. Os indicadores correspondem à base fictícia original, antes de alterações realizadas no terminal.

## Dados e organização

| Requisito | Implementação e evidência |
|---|---|
| Ocorrências simuladas e categorizadas | `data/ocorrencias.csv`: 18 registros iniciais; 16 válidos e dois inconsistentes, códigos 017 e 018 |
| Iluminação, acessibilidade, limpeza e conservação | Categorias padronizadas em `src/validacao.py` e documentadas em `docs/dados.md` |
| Três situações com significado explícito | `aberta`, `em_analise`, `concluida`; descritas em `src/validacao.py` |
| Histórico com eventos de acompanhamento | `data/historico.csv` com 16 eventos originais |
| Dados fictícios sem identificação pessoal | Referências genéricas a locais da Vila Esperança |
| Lista de ocorrências | `sistema["ocorrencias"]`, em `src/estruturas.py` |
| Fila de triagem | `sistema["fila"]`; atendimentos por ordem de registro |
| Pilha de alterações | `sistema["pilha"]`; última atualização pode ser desfeita |
| Dicionário de consulta | `sistema["por_id"]`; busca por identificador |
| Hierarquia | `sistema["hierarquia"]`: bairro → categoria → ocorrência |
| Matriz | `sistema["matriz"]`: categoria × situação |

## Regras e operações

| Requisito | Implementação e evidência |
|---|---|
| Leitura de CSV/TXT simples | `src/dados.py`; leitura de arquivos UTF-8 separados por ponto e vírgula |
| Campos obrigatórios e validação | `validar_registro`, em `src/validacao.py`, com rejeição de códigos duplicados, valores desconhecidos, campos vazios, caracteres incompatíveis, descrição longa e dias inválidos |
| `if`, `elif`, `else` | Validação, transições de status e menu no terminal |
| `and`, `or`, `not` | Regras de filtragem, validação, detecção de possíveis duplicatas e pendências |
| Expressão booleana documentada | Filtro de categoria e status, detalhado no README |
| Cadastro e mensagens claras | `operacoes.cadastrar` e opção 4 do terminal |
| Busca e filtros | `operacoes.buscar` e `operacoes.filtrar`; opções 2 e 3 |
| Atualização e histórico | `operacoes.atualizar_status`, histórico e opção 6 |
| Correção de inconsistências | `operacoes.corrigir_inconsistente`; opção 11 |
| Continuidade local dos dados | `data/saida/` armazena versões da sessão; escolha de retomada na abertura; dados originais preservados |
| Interface textual | `src/interface.py`, incluindo modo acessível |
| Visualização HTML complementar | `src/painel_html.py` gera as páginas Início e Solicitações; `src/mapa_html.py` gera o mapa |
| Página Sobre | `painel/sobre.html`: apresentação, equipe e limites acadêmicos do protótipo |
| Formulário demonstrativo | `painel/formulario.html`: interface visual; o cadastro funcional ocorre no terminal |
| Mapa interativo (bônus) | `painel/mapa_template.html` (HTML, SVG, CSS e JavaScript local) → `painel/mapa.html`; incorporado por iframe na página Início |
| Origem dos marcadores | `src/mapa_html.py` gera pinos e contagens somente a partir de `sistema["ocorrencias"]`; registros inconsistentes não são exibidos |
| Interação do mapa | Clique/teclado nos pinos para consultar descrição, categoria, dia e situação; filtros, arraste e botões de zoom; rolagem da página preservada |
| Exceções técnicas autorizadas | `CLAUDE.md` registra a confirmação do líder para `base64`, `pathlib`, `tempfile` e JavaScript local, com escopo limitado |

## Indicadores

| Indicador | Resultado da base fictícia original |
|---|---|
| Ocorrências válidas | 16 |
| Por categoria | Iluminação 5; acessibilidade 4; limpeza 3; conservação 4 |
| Por situação | Abertas 6; em análise 4; concluídas 6 |
| Pendências | 10 de 16 = 62,50% |
| Tempo médio até a conclusão | 32 ÷ 6 = 5,33 dias simulados |
| Média de dias pendentes em acessibilidade | 24,67 dias |
| Ranking de prioridade | Calculado em `src/indicadores.py` por dias em aberto × peso de categoria |

A origem e as fórmulas dos indicadores estão em `docs/dados.md` e no README. A interpretação detalhada aparece no terminal e no painel HTML.

## Execução e verificação

A partir da pasta `1CC/GLOBAL-SOLUTION-2`:

```bash
python3 src/sistema.py
python3 src/testes.py
```

A suíte em `src/testes.py` contém 11 verificações de carga, estruturas, validação, consultas, indicadores, cadastro, status, triagem, correção, páginas HTML (incluindo mapa dinâmico e logo incorporada) e persistência isolada. As páginas de navegação são Início, Sobre, Formulário e Solicitações; o mapa usa posições ilustrativas, não endereços reais.

## Entrega

A entrega da FIAP ON consiste em um arquivo TXT com os links do repositório GitHub público e do vídeo de apresentação no YouTube como **Não listado**. O vídeo é referenciado na seção 9 do README após a publicação. O uso de inteligência artificial está documentado em `docs/uso_ia.md`.
