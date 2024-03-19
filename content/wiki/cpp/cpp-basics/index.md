+++
title = "C++ Basics"
date = "2023-10-02"
tags = ["c++"]
draft = false
+++

# C++ Basics

# Variaveis
Toda variável segue esse formato: **tipo**  **nome da variavel** = **inicialização (opcional)**
Ex.:

```cpp
int i1 = 2;
int i2, i3 = 5; //i2 não é inicializado
floar pi = 3.14159
char c1 = 'a', c2 = 35;
```

# Tipos pŕe definidos

![[Pasted image 20230827112516.png]]

# Caracteres e Strings
O tipo char pode ser utilizado para armazenar caracteres

```cpp
char c = 'f'
``` 

Você pode representar qualquer letra que encaixe em 8 bits em um caractere.

Podemos representar string como uma lista de caracteres

```cpp
char name[8] = "Herbert";
```

Esses tipos de string terminam com um binario `0` como valor em caracter. Adicionar mais caracteres nesta string é perigoso pois podera sobreescrever memória em outros locais. Por isso é recomendado não utilizar ela além de valores literais.
O compilador C++ distingue entre aspas simples e duplas: `'a'` é o caractere
“a” (tem o tipo char ) e `"a"` é um array com um binário 0 como terminação (ou seja, seu tipo é `const char[2]` ).
A forma mais conveniente para trabalhar com string é utilizando a class `string`

```cpp
# include < string >
int main ()
{
	std :: string name = " Herbert " ;
}
```

A classe `string`  utiliza memória dinamica e gerencia por ela mesma. Portanto se precisamos adicionar mais texto em uma string não precisamos nos preocupar com corrupção de memória ou erro na adicição do texto.

```cpp
name = name + ", hello world "
```

# Constantes
```cpp
const int c1 = 2;
```

Constantes são variáveis com atributo `const` como não podem ser modificadas é obrigatório inicializa-las ao serem declaradas.

# Literais
![[Pasted image 20230827134904.png]]

Existem 4 motivos principais do porque devemos tomar cuidado aos tipos de literais;
1. Disponibilidade
2. Ambiguidade
3. Acuracia
4. Numeros nao decimais

Apartir do  C++14 podemos criar uma string diretamente ao adicionar um `s`:

```cpp
f ( "I ' m not a string " ); // literal of type const char []
f ( "I ' m really a string " s ); // literal of type string
```

# Inicialização sem restrição
```cpp
long l2 = 1234567890123;
```

O código acima compila e funciona normalmente, porém o valor pode ser cortado em plataformas 32bits. C++11 introduz uma inicialização que garante que o valor não sera cortado:

```cpp
long l{1234567890123};
```

Nesse caso o compilador irá verificar se na arquietura do sistema o valor será mantido. Garantindo que o valor não irá perder precisão.

```cpp
int i1 = 3.14; // compiles despite narrowing ( our risk )
int i1n = { 3.14 }; // Narrowing ERROR : fractional part lost
unsigned u2 = - 3; // Compiles despite narrowing ( our risk )
unsigned u2n = {-3}; // Narrowing ERROR : no negative values
float f1 = { 3.14 }; // okay
```

# Escopo
O escopo determina o tempo de vida e visibilidade (variaveis não estaticas) e constantes e contribuem para estabelecer uma estrutura para o programa

## Global
No escopo global variaveis podem ser acessadas e modificadas em qualquer parte do programa. É recomendado evitar devido as implicações e a quantidade de erros que podem ser gerados quando variaveis forem modificadas dinamicamente.

## Local
A disponibilidade e visibilidade de variaveis no escopo local é determinado pelos limites dos colchetes `{ }`.

# Operadores Aritméticos
![[Pasted image 20230827152803.png]]

# Operadores Booleanos
![[Pasted image 20230827153704.png]]

Existem keyword representando cada uma dessas expressões, porém são pouco utilizadas com exceção do `not`

```cpp
big = !little ; // You knew before there ' s an !
big = not little ; // Much easier to spot , though
```

# Operadores Bitwise
![[Pasted image 20230827160503.png]]

# Assignment
![[Pasted image 20230827161457.png]]
```cpp
object = expr
```

