+++
title = "Pacotes privados em Go"
date = "2023-12-27"
tags = ["Golang"]
categories = ["post"]
draft = true
+++

Uma hora você quebra o código em vários repositórios e algum deles é privado. Aí o `go mod tidy`, que sempre funcionou, começa a falhar com mensagens sobre `410 Gone`, `verifying module` ou simplesmente fica parado esperando alguma coisa. Este post é a nota que eu queria ter tido quando isso aconteceu comigo.

## Por que quebra

Por padrão, o Go não baixa os módulos direto do GitHub. Ele passa pelo proxy público (`proxy.golang.org`) e confere o hash de cada módulo no banco de checksums (`sum.golang.org`). Nenhum dos dois consegue enxergar o seu repositório privado, então a busca falha antes de o Go tentar ir direto na fonte.

## GOPRIVATE

A variável `GOPRIVATE` diz ao Go quais módulos devem ser buscados direto no repositório, sem proxy e sem checagem no banco público. O jeito mais rápido de testar é na própria linha de comando:

```sh
GOPRIVATE=github.com/rfbatista/gohydrate GIT_TERMINAL_PROMPT=1 go mod tidy
```

O `GIT_TERMINAL_PROMPT=1` permite que o Git peça usuário e senha (ou token) no terminal. Por padrão o Go desliga esse prompt, e é por isso que às vezes o comando fica travado ou falha sem explicar nada.

Para não ter que lembrar disso toda vez, grave a configuração. Ela aceita padrões, então dá para liberar todos os seus repositórios de uma vez:

```sh
go env -w GOPRIVATE=github.com/rfbatista/*
```

Quem mantém privados os repositórios de uma organização inteira pode usar `github.com/minha-empresa/*` e pronto. O `GOPRIVATE` já serve de valor padrão para `GONOPROXY` e `GONOSUMDB`, então normalmente você não precisa mexer nessas duas.

## Autenticação

Resolvido o proxy, o Go vai chamar o Git, e o Git precisa conseguir se autenticar. Eu prefiro usar SSH, porque já tenho as chaves configuradas. Basta dizer ao Git para trocar HTTPS por SSH nos endereços do GitHub:

```sh
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

A partir daí, quando o Go pedir `https://github.com/rfbatista/gohydrate`, o Git vai buscar por SSH com a sua chave. Se você usa mais de uma conta no GitHub, vale ler o post sobre [gerenciar múltiplas contas do Git](/posts/managing-multiple-git-accounts/).

## E no CI?

No pipeline não tem chave SSH nem alguém para digitar senha. O que eu faço é gerar um token com permissão de leitura nos repositórios e usar o mesmo truque do `insteadOf`, agora com o token na URL:

```sh
git config --global url."https://${GITHUB_TOKEN}@github.com/".insteadOf "https://github.com/"
export GOPRIVATE=github.com/rfbatista/*
go mod download
```

Cuidado para esse token não aparecer nos logs, e dê a ele só a permissão de leitura que o build precisa.

## Resumo

1. `go env -w GOPRIVATE=github.com/seu-usuario/*`
2. Configure o Git para se autenticar: SSH com `insteadOf` na sua máquina, token no CI.
3. Se travar, rode de novo com `GIT_TERMINAL_PROMPT=1` para ver o que o Git está pedindo.

# Referências

- [Go Modules Reference: private modules](https://go.dev/ref/mod#private-modules)
