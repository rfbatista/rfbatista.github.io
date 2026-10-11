+++
title = "Gerenciando múltiplas contas do Git"
tags = ["git"]
categories = ["post"]
draft = true
+++

Conta pessoal e conta do trabalho no mesmo computador é uma situação bem comum, e o Git não ajuda muito. O resultado clássico é fazer push com a chave errada e tomar um `Permission denied`, ou pior, commitar no projeto da empresa com o seu e-mail pessoal. Aqui vão as formas que eu uso para manter as duas coisas separadas.

## Uma chave SSH por conta

Se você ainda não tem uma chave para cada conta, crie a segunda com um nome diferente para não sobrescrever a primeira:

```sh
ssh-keygen -t ed25519 -C "voce@empresa.com" -f ~/.ssh/id_ed25519_trabalho
```

Depois adicione o conteúdo do `.pub` nas configurações de SSH da conta correspondente no GitHub (ou GitLab, Bitbucket, tanto faz).

Para listar as chaves que já existem:

```sh
ls $HOME/.ssh
```

Vai aparecer algo assim:

```
config  id_ed25519  id_ed25519.pub  id_ed25519_trabalho  id_ed25519_trabalho.pub
```

## Opção 1: definir a chave por repositório

Dentro do repositório, escolha qual chave ele deve usar:

```sh
git config core.sshCommand "ssh -i ~/.ssh/<nome da chave> -o IdentitiesOnly=yes -F /dev/null"
```

Esse comando adiciona uma diretiva no arquivo `.git/config` do repositório, na seção `[core]`. A partir daí o Git passa a usar esse comando em todas as operações SSH daquele repositório.

O `-F /dev/null` faz o SSH ignorar o seu `~/.ssh/config`, e o `IdentitiesOnly=yes` impede que o ssh-agent ofereça outras chaves antes da que você escolheu. Sem ele, o GitHub pode aceitar a primeira chave que o agente apresentar e te autenticar com a conta errada.

O ponto fraco dessa opção é que você precisa lembrar de rodar o comando em cada repositório novo. Para clonar, use a variável de ambiente na primeira vez:

```sh
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_trabalho -o IdentitiesOnly=yes" git clone git@github.com:empresa/projeto.git
```

## Opção 2: um apelido de host no ~/.ssh/config

Outra forma é criar um host "falso" para cada conta no `~/.ssh/config`:

```
Host github.com
  HostName github.com
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes

Host github-trabalho
  HostName github.com
  IdentityFile ~/.ssh/id_ed25519_trabalho
  IdentitiesOnly yes
```

E na hora de clonar um repositório do trabalho, troque `github.com` pelo apelido:

```sh
git clone git@github-trabalho:empresa/projeto.git
```

Funciona bem, mas você precisa lembrar de trocar o host em toda URL que copiar do GitHub.

## Não esqueça do e-mail

A chave decide com qual conta você se autentica, mas o autor do commit vem do `user.email`. Dá para configurar por repositório com `git config user.email`, mas o jeito que eu prefiro é separar por pasta. Deixo tudo do trabalho dentro de `~/trabalho/` e coloco no `~/.gitconfig`:

```
[user]
  name = Seu Nome
  email = voce@pessoal.com

[includeIf "gitdir:~/trabalho/"]
  path = ~/.gitconfig-trabalho
```

E no `~/.gitconfig-trabalho`:

```
[user]
  email = voce@empresa.com

[core]
  sshCommand = ssh -i ~/.ssh/id_ed25519_trabalho -o IdentitiesOnly=yes
```

Com isso, qualquer repositório dentro de `~/trabalho/` usa o e-mail e a chave do trabalho automaticamente, sem comando extra. Atenção à barra no final de `gitdir:~/trabalho/`: sem ela, a regra não pega as subpastas.

Para conferir o que está valendo num repositório:

```sh
git config user.email
git config core.sshCommand
```
