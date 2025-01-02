+++
title = "Arvores de expressão em C++"
date = "2024-03-19"
tags = ["c++"]
draft = false
+++

# Arvores de expresão em C++

Os compiladores utilizam uma lista de categorias para determinar as regras à serem seguidas ao realizar operações 
em objetos temporários.

![](./value_categories.png)

Um lvalue (locator value) representa um objeto que ocupa uma posição identificavel na memória, por exclusão 
um rvalue é um objeto que não ocupa uma posição identificavel em memória


## gvalue (generalized value)

Determina a identidade de um objeto, tudo que podemos contruir uma referencia.

## prvalue (pure rvalue)

Inicializa um objeto ou um campo de bits ou calcula o valor do operando de um operador, conforme especificado pelo contexto no qual ele aparece.

## xvalue (expiring value)
