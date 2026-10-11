+++
title = "Endereçabilidade em Go: por que não dá para alterar um campo dentro do map"
date = "2023-10-02"
tags = ["Golang"]
categories = ["post"]
draft = true
+++

Todo mundo que programa em Go já tropeçou nesse erro pelo menos uma vez:

```go
type Ponto struct {
	X, Y int
}

pontos := map[string]Ponto{"a": {1, 2}}
pontos["a"].X = 10 // não compila
```

O compilador reclama com algo como `cannot assign to struct field pontos["a"].X in map`. A primeira reação é achar que é uma limitação boba. Não é, e entender o motivo explica uma porção de outros erros parecidos.

## O que é ser endereçável

Em Go, um valor é *endereçável* quando ele mora num lugar fixo da memória e você pode pegar o endereço dele com `&`. A especificação lista o que é endereçável:

- variáveis;
- o que você acessa através de um ponteiro (`*p`);
- elementos de um slice (`s[i]`);
- campos de uma struct endereçável (`v.Campo`);
- elementos de um array endereçável (`a[i]`).

Tudo o que não está nessa lista não é endereçável. Os casos mais comuns:

- elementos de map (`m["chave"]`);
- valor de retorno de função (`f()`);
- constantes e literais (`&42` não existe);
- bytes de uma string (`s[0]` dá para ler, mas não dá para mudar nem pegar o endereço).

E a regra que amarra tudo: para atribuir a algo, ou para chamar um método com receiver de ponteiro, esse algo precisa ser endereçável. A única exceção é a atribuição direta a um elemento de map, `m["a"] = v`, que é tratada de forma especial.

## Por que o map não deixa

Um map em Go é uma tabela hash, e ela cresce. Quando passa de um certo nível de ocupação, o runtime aloca uma tabela maior e move os elementos para lá. Se a linguagem deixasse você guardar `&pontos["a"]`, esse ponteiro poderia apontar para uma região que não pertence mais ao map depois de um crescimento. Para evitar isso, Go proíbe pegar o endereço de um elemento de map, e alterar um campo do elemento cai na mesma regra.

O slice não tem esse problema da mesma forma. Quando ele cresce, o `append` devolve um slice novo apontando para outro array, mas o array antigo continua existindo enquanto alguém fizer referência a ele. Por isso `s[0].X = 10` compila.

## Os outros sintomas

O mesmo motivo aparece com métodos que têm receiver de ponteiro:

```go
func (p *Ponto) Mover(dx int) { p.X += dx }

pontos["a"].Mover(1) // não compila: o elemento não é endereçável
```

E com retorno de função:

```go
func novoPonto() Ponto { return Ponto{} }

p := &novoPonto()   // não compila
novoPonto().X = 3   // também não
```

Uma curiosidade: `&Ponto{1, 2}` compila, mesmo que um literal não seja endereçável. É uma exceção da linguagem para literais compostos, feita por conveniência.

## Como contornar

A saída mais simples é ler, alterar e escrever de volta:

```go
p := pontos["a"]
p.X = 10
pontos["a"] = p
```

Ou guardar ponteiros no map. Assim o elemento do map é o ponteiro, e o que você altera é a struct para onde ele aponta, que mora fora da tabela:

```go
pontos := map[string]*Ponto{"a": {1, 2}}
pontos["a"].X = 10 // compila
pontos["a"].Mover(1)
```

Qual usar depende do caso. Ponteiros evitam cópias quando a struct é grande e permitem alterar no lugar, mas significam mais alocações e o risco de dois lugares do código mexerem no mesmo valor sem perceber. Para structs pequenas eu costumo ficar com a cópia.

# Referências

- [Not addressable in Golang (sobyte)](https://www.sobyte.net/post/2022-01/not-addressable-in-golang/)
- [The Go Programming Language Specification: Address operators](https://go.dev/ref/spec#Address_operators)