Se os tipos da variaveis não são iguais, `expr` é convertido para o tipo do `object`se possivel.

```cpp
a *= b + c ; // corresponds to
a = a * ( b + c);
```

A operações são realizadas da direita para esquerda

# Fluxo do Programa
`c ? x : y`  operador ternario
*Comma Operator*

# Gestão de memória
Os operadores `new`  e `delete` aloca e desealoca memória respectivamente.

# Operadores de acesso
![[Pasted image 20230827161834.png]]

# Gestão de tipos
![[Pasted image 20230827161934.png]]

# Gestão de erros
`throw` é utilizado para indicar uma exceção na execução de um programa

# Overloading

# Expressões
Em muitas linguagens uma atribuição é considerado uma declaração, mas em c++ uma atribuição é avalida como uma expressão, dessa forma:
```cpp
x2= x= y + z;
```
É avaliado da direita para a esquerda

# Ramificação
## if-else
```cpp
if (x > 100)
	cout << "teste";
else
	cout << "else";
```
## condition ? result_for_true : result_for_false

## switch case

# Loops
## while and do-while

## for-loop
O loop consiste em 3 componentes:
1. A inicialização
2. Critério de continuidade
3. Uma operação em cada passo

## Range base for-loops
```cpp
int primes []= {2 , 3 , 5 , 7 , 11 , 13 , 17 , 19};
for ( int i : primes )
	std::cout << i << " ";
```

## Loop control
`break`
`continue`

# Funções
## Chamada por valor
```cpp
void increment(int x)
{
	++x;
}
```

## Chamada por referência
```cpp
void increment(int& x)
{
	++x;
}
```
Variaveis temporaria não podem passadas por referencia
```cpp
increment ( i + 9 ); // Error : temporary not referable
```
Para evitar que uma variavel passada por referência não seja modificada precisamos adicionar a propiedade `const`:
```cpp
double two_norm(const vector & v){ ... }
```
Em contraste parametros constantes permitem que variaveis temporarias sejam passadas na chamada da função por referência
```cpp
alpha = two_norm( v + w );
```

## Parametros com valores padrão
```cpp
double root ( double x , int degree = 2 ) { ... }
```

Essa função pode ser chamada com dois ou um parametro
```cpp
x = root (3.5 , 3);
y = root (7.0);// like root (7.0 , 2)
```
Valores padrões devem ser definidos por ultimo, assim após definir um valor padrão para um paramentro os próximos parametros precisam ter um valor padrão

## Inlining
Chamada de uma função é relativamente custosa, para evitar isso o compilador pode declarar a função `inline`
```cpp
inline double square ( double x ) { return x* x ; }
```
Mesmo declarando a função com a keyword `inline` o compilador pode não definir a função desta forma.

## Função `main`

```cpp
int main ( int argc , char * argv [] )
```
argc: quantidade de argumentos
argv: lista de argumentos

# Gestão de erros
## Assertions
A macro `assert`  que vem do header `cassert` é utilizado para avaliar uma expressão e caso o resultado seja `false` o programa é finalizado.
```cpp
#include <cassert>
double square_root ( double x )
{
	check_somehow ( x >= 0);
	...
	assert ( result >= 0.0);
	return result ;
}
```
Quando a verificação for falsa o programa ira terminar e exibir uma mensagem:
```text
assert_test : assert_test . cpp :10: double square_root (double):
Assertion ' result >= 0 . 0 ' failed .
```

Uma vantagem do `asset` é que podemos desaparecer com eles apenas com um parametro ao compilar o código:
```cpp
#define NDEBUG
#include < cassert >
```
Assim podemos apenas adicionar um parametro na compilação para habilitar os assert:
```
g ++ my_app . cpp -o my_app -O3 - DNDEBUG
```
Já que podemos desabilitar o conselho é*Testar o maximo de parametros*
## Throwing
```cpp
matrix read_matrix_file(const std::string& fname)
{
	fstream f(fname)
	if (!f.is_open())
		throw "Cannot open file"
}
```
Em c++ você pode passar qualquer tipo de dados no `throw`: string, number e etc.
Porém é melhor definir o tipo da exceção ou utilizar da biblioteca padrão.

