+++
title = "Geração procedural de layouts"
tags = ["algorithms", "games", "procedural-generation"]
categories = ["post"]
draft = true
+++

Neste post quero compartilhar algumas ideias de algoritmos para gerar novos layouts geométricos: plantas de casa, salas de uma dungeon, a disposição de elementos numa página. É mais um caderno de ideias do que um tutorial. Venho juntando anotações sobre isso no meu [jardim](/jardim/games/procedural-generation/) e aqui tento organizar o que aprendi até agora.

O problema parece simples. Você tem um espaço retangular e quer dividi-lo em pedaços que façam sentido. O difícil é o "que façam sentido": um gerador aleatório produz layouts válidos com facilidade, mas a maioria é feia, repetitiva ou inútil. Por isso eu penso no problema em duas partes. Uma é gerar candidatos, a outra é avaliar se um candidato é bom.

## Gerando candidatos

### Dividir o espaço: árvores BSP

A técnica mais intuitiva é a *binary space partitioning*. Você pega o retângulo inteiro, corta em dois numa posição aleatória (na horizontal ou na vertical) e repete o processo em cada metade até os pedaços ficarem do tamanho que você quer.

```
dividir(retangulo):
  se retangulo é pequeno o suficiente:
    retorna [retangulo]
  escolhe direção e posição do corte
  a, b = corta(retangulo)
  retorna dividir(a) + dividir(b)
```

O resultado é uma árvore em que cada folha é uma sala. Uma vantagem que eu acho subestimada é que a árvore guarda quem é vizinho de quem, e isso facilita criar corredores ou portas entre salas irmãs. A desvantagem é que tudo fica com cara de grade: retângulos alinhados, sem nenhuma surpresa.

### Encaixar peças: rectangle packing

A abordagem contrária é partir das peças. Você já sabe que precisa de uma sala de 4x5, dois quartos de 3x3 e um banheiro de 2x2, e quer encaixá-los num espaço. Esse é o problema de *rectangle packing*, o mesmo que aparece quando um jogo monta um atlas de texturas.

Uma heurística simples e boa é a *skyline*: você mantém o "horizonte" formado pelo topo das peças já colocadas e encaixa a próxima peça no ponto mais baixo onde ela couber. É rápida e dá resultados razoáveis. O [texto do David Colson](https://www.david-colson.com/2020/03/10/exploring-rect-packing.html) compara várias dessas heurísticas com animações e é o melhor ponto de partida que encontrei.

O problema é que packing otimiza ocupação, e ocupação não é o mesmo que um layout bom. Uma casa perfeitamente compacta pode ter o banheiro no meio da sala.

### Evoluir soluções: algoritmos genéticos

Quando "bom" é difícil de definir com uma regra, algoritmos evolutivos são uma opção interessante. Você representa um layout como um genoma (por exemplo, a lista de cortes de uma BSP ou a ordem e a rotação das peças no packing), gera uma população aleatória e, a cada geração, mantém os melhores, cruza uns com os outros e aplica pequenas mutações.

Tudo depende da *fitness function*, a função que dá nota para cada layout. E isso me leva à parte que mais me interessa.

## Avaliando candidatos

Dá para escrever regras na mão: penalizar sala sem porta, premiar cozinha perto da sala de jantar. Funciona, mas cada regra é um caso especial, e o gerador acaba aprendendo a burlar a função em vez de gerar coisas boas.

Foi aí que encontrei o artigo *Entropic-based Similarity and Complexity Measures of 2D Architectural Drawings*. A ideia que me chamou atenção é usar entropia, um conceito da teoria da informação, para medir a complexidade de um desenho e a similaridade entre dois desenhos. Um layout muito simples (uma grade perfeita) tem pouca informação. Um layout totalmente aleatório tem informação demais e parece ruído. Os layouts que achamos interessantes costumam estar no meio.

Se isso funcionar como eu imagino, dá para usar a medida de complexidade como parte da fitness, pedindo ao algoritmo layouts que não sejam nem chatos nem caóticos. E a medida de similaridade serve para outra coisa: garantir que dez layouts gerados sejam realmente diferentes entre si, e não dez variações da mesma planta.

## Para onde quero ir

O plano é juntar as peças num experimento pequeno: BSP ou skyline para gerar candidatos, um algoritmo genético para melhorar, e uma fitness que combine regras básicas de validade com alguma medida de entropia. Ainda não sei se a entropia vai ajudar de verdade ou se vai ser só mais um número difícil de calibrar. Quando tiver resultados, conto aqui.

# Referências

- Entropic-based Similarity and Complexity Measures of 2D Architectural Drawings
- [Exploring rectangle packing algorithms - David Colson](https://www.david-colson.com/2020/03/10/exploring-rect-packing.html)
- [A Skyline-Based Heuristic for the 2D Rectangular Strip Packing Problem](https://www.researchgate.net/publication/221049934_A_Skyline-Based_Heuristic_for_the_2D_Rectangular_Strip_Packing_Problem)
- [End-to-End Procedural Generation in Caves of Qud](https://www.youtube.com/watch?v=jV-DZqdKlnE)
