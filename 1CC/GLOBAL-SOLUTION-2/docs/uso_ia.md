# Uso de IA no projeto

O edital permite usar IA, desde que a equipe registre **como ela ajudou** e **como os resultados foram verificados**. Todo o código precisa ser entendido, testado e justificado pela equipe.

**Ferramenta:** Claude (Anthropic), via Claude Code.

## Registro

| Data | O que a IA fez | Como verificamos |
|---|---|---|
| 10/11/2026 | Leu o resumo do edital e as notas do curso e listou o que foi ensinado nas Fases 1 a 3 (módulos e `import` sim; `try/except` não) | Marcelo conferiu com os capítulos |
| 10/11/2026 | Abriu o repositório modelo da coordenação e montou a mesma estrutura de pastas (`1CC/GLOBAL-SOLUTION-2` com `data`, `docs`, `src`) | Comparação pasta a pasta com o modelo |
| 10/11/2026 | Criou esta checklist e o esqueleto do README com as 10 seções obrigatórias | Conferência item a item com o edital |
| 10/11/2026 | Escreveu o rascunho do algoritmo (`docs/algoritmo_v1.md`) com as decisões em aberto para a reunião da equipe | Será discutido e alterado pela equipe antes de qualquer código |
| 12/11/2026 | A pedido do Douglas, na branch `douglas` (proposta para a equipe, fora do `main`): criou os dados fictícios (`data/*.csv`) e o código em `src/` seguindo o `algoritmo_v1.md`, com a sugestão de cada decisão D1–D14. Também criou o caminho 2, que gera o painel HTML (`painel/solicitacoes.html`) | `src/testes.py`: 10 testes comparam o resultado do código com o gabarito calculado à mão (`docs/dados.md`). Duas sessões completas foram rodadas no terminal (cadastro, filtro, transição proibida, desfazer, triagem, correção de inconsistências, modo acessível), e a página gerada foi aberta no navegador. **A equipe ainda precisa revisar e aprovar** |
| 12/11/2026 | Passou a gerar também a página Início do painel (`painel/painel.html`) com os números dos dados, no lugar dos números de exemplo. Explicou todas as funções do código (docstrings) e preencheu as seções 2, 3, 4, 5, 7, 8 e 10 do README | Teste `teste_painel_html` confere que a Início mostra 16 no total, e não os 12 de exemplo. Os exemplos da seção 7 foram copiados de uma execução real. Um script conferiu que nenhuma função ficou sem explicação. Os aprendizados (seção 10) ficam para a equipe escrever |
| 12/11/2026 | A pedido do Marcelo, revisou a branch do Douglas sem alterar o código (requisitos do edital, testes de entradas inválidas e recálculo independente dos indicadores) e escreveu `docs/roteiro_video.md`; depois uniu tudo na `main` e preencheu os RMs no README | Rodou os 10 testes e sessões completas no terminal; os pontos encontrados foram passados ao Douglas para ele decidir e corrigir |
| 12/11/2026 | ChatGPT (OpenAI) revisou os requisitos e o código existente. Na branch `aline/atualização`, alinhou o formulário estático ao cadastro Python, corrigiu dados da equipe no HTML, acrescentou persistência da sessão por CSV, validação central do limite de descrição, teste isolado de persistência e revisou o README/checklist/documentação. Não alterou a `main` nem publicou o repositório. | Leitura estática do código e conferência independente das contagens e médias a partir dos CSVs originais. As alterações foram registradas na branch separada. **Os testes de Python atualizados e o ensaio completo no terminal ainda precisam ser executados e validados pela equipe antes de declarar aprovação final.** |

## Como verificamos o que a IA produz
- Rodamos o programa e testamos os casos de erro (entrada vazia, código inexistente, status inválido).
- Conferimos os cálculos dos indicadores à mão.
- Cada integrante lê e explica o trecho de código pelo qual é responsável antes de aprovar as alterações para entrega.
- Alterações propostas com ajuda de IA que ainda não passaram por execução independente são marcadas como pendentes no checklist; não são tratadas como testadas.
