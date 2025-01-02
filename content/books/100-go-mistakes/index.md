+++
title = "100 Go Mistakes"
date = "2024-03-16"
tags = ["go", "book"]
categories = ["book"]
draft = false
+++

# 100 Go Mistakes

## 1: Unintended variable shadowing

```go
var client *http.Client // esse valor sempre será nil, pois o client atribuido nas
                        // condições abaixos não será o mesmo
if tracing {
    client, err := createClientWithTracing()
    if err != nil {
        return err
    }
    log.Println(client)
} else {
    client, err := createDefaultClient()
    if err != nil {
    return err
}
    log.Println(client)
}
```
Alternativa para evitar  shadowing

```go
var client *http.Client
var err error
if tracing {
    client, err = createClientWithTracing()
} else {
    client, err = createDefaultClient()
}
if err != nil {
// Common error handling
}

```
## 2: Unnecessary nested code

Código com uma leitura facil demandam um esforço menor para serem mantidos funcionando e respeitando uma arquitetura
prédeterminada. Um aspecto importante na dificuldade para a leitura de um código é o nível de aninhamento mantido nele.

```go
func join(s1, s2 string, max int) (string, error) {
        if s1 == "" {
    return "", errors.New("s1 is empty")
    } else {
        if s2 == "" {
            return "", errors.New("s2 is empty")
        } else {
            concat, err := concatenate(s1, s2)
            if err != nil {
            return "", err
            } else {
            if len(concat) > max {
                return concat[:max], nil
            } else {
                return concat, nil
            }
            }
        }
    }
}
```

```go
func join(s1, s2 string, max int) (string, error) {
    if s1 == "" {
        return "", errors.New("s1 is empty")
    }
    if s2 == "" {
        return "", errors.New("s2 is empty")
    }
    concat, err := concatenate(s1, s2)
    if err != nil {
        return "", err
    }
    if len(concat) > max {
        return concat[:max], nil
    }
    return concat, nil
}
```

Se um bloco `if` retornar devemos evitar o uso do `else`

## 3: Misusing init functions

Uma função `init` é utilizada para inicializar o estado de uma aplicação. Ela não contém nenhum argumento e não 
retorna resultados. A inicialização de um pacote segue os seguintes passos:
1. Todas as constantes e variaveis do pacote são avalidas
2. a função `init` é executada

## 4: Overusing getters and setters

## 5: Interface pollution
Algumas situações que devemos considerar para o uso de interfaces:
1. Comportamento comum
2. Desacoplamento
3. Restrição de comportamento

## 6: Interface on the producer side
Na maioria dos casos deixe o cliente criar sua definição de interface baseada na implementação do produtor. Dessa forma
o cliente pode definir a interface mais apropiada para o seu caso de uso.

## 7: Returning interfaces

Retornar interfaces obrigam aos clientes dependerem da mesma abstração, se um cliente precisar de uma abstação 
ele ainda pode realizar do seu lado. Retornar uma interface é tentar prever o futuro na esperança de que a abstração será útil 
para todos os clientes. Abstrações não devem ser forçadas na maioria dos casos mas descobertas pelos clientes.

## 8: any says nothing

## 9: Being confused about when to use generics

## 10: Not being aware of the possible problems with type embedding

Em golang uma propiedade de uma `struct` é considerado incorporado se é declarado sem um nome:

```go
type Foo struct {
 Bar
}
```
Dessa forma métodos de Bar ficam disponiveis em Foo

Incoporar uma struct é sobre composição e não herança

## 11: Not using the functional options pattern

Lidar com a evolução de uma api pode ser algo frustante, mudanças na api podem obrigar a mudança de acesso em 
todos os clientes do seu código para evitar isso podemos utilizar o padrão funcional de opções.

```go 
type options struct { // struct que contém todas as opções de configuração
    port *int
}
type Option func(options *options) error // tipagem para funções de configuração

func WithPort(port int) Option {        // a função de configuração que atualiza a struct de configuração
    return func(options *options) error {    
        that updates the port
        if port < 0 {
        return errors.New("port should be positive")
        }
        options.port = &port
        return nil
    }
}

func NewServer(addr string, opts ...Option) { // argumento variadic que aceita uma lista de funções para configuração
    var options options
    for _, opt := range opts {
        err := opt(&options)
        if err != nil {
            return nil, err
        }
    }
}
```

## 12: Project misorganization
- /cmd — The main source files. The main.go of a foo application should live in /cmd/foo/main.go.
- /internal — Private code that we don’t want others importing for their applications or  libraries.
- /pkg — Public code that we want to expose to others.
- /test — Additional external tests and test data. Unit tests in Go live in the same
package as the source files. However, public API tests or integration tests, for example, should live in /test.
- /configs — Configuration files.
- /docs — Design and user documents.
- /examples — Examples for our application and/or a public library.
- /api — API contract files (Swagger, Protocol Buffers, etc.).
- /web — Web application-specific assets (static files, etc.).
- /build — Packaging and continuous integration (CI) files.
- /scripts — Scripts for analysis, installation, and so on.
- /vendor — Application dependencies (for example, Go modules dependencies).

## 13: Creating utility packages

é uma má pratica a criação de um pacote util, common, e base

## 14: Ignoring package name collisions

```go 
redis := redis.NewClient()
v, err := redis.Get("foo")
```

## 15: Missing code documentation

Todo elemento exportado deve ser documentado, a convenção é adicionar comentarios iniciando com o 
nome do elemento exportado.

```go 
// Customer is a customer representation.
type Customer struct{}

// Package math provides basic constants and mathematical functions.
//
// This package does not guarantee bit-identical results
// across architectures.
package math
```

## 16: Not using linters

- https://golang.org/cmd/vet/—A standard Go analyzer
- https://github.com/kisielk/errcheck—An error checker
- https://github.com/fzipp/gocyclo—A cyclomatic complexity analyzer
- https://github.com/jgautheron/goconst—A repeated string constants analyzer
- https://github.com/golangci/golangci-lint
