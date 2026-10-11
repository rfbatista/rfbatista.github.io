+++
title = "Protocol Buffers"
date = "2023-10-02"
tags = ["Golang", "protobuf"]
categories = ["post"]
draft = true
+++

Quando a gente constrói uma API pública, a primeira opção que vem à cabeça para mandar dados pela rede é JSON. Ele é legível, todo mundo conhece e qualquer linguagem sabe ler. Mas se você controla os clientes que vão consumir esses dados, por exemplo na comunicação entre seus próprios serviços, dá para explorar outros formatos. É aí que o Protocol Buffers brilha. Na definição do Google, ele é um mecanismo extensível, neutro de linguagem e de plataforma, para serializar dados estruturados.

Na prática: você descreve a forma dos seus dados num arquivo `.proto`, um compilador gera código para a sua linguagem e esse código sabe transformar os objetos em bytes e de volta.

## Por que usar

- Serialização rápida e mensagens pequenas, porque o formato é binário e não repete o nome dos campos em toda mensagem.
- Tipagem: o contrato é compilado, então mandar texto num campo numérico vira erro de compilação em vez de bug em produção.
- Compatibilidade entre versões, se você seguir algumas regras (mais sobre isso abaixo).
- Código gerado para várias linguagens a partir do mesmo arquivo, o que ajuda muito quando o serviço em Go conversa com outro em Python.

## Um exemplo

```proto
syntax = "proto3";

package exemplo;

option go_package = "github.com/seu-usuario/exemplo-proto/pessoa";

message Pessoa {
  string nome = 1;
  int32 idade = 2;
  repeated string emails = 3;
}
```

Os números `= 1`, `= 2` e `= 3` não são valores padrão. São os identificadores dos campos, e é isso que vai para o fio no lugar do nome. Guarde essa informação, ela é a parte mais importante do post.

Para gerar o código Go, instale o plugin e rode o `protoc`:

```sh
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
protoc --go_out=. --go_opt=paths=source_relative pessoa.proto
```

E para usar:

```go
package main

import (
	"encoding/json"
	"fmt"
	"log"

	"github.com/seu-usuario/exemplo-proto/pessoa"
	"google.golang.org/protobuf/proto"
)

func main() {
	p := &pessoa.Pessoa{
		Nome:   "Maria",
		Idade:  30,
		Emails: []string{"maria@exemplo.com"},
	}

	bin, err := proto.Marshal(p)
	if err != nil {
		log.Fatal(err)
	}

	js, _ := json.Marshal(p)

	fmt.Println("protobuf:", len(bin), "bytes")
	fmt.Println("json:", len(js), "bytes")

	var lida pessoa.Pessoa
	if err := proto.Unmarshal(bin, &lida); err != nil {
		log.Fatal(err)
	}
	fmt.Println(lida.GetNome())
}
```

Nesse caso a mensagem em protobuf tem 28 bytes e a mesma informação em JSON compacto tem 58. A diferença vem principalmente dos nomes dos campos, que o JSON repete em toda mensagem e o protobuf troca por um byte com o número do campo. Números pequenos também ocupam pouco, porque são codificados como *varint*: o 30 da idade cabe em um byte.

(Se for converter mensagens protobuf para JSON de verdade, use o pacote `protojson` em vez do `encoding/json`. Usei o segundo aqui só para comparar o tamanho.)

## Compatibilidade: as regras que importam

Como o que trafega é o número do campo, você pode renomear um campo à vontade sem quebrar nada. O que não pode é mudar o significado de um número. As regras que eu sigo:

- Nunca troque o número de um campo que já está em uso.
- Nunca reaproveite o número de um campo removido. Marque como reservado:

```proto
message Pessoa {
  reserved 2;
  reserved "idade";
  string nome = 1;
  repeated string emails = 3;
  string data_nascimento = 4;
}
```

- Adicionar campo novo é seguro. Quem tem o código antigo simplesmente ignora o campo que não conhece, e quem tem o código novo recebe o valor padrão quando o campo não vem.
- Mudar o tipo de um campo é, na maioria dos casos, quebrar o contrato. Prefira criar um campo novo.

Seguindo isso, o serviço A pode subir uma versão nova sem esperar o serviço B ser atualizado. Para quem já fez deploy coordenado de dois serviços às duas da manhã, isso vale muito.

## Quando não usar

Protobuf não é bala de prata. Você não consegue abrir a mensagem e ler com os olhos, o que deixa debugar um pouco mais chato. Precisa distribuir os arquivos `.proto` entre os times e manter isso organizado. E para uma API pública consumida por navegadores e por gente que você nunca vai conhecer, JSON continua sendo a escolha mais sensata.

Onde ele faz mais sentido é na comunicação entre serviços que você controla, e é a base do gRPC, que eu mostro no [post sobre servidor gRPC em Go](/posts/go-grpc-server/).

# Referências

- [Protocol Buffers: documentação oficial](https://protobuf.dev/)
- [Guia da linguagem proto3](https://protobuf.dev/programming-guides/proto3/)
