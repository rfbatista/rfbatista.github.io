+++
title = "Joias escondidas do Git"
date = "2023-10-02"
tags = ["git", "tricks"]
categories = ["post"]
draft = true
+++

Este post nasceu de uma palestra com o mesmo nome, "Git Hidden Gems", do Enrico Campidoglio na DevFest de Copenhague de 2023. O link está nas referências e vale muito a pena assistir.

O Git tem uma porção de comandos que a gente não usa no dia a dia. Tem gente que prefere ficar numa interface gráfica, e tudo bem, ela resolve a maioria dos casos. O problema é que você fica limitado ao que outro programador decidiu colocar como botão. Na minha opinião, estudar a fundo uma ferramenta que a gente usa todo santo dia se paga rápido.

Não vou repetir a palestra item a item. Separei os recursos que acho mais úteis e que pouca gente conhece.

## git add -p: commitando só parte do arquivo

Você mexeu em três coisas no mesmo arquivo e quer separar em dois commits. O `-p` (de *patch*) mostra cada trecho alterado e pergunta o que fazer com ele:

```sh
git add -p
```

`y` adiciona o trecho, `n` pula, `s` quebra em pedaços menores e `e` deixa você editar na mão. Com o hábito, os commits ficam bem mais limpos e fáceis de revisar.

## git commit --fixup e rebase --autosquash

Abriu o PR, alguém pediu uma correção num commit de três commits atrás. Em vez de criar um commit "fix review", marque a correção como fixup do commit original:

```sh
git commit --fixup <hash-do-commit>
git rebase -i --autosquash main
```

O rebase já abre com o commit de correção posicionado logo abaixo do original e marcado para ser fundido. É só salvar e fechar.

## git log -S: quem apagou essa função?

O famoso *pickaxe*. Ele procura commits que mudaram a quantidade de ocorrências de um texto, ou seja, commits que adicionaram ou removeram aquilo:

```sh
git log -S "calculaFrete" --oneline
```

Já o `-L` mostra a história de um trecho específico de um arquivo, commit por commit:

```sh
git log -L 10,30:src/frete.go
git log -L :calculaFrete:src/frete.go
```

A segunda forma usa o nome da função em vez de números de linha, o que é bem mais prático.

## git bisect: busca binária por bugs

Ontem funcionava, hoje não, e no meio tem cinquenta commits. O `bisect` faz uma busca binária e encontra o culpado em uns seis passos:

```sh
git bisect start
git bisect bad            # o commit atual está quebrado
git bisect good v1.4.0    # essa versão funcionava
```

O Git faz checkout de um commit no meio do caminho, você testa e responde `git bisect good` ou `git bisect bad`. Se você tiver um script que retorna 0 quando está tudo certo, dá para automatizar tudo:

```sh
git bisect run make test
git bisect reset
```

## git worktree: duas branches abertas ao mesmo tempo

Está no meio de uma feature e precisa corrigir algo urgente na `main`? Em vez de `git stash` e trocar de branch, crie outra pasta de trabalho apontando para o mesmo repositório:

```sh
git worktree add ../hotfix main
cd ../hotfix
```

Cada worktree tem seus próprios arquivos, mas compartilha o histórico. Quando terminar, `git worktree remove ../hotfix`.

## git reflog: o desfazer do Git

Fez um `reset --hard` errado ou apagou uma branch sem querer? O reflog guarda por onde o seu `HEAD` passou, inclusive commits que não estão mais em branch nenhuma:

```sh
git reflog
git reset --hard HEAD@{2}
```

Quase nada no Git se perde de verdade, desde que tenha sido commitado em algum momento.

## git rerere: resolvendo o mesmo conflito uma vez só

Se você faz rebase com frequência, provavelmente já resolveu o mesmo conflito várias vezes. O `rerere` (*reuse recorded resolution*) grava como você resolveu e aplica de novo sozinho na próxima vez:

```sh
git config --global rerere.enabled true
```

É só ligar e esquecer.

# Referências

[Git Hidden Gems - Enrico Campidoglio](https://www.youtube.com/watch?v=uFrPgUjv_Y8&ab_channel=NDCConferences)
