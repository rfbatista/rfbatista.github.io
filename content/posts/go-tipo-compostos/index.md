+++
title = "GO - Tipos compostos"
date = "2023-10-02"
tags = ["Golang"]
draft = true
+++

# Array

Um array é uma sequencia de tamanho fixo de zero ou mais elements

```
var q [3]int = [3]int{1,2,3}
q := [...]int{1,2,3} // com a reticencia o tamano será determinado pela quantidade de inicializadores
```

O tamanho de um array faz parte do seu tipo

```
q := [3]int{1,2,3}
q = [4]int{1,2,3,4} // erro de compilação: não é permitido atribuir [4]int a [3]int
```

Arrays são inflexiveis

# Fatias (slices)

Uma fatia representa um sequencia de tamanho variavel cujo elementos tem o mesmo tipo.
Uma fatia tem tres elementos:

- um ponteiro: aponta para o primeiro elemento do array acessivel pela fatia
- tamanho: número de elementos da fatia, não pode exceder a capacidade
- capacidade: numero de elementos entre o inicio da fatia e o final do array subjacente
  As funções:
- `len` - retorna o tamanho
- `cap` - retorna a capacidade

Uma fatia pode ser extendia além de seu tamanho, mas não além da sua capacidade.
Como uma fatia contém um ponteiro para o `array subjacente` isso permite que uma função modifique os elementos do `array subjacete`

### Make

```
make([]T, len)
make([]T, len, cap) // mesmo que make ([]T, cap)[:len]
```

### Função append

```
u := [11]int{}
y := u[:10]
fmt.Println(u, y)
z := append(y, 2, 3)
```

Esta função vai extender o slice caso a capacidade do `array subjacente` seja suficiente para encaixar os novos elementos, caso contrário é criado um novo `array subjacente` com capacidade suficiente para encaixar os novos elementos.

# Mapas

É uma referência a uma tabela hash, escrito como `map[K]V`
Requisitos:

- Todas as chaves são do mesmo tipo
- Todos os valores são do mesmo tipo
- Mas as chaves e valores não precisam ser do mesmo tipo
- O tipo da chave `K` deve ser comparavel

```
ages := make(map[string]int)
deletes(ages, "alice") // remove o elemento com a chave "alice"
```

- Um elemento de mapa não é uma variavels, então não podemos obter seu endereço (adicionar um novo elemento pode alterar os endereços por isso não é possivel acessar o ponteiro)
- Não é possivel atribuir valores a um mapa não alocado
  ` ages["carol"] =  21 // pânico: atribuição a uma entrada em um mapa nil`
- Acessar um elemento do mapa sempre ira retornar um valor, para verificar podemos fazer essa operação:
  `age, ok := ages["bob"]; !ok { //bob não é uma chave nesse mapa
- Mudanças nos mapas realizadas por funções serão efetuadas no mapara original sem a necessidade de passar ponteiros. Exemplo:

```
import (
	"fmt"
)

func main() {
	m := map[string]int{"originalMap": 1}
	reallocate(m)
	fmt.Println(m) // prints originalMap: 1
	reallocatePtrWrong(&m)
	fmt.Println(m) // prints originalMap: 1
	reallocatePtr(&m)
	fmt.Println(m) // prints overrideMap: 1
	extend(m)
	fmt.Println(m) // prints overrideMap: 1 extended: 2
}

func reallocate(m map[string]int) {
	// Orginal value of m outside function not changed.
	m = map[string]int{"overrideMap": 1}
}

func extend(m map[string]int) {
	// Chaging m without realocation works, and don't need a pointer.
	m["extended"] = 2
}

func reallocatePtrWrong(m *map[string]int) {
	// Realocate using pointer don't become visible outisde if we
	// only update the poniter value.
	m = &map[string]int{"overrideMap": 1}
}

func reallocatePtr(m *map[string]int) {
	// Realocate using pointer work if we do it right.
	*m = map[string]int{"overrideMap": 1}
}
```

# Estruturas

A estrutura é um tipo de dado que agregra diferentes tipos em uma unica entidade.

- Não é possivel acessar campos não exportados em outros pacores

```
package p
type T struct{a, b int}
package p
va _ = p.T{a: 1, b:2 } // erro de compilação: não é possivel referencias a, b
va _ = p.T{1, 2} // erro de compilação: não é possivel referencias a, b
```

- se todos os campos de uma estrutura são comparaveis, então a estrutura é comparável

### Campos anônimos

```
type Circle struct {
	Point
	Radius int
}
```

Com o campo anônimo podemos acessar várivaeis correspondentes ao tipo anonimo diretamente na raiz:

```
var c Circle
c.X = 10 // se não fosse anonimo precisariamos acessar assim x.Point.X = 10
c.Y = 10

```

Porém para popular os campos na inicialização precisamos declarar os tipos especificados

```
c := Circle{Point{x: 1, y: 2}, 10}
```

```
pp := &Point{1, 2}
```
