+++
title = "GO - Strings"
date = "2023-10-02"
tags = ["Golang", "data-structures"]
draft = true
+++

Uma string é uma sequencia imutavel de bytes
As strings de text são convencionalmente interpretadas como sequencias de pontos de código Unicode (`runas`) codificadas em UTF-8.

A função `len`devolve o número de bytes não de runas

```golang
s :+ "hello, world"
fmt.Println(len(s)) // 12
fmt.Println(s[0], s[7])  // "104 119"
```

O iésimo byte de uma string não corresponde diretamente ao iésimo caracter, pois a codificação `UTF-8` de um ponto de código que não seja ASCII exige mais.

Como strings são imutáveis, operações que tentam modificar os dados de uma string in-place não são permitidas

# Unicode

Em golang um unicode é representado como uma `runa`. Com a versão 8 capaz de representar mais de 120 mil caracteres.
O tipo natural para armazenar uma única runa é `int32`
Com isso podemos representar uma sequência de runas com uma sequência de valores `int32`.
Essa representação se chama UTF-32 ou USC-4
Cada ponto de codígo Unicode tem 32 bits
Ocupa mais espaço que ASCII, que exige apenas 8 bits

# UTF-8

O UTF-8 é uma codificação de tamanho varíavel de pontos de código unicode na forma de bytes.
Esse padrão usa entre um e 4 bytes
Os bits de alta ordem no primeiro byte da runa indicam quantos bytes existem na sequencia

```
0XXXXXXX runas (0-127) ASCII
110XXXXX 10XXXXXX 128-2047
1110XXXX 10XXXXXX 10XXXXXX 2048-65535
11110XXX 10XXXXXX 10XXXXXX 10XXXXX 65536-0x10ffff
```

UTF-8 é a codificação preferida para strings de texto manipulados em GO
A ordem lexicográfica dos bytes é igual a ordem dos pontos de código Unicode

- Em uma string literal. Ex("hello world"), podemos utilizar escape para incluir valor arbitrário de bytes. Ex.:

```
\u4e16
\U00004E16
```

```
import (
	"fmt"
	"unicode/utf8"
)

func main() {
	s := "Hello, 世界"
	fmt.Println(len(s)) // 13
	fmt.Println(utf8.RuneCountInString(s)) // 9
}
```

```
import (
	"fmt"
	"unicode/utf8"
)

func main() {
	s := "Hello, 世界"
	for i := 0; i < len(s); {
		r, size := utf8.DecodeRuneInString(s[i:])
		fmt.Printf("%d\t%c\n", i, r)
		i += size
	}
	fmt.Println(s[2:])
	str := "Hello, 世界"

	for len(str) > 0 {
		r, size := utf8.DecodeRuneInString(str)
		fmt.Printf("%c %v\n", r, size)

		str = str[size:]
	}
	str = "Hello, 世界"

	r, size := utf8.DecodeRuneInString(str[0:]) // retorna a primeira runa encontrada
	fmt.Printf("%c %v\n", r, size)
}

```

O loop `range` quando aplicado a uma string ja executa a decodificacao implicitamente e

# Conversão string e números

```
strconv.Itoa(123) // "123"
```

# Gerador de constantes iota