## Catching
```cpp
try {
	A = read_matrix_file (" does_not_exist . dat " );
} catch ( const cannot_open_file & e ) {
	// Here we can deal with it , hopefully .
}
```

# IO
## Standard Output
`<<` insertion operator
`endl` produz uma nova linha e faz o flush do buffer

## Standard Input
```cpp
std::cin >> name;
```

## Input/Output com arquivos
![[Pasted image 20230827201908.png]]
Podemos utilizar os arquivos da mesma forma que utilizamos `cin` e `cout`:
```cpp
#include <fstream>
int main()
{
	std::ofstream square_file;
	square_file.open("squares.txt");
	for (int i=0; i<10; ++i)
		square_file << i << "^2 = " << i*i << "\n";
	square_file.close();
}
```
O código acima cria um arquivo chamado `squares.txt` ou sobreescreve caso já exista. Quando definimos  o operador << para um novo tipo, ele funcionara para arquivos e para o console (`cout` e `cin`)

## Stream generico
Qualquer classe pode ser utilizada como um stream se for derivada do `istream`, `ostream` e `iostream` . Podemos funções que aceitem qualquer tipo de stream ao aceitrar uma referencia mutável do `ostream`.
```cpp
#incluse <iostream>
#include <fstream>
#include <sstream>
void write_something(std::ostream& os)
{
	os << "Hi stream, did you know that 3 * 3 = " << 3 * 3 << '\n';
}
int main()
{
	std::ofstream myfile{"example.txt"}
	std::stringstream mystream;
	write_something(std::cout);
	write_something(myfile);
	write_something(mysstream);
	std::cout << "mysstream is: " << mysstream.str();
}
```

## Formatting
```cpp
cout << "pi is" << setprecision(16) << pi << '\n';
cout << "pi is" << setw(30) << pi << '\n';
cout << "pi is" << setfill('-') << pi << '\n';
cout.setf(ios_base::showpos);
```
I/O streams são formatadas por I/O manipulators, que são encontrados no header file `<iomanip>`
Não é recomendado a utilização do `printf` original do C, por dois motivos:
1. Não pode ser utilizado por tipos definidos por usuario
2. Não tem segurança na tipagem
A nova biblioteca `<format>`do C++20 combina a facilidade de formatação com tipagem segura. (Os compiladores nas seguintes versões ainda não tem suporte: GCC 12.0, Clang 13 e Visual Studio 16.9.6)

## Gerenciando erros I/O
Por padrão streams não lançam erros
```cpp
int main ()
{
	std :: ifstream infile ;
	std :: string filename { " some_missing_file.xyz " };
	bool opened = false ;
	while (! opened ) {
		infile.open ( filename );
		if ( infile.good () ) {
		opened = true ;
		} else {
			std :: cout << " The file ' " << filename
			<< " ' doesn ' t exist ( or can 't be opened ) ,"
			<< " please give a new filename : ";
			std::cin << filename ;
		}
	}
	int i ;
	double d ;
	infile << i << d;
	if ( infile.good() )
		std::cout << " i is " << i << " , d is " << d << '\n';
		else
		std::cout  " Could not correctly read the content \n";
		infile.close ();
}
```

## Filesystem

# Arrays, Pointers e Referências

Em c++ o tamanho de um array deve ser conhecido em tempo de compilação

```cpp
// x[0] inicio do array x[9] final doarra
int x[10];

// Arrays podem ser inicializados apartir da definição
float v []= {1.0 , 2.0 , 3.0} , w []= {7.0 , 8.0 , 9.0} ;

int v []= {1.0 , 2.0 , 3.0} ; // Error in C ++11: narrowing <- coversao de float-point literal para int potencialmente perde precisão

// Podemos definir vetores de alta dimensão 
float A [7][9] ;
int q [3][2][3] ;
```

Um array não contém explicitamente seu tamanho, como sabemos o tamanho do array antes da compilação podemos encontrar apartir da seguinte divisão

```cpp
sizeof x/sizeof x[0]
```

# Pointers
Um ponteiro é uma variavel que contém uma endereço de memória
```cpp
int* y = new int[10] // aloca um array de tamanho 10
```

O programador é o responsável por liberar a memória caso não utilize mais o ponteiro

```cpp
delete[] y;
```
