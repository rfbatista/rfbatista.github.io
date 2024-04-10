+++
title = "Procedural Generation"
date = "2024-02-03"
tags = ["games", "procedural generation"]
draft = false
+++

# Procedural Generation

## Evolutionay Computation

É uma categoria de algoritmos baseados na idéia de uma população baseada em individuos.
Em cada geração (iteração do algoritmos) os individuos são atualizados
Isso acontece em duas operações `mutação` e `seleção`

- mutação: age em cada individuo aplicando pequenas modificações
- seleção: age em toda população removendo o pior individuo após a aplicação de uma `fitness function`

A `fitness function` utilizada para avaliar as soluções e determinar a condição de término do algoritmo.
Esse método funciona bem em aplicações com grande numero de possiveis soluções.

### Algoritmo Genético

No algoritmo genético definimos os genomas para varios individuos de uma geração inicial de forma aleatória.
Calculamos a `fictness function` em cada individuo, selecionamos os melhores individuos e após isso aplicamos
uma `croosover function` que faz a transferencia de atributos para dos pais para os filhos de forma aleatória.

- representação genetica de uma solução 
- função para gerar novas soluções 
- fitness function 
- selection function
- crossover function: selecionando dois individuos da populaçãos seus genomas são trocados para produzir
dois novos individuos
- mutation function
- encoding scheme: a representação do genoma de um individuo

### Encoding schemas
- Floating point
- tree enconding (Koza)

## Markov Chain

## Cellular automata

## BSP Tree


## Hilbert Curves

# Referências
[6 Techniques for Leveraging AI in Content Generation](https://www.youtube.com/watch?v=priaBvs441Y)
[ End-to-End Procedural Generation in Caves of Qud ](https://www.youtube.com/watch?v=jV-DZqdKlnE)
[](https://www.politesi.polimi.it/retrieve/a81cb05d-7b46-616b-e053-1605fe0a889a/2019_12_Carideo.pdf)
