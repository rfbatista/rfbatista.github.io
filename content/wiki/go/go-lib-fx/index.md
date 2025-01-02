+++
title = "Dependency injection system for Go"
date = "2024-02-03"
tags = ["golang"]
draft = false
+++

# Parameter Object

São objetos com o propósito de carregar para métodos ou funções como as funções `New*` que criam objetos.

```go
type ClientParams struct {
  fx.In

  Config     ClientConfig
  HTTPClient *http.Client
}

func NewClient(p ClientParams) (*Client, error) {
  return &Client{
    url:  p.Config.URL,
    http: p.HTTPClient,
    // ...
  }, nil
```

# Result Object

Similar ao **Parameter Object** é utilizado para carregar os resultados de uma função ou método, o objeto é definido
exclusivamente por uma função ou método

```go
type Result struct {
  fx.Out

  Client *Client
}

func New() (Result, error) {
  client := &Client{
    // ...
  }
  return Result{
    Client: client,
  }, nil
```
