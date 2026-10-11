+++
title = "Servidor gRPC em Go"
date = "2023-10-02"
tags = ["Golang", "grpc"]
categories = ["post"]
draft = true
+++

Neste post eu monto um servidor gRPC mínimo em Go, do arquivo `.proto` até um cliente chamando o servidor. Se você nunca mexeu com Protocol Buffers, talvez valha ler antes o [post sobre protobuf](/posts/go-protocol-buffers/), porque o gRPC é construído em cima dele.

## Instalando os plugins

Você precisa do compilador `protoc` (no Ubuntu é `sudo apt install protobuf-compiler`, no Mac `brew install protobuf`) e de dois plugins para Go: um gera as mensagens e o outro gera o código do serviço.

```sh
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

Os plugins são instalados em `$GOBIN`, que por padrão é `$GOPATH/bin`. Essa pasta precisa estar no seu `$PATH`, senão o `protoc` não encontra os plugins e reclama com uma mensagem nada amigável.

## O contrato

Crie um projeto e o arquivo `proto/greeter.proto`:

```sh
mkdir hello-grpc && cd hello-grpc
go mod init github.com/seu-usuario/hello-grpc
```

```proto
syntax = "proto3";

package greeter;

option go_package = "github.com/seu-usuario/hello-grpc/proto";

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
}

message HelloRequest {
  string name = 1;
}

message HelloReply {
  string message = 1;
}
```

E gere o código:

```sh
protoc --go_out=. --go_opt=paths=source_relative \
       --go-grpc_out=. --go-grpc_opt=paths=source_relative \
       proto/greeter.proto
```

Vão aparecer dois arquivos em `proto/`: `greeter.pb.go`, com as mensagens, e `greeter_grpc.pb.go`, com a interface do servidor e o cliente. Não edite nenhum dos dois, eles são regerados toda vez.

## O servidor

```go
package main

import (
	"context"
	"log"
	"net"

	pb "github.com/seu-usuario/hello-grpc/proto"
	"google.golang.org/grpc"
)

type server struct {
	pb.UnimplementedGreeterServer
}

func (s *server) SayHello(ctx context.Context, req *pb.HelloRequest) (*pb.HelloReply, error) {
	return &pb.HelloReply{Message: "Olá, " + req.GetName()}, nil
}

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("falha ao escutar: %v", err)
	}

	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})

	log.Println("servidor ouvindo em :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("falha ao servir: %v", err)
	}
}
```

Rode `go mod tidy` para baixar as dependências e `go run .` para subir.

## Por que esse Unimplemented ali?

Essa linha confunde todo mundo na primeira vez. O plugin `protoc-gen-go-grpc` exige que a implementação do serviço embuta a struct `Unimplemented<NomeDoServico>Server`. Ela já tem todos os métodos do serviço, cada um retornando o erro `Unimplemented`.

O motivo é compatibilidade com o futuro. Se amanhã alguém adicionar um `rpc SayGoodbye` no `.proto` e regerar o código, o seu servidor continua compilando. Quem chamar `SayGoodbye` recebe um erro dizendo que o método não foi implementado, em vez do build inteiro quebrar.

Esse comportamento mudou em relação ao gerador antigo, que vinha junto com o `protoc-gen-go`. Dá para voltar ao jeito antigo com uma opção:

```sh
protoc --go-grpc_out=. --go-grpc_opt=require_unimplemented_servers=false proto/greeter.proto
```

A própria documentação diz que não é recomendado e que a opção só existe para manter compatibilidade com código gerado antes. Eu deixo o padrão.

## Um cliente para testar

Em outra pasta, por exemplo `cmd/client/main.go`:

```go
package main

import (
	"context"
	"log"
	"time"

	pb "github.com/seu-usuario/hello-grpc/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

func main() {
	conn, err := grpc.NewClient("localhost:50051",
		grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("falha ao conectar: %v", err)
	}
	defer conn.Close()

	client := pb.NewGreeterClient(conn)

	ctx, cancel := context.WithTimeout(context.Background(), time.Second)
	defer cancel()

	resp, err := client.SayHello(ctx, &pb.HelloRequest{Name: "Renan"})
	if err != nil {
		log.Fatalf("erro na chamada: %v", err)
	}
	log.Println(resp.GetMessage())
}
```

Com o servidor rodando, `go run ./cmd/client` deve imprimir `Olá, Renan`.

O `insecure` está aí porque estamos em localhost sem TLS. Em qualquer coisa que saia da sua máquina, configure TLS de verdade. E sempre passe um contexto com timeout nas chamadas: sem ele, um servidor travado deixa o cliente esperando para sempre.

# Referências

- [gRPC Go: Quick start](https://grpc.io/docs/languages/go/quickstart/)
- [protoc-gen-go-grpc README](https://github.com/grpc/grpc-go/blob/master/cmd/protoc-gen-go-grpc/README.md)
