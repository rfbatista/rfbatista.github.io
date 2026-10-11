+++
title = "Dica rápida: buscar e substituir em vários arquivos no Neovim"
date = "2023-12-03"
tags = ["neovim"]
categories = ["post"]
draft = false
+++

Renomear alguma coisa no projeto inteiro é uma daquelas tarefas que fazem muita gente abrir o VS Code "só para isso". Não precisa. Com o Telescope para buscar e a quickfix list para aplicar a mudança, o Neovim resolve em quatro passos.

## Passo 1: buscar com o Telescope

Rode `:Telescope live_grep` e digite a palavra ou o padrão que você quer substituir.

![](./1.png)

## Passo 2: mandar os resultados para a quickfix list

Com os resultados na tela, aperte `Ctrl + q`. O Telescope manda todas as ocorrências para a quickfix list.

![](./2.png)

## Passo 3: substituir

Agora rode a substituição em cada item da lista:

```vim
:cdo s/busca/troca/g
```

O `:cdo` executa o comando seguinte em cada item da quickfix list, então o `s/busca/troca/g` só é aplicado nas linhas que o Telescope encontrou. Coloque um `c` no final (`s/busca/troca/gc`) se quiser confirmar cada troca.

![](./3.png)

## Passo 4: salvar tudo

As mudanças ainda estão só nos buffers. Para gravar de uma vez todos os arquivos alterados:

```vim
:cdo update
```

O `update` só grava o buffer se ele foi modificado, então arquivos que não mudaram ficam como estão. Um `:wa` também resolve, se você preferir salvar todos os buffers abertos.

# Referências

- [Quickfix](https://neovim.io/doc/user/quickfix.html)
- [Telescope](https://github.com/nvim-telescope/telescope.nvim)
