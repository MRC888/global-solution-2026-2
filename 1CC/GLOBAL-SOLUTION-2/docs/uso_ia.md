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

## Como verificamos o que a IA produz
- Rodamos o programa e testamos os casos de erro (entrada vazia, código inexistente, status inválido).
- Conferimos os cálculos dos indicadores à mão.
- Cada integrante lê e explica o trecho de código pelo qual é responsável antes de ele entrar no repositório.
