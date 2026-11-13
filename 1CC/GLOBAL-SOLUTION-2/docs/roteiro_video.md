# Roteiro do vídeo — Neighborhood Action Dashboard

**Duração:** cerca de 5 minutos. **Publicação:** YouTube, como **"Não listado"**. O link entra na seção 9 do README e no `.TXT` da entrega.

**Fio da história:** a Dona Lúcia, moradora fictícia da Vila Esperança, vê um poste apagado na Praça Central. Acompanhamos o registro dela, do cadastro até o painel de indicadores.

**Antes de gravar:**
- Rodar `python3 src/sistema.py` a partir da pasta `1CC/GLOBAL-SOLUTION-2`, com os dados originais. Assim os números batem com os deste roteiro.
- Se aparecer **"Encontrei uma sessão anterior"**, escolher `2` (recomeçar) e confirmar com `s`. Outra saída é apagar a pasta `data/saida/` antes de gravar.
- Terminal com fonte grande (pelo menos 18 pt) e janela larga. O tutor precisa conseguir ler a tela.
- Os textos entre aspas são sugestões. Falem com as próprias palavras.

---

## 1. Abertura (0:00–0:30) · Marcelo
**Tela:** README no GitHub, depois o terminal na tela inicial.

> "Somos a equipe [nome] e este é o Neighborhood Action Dashboard. É um painel comunitário que registra, organiza e acompanha problemas de um bairro fictício, a Vila Esperança: iluminação, acessibilidade, limpeza e conservação."

> "Os relatos de um bairro costumam ficar espalhados. O morador não sabe o que é mais urgente nem em que pé está a solicitação. A nossa proposta organiza isso com Python puro e as estruturas que estudamos nas três primeiras fases."

## 2. Carga e validação (0:30–1:00) · Douglas
**Tela:** a mensagem de carga logo na abertura.

> "Ao abrir, o sistema lê 18 registros do CSV. Dezesseis estão válidos e dois têm problema de propósito: o 017 está sem categoria, e o 018 tem um status que não existe, 'resolvido'. Eles ficam separados e não entram nos números."

**Ação:** escolher `1` (terminal) e `n` (modo acessível desligado, por enquanto).

## 3. Listar e buscar (1:00–1:30) · Douglas
**Ação:** opção `1` (listar) e depois opção `2`, digitando `14`.

> "A listagem percorre a **lista** de ocorrências. Na busca por código, digito só 14 e o sistema acha a 014 direto pelo **dicionário**, sem percorrer tudo."

**Ação:** opção `2`, digitando `999`.

> "Se o código não existe, a mensagem é clara."

## 4. A Dona Lúcia registra o poste (1:30–2:15) · Alice
**Ação:** opção `4`. Descrição: `Poste apagado perto do banco`. Escolher **Iluminação**, **Praça Central** e o dia `29`.

> "O cadastro confere cada campo obrigatório. Se faltar algo, ele explica o que fazer. Repare que o sistema sugere a categoria a partir das palavras da descrição, e avisa quando já existe uma ocorrência parecida no mesmo lugar."

> "A nova ocorrência ganha um código automático e entra no fim da **fila** de triagem, como uma senha de banco."

## 5. Consulta com filtro (2:15–2:45) · Alice
**Ação:** opção `3`, filtrando **Iluminação** e **Aberta**.

> "Aqui está a expressão booleana do README: a ocorrência aparece se a categoria bater **e** o status bater, e cada filtro em branco vale para todas. O registro da Dona Lúcia já aparece."

## 6. Triagem, status e desfazer (2:45–3:45) · Marcelo
**Ação:** opção `5` (triagem).

> "A triagem chama a ocorrência mais antiga da fila: quem chegou primeiro é atendido primeiro."

**Ação:** opção `6`, código `14`. Primeiro tentar **Concluída**, depois escolher **Em análise** e a observação `Equipe avisada`.

> "Uma ocorrência aberta não pode pular direto para concluída: o sistema recusa e explica. Indo para 'em análise', a mudança entra no **histórico**."

**Ação:** opção `7` (desfazer) e depois opção `8` (histórico).

> "Errei? O desfazer tira a última mudança do topo da **pilha**. O histórico não apaga nada: ele ganha um evento 'desfeito'."

## 7. O bairro em árvore (3:45–4:05) · Douglas
**Ação:** opção `9`, escolher **Acessibilidade**.

> "A **hierarquia** organiza o bairro como uma árvore: Vila Esperança, depois a categoria, depois as ocorrências. Dá para navegar por partes."

## 8. Indicadores e o que eles dizem (4:05–4:45) · Douglas
**Ação:** opção `10` (painel de indicadores).

> "Para cada indicador, o sistema mostra os dados de origem, a fórmula e o resultado. A **matriz** cruza categoria e status."

> "O que os números dizem: mais da metade das ocorrências ainda está pendente. A acessibilidade é só um quarto dos registros, mas é a que espera há mais tempo, quase 25 dias em média, e as pendências dela ficam todas no entorno da UBS, onde circulam idosos e pessoas com mobilidade reduzida. Por isso ela lidera o ranking de prioridade."

## 9. Acessibilidade e privacidade (4:45–5:05) · Alice
**Ação:** opção `12` (modo acessível) e depois opção `1`.

> "No modo acessível, as cores somem e cada ocorrência vira uma frase completa, o que ajuda quem usa leitor de tela. O sistema não pede nome, e-mail nem endereço: o local é sempre um ponto genérico do bairro."

**Opcional (bônus):** mostrar em poucos segundos o painel HTML gerado pela opção `2` da tela inicial (fica em `data/saida/painel/painel.html`).

## 10. Encerramento (5:05–5:30) · Marcelo
**Ação:** opção `0` (salvar).

> "Com estruturas simples e regras com if, transformamos relatos soltos em informação útil. Os dados são simulados e o sistema não se liga a nenhum órgão público. Ele organiza e acompanha, mas não resolve sozinho. Obrigado!"

---

## Checklist de gravação
- [ ] Todas as opções acima funcionaram no ensaio, sem mensagem de erro.
- [ ] O som está claro e a tela, legível.
- [ ] Vídeo publicado como **"Não listado"**, com o link testado numa janela anônima.
- [ ] Link colado na seção 9 do README e no `.TXT` da entrega.
