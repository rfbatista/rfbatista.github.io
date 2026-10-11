+++
title = "O Princípio da Pirâmide"
date = "2023-10-02"
tags = ["Strategy", "comunicação"]
categories = ["post"]
draft = true
+++

Engenheiro costuma escrever do jeito que pensou: primeiro o contexto, depois a investigação, depois os detalhes e, lá no último parágrafo, a conclusão. Faz sentido para quem escreveu, porque foi essa a ordem em que as coisas aconteceram. Para quem lê, é cansativo. A pessoa precisa atravessar o texto inteiro para descobrir o que você quer dela.

O Princípio da Pirâmide, criado pela Barbara Minto quando ela trabalhava na McKinsey, inverte essa ordem. Comece pela resposta e depois sustente com os argumentos.

## A estrutura

Imagine uma pirâmide. No topo fica a ideia principal, a única coisa que o leitor precisa levar se parar de ler ali. Logo abaixo vêm de três a cinco argumentos que sustentam essa ideia. E abaixo de cada argumento ficam os dados, exemplos e detalhes que o sustentam.

Duas regras mantêm a pirâmide de pé:

- **Vertical**: cada nível responde à pergunta que o nível de cima provoca. Se o topo diz "devemos migrar para Postgres", a pergunta natural é "por quê?", e o nível de baixo responde.
- **Horizontal**: as ideias de um mesmo nível devem ser do mesmo tipo e, juntas, cobrir o assunto sem se repetir. É o famoso MECE (*mutually exclusive, collectively exhaustive*).

## Como ordenar os argumentos

Os argumentos de um mesmo nível precisam de uma ordem, e o livro sugere três:

1. **Ordem temporal**: se existe uma sequência de eventos com relação de causa e efeito, apresente as ideias na ordem em que acontecem. Bom para postmortems e planos de execução.
2. **Ordem estrutural**: quebre uma ideia nas suas partes, garantindo que todas as ideias de suporte importantes estejam cobertas. Bom para descrever um sistema por componentes ou um problema por área.
3. **Ordem de grau**: apresente os argumentos por importância, do mais importante para o menos importante. Bom quando você está convencendo alguém e pode perder a atenção dele no meio do caminho.

Se você não consegue dizer qual dessas ordens está usando, provavelmente os argumentos ainda não estão claros na sua cabeça.

## Um exemplo

O jeito que eu escreveria sem pensar:

> Na última sprint investigamos a lentidão no relatório mensal. Olhamos os logs e vimos que as queries estavam demorando. Testamos alguns índices, mas não resolveu muito. Depois percebemos que o MongoDB não lida bem com os joins que o relatório faz. Fizemos um protótipo em Postgres e ficou bem mais rápido. Então achamos que vale a pena migrar.

Com a pirâmide:

> Proponho migrar o módulo de relatórios para Postgres. O relatório mensal ficou bem mais rápido no protótipo, os índices que testamos no MongoDB não resolveram, e a migração fica restrita a um módulo, então o risco é baixo. Os detalhes de cada ponto estão abaixo.

A informação é a mesma. A diferença é que no segundo texto o leitor sabe nas duas primeiras linhas o que você quer e pode decidir quanto detalhe precisa ler.

## SCQA para a introdução

Para abrir um documento maior, a Minto sugere a sequência SCQA:

- **Situação**: o contexto que o leitor já conhece e com o qual concorda.
- **Complicação**: o que mudou ou o que está dando errado.
- **Questão**: a pergunta que a complicação levanta.
- **Resposta**: o topo da pirâmide.

No exemplo acima: "o relatório mensal é usado pelo financeiro todo começo de mês (situação); desde o último trimestre ele está lento demais (complicação); o que fazemos? (questão); migrar o módulo para Postgres (resposta)."

## Onde eu uso

Dá para aplicar isso em quase tudo que a gente escreve no trabalho: descrição de PR, documento de design, mensagem para o gestor e até resposta longa no Slack. O teste que eu gosto é simples. Se a pessoa ler só a primeira frase, ela sabe o que eu preciso dela? Se não souber, vale reescrever.

# Referências

- [The Pyramid Principle - Lessons from McKinsey](https://medium.com/lessons-from-mckinsey/the-pyramid-principle-f0885dd3c5c7)
- Barbara Minto, *The Pyramid Principle: Logic in Writing and Thinking*
