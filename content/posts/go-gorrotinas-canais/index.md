+++
title = "Gorrotinas e Canais"
date = "2023-10-02"
tags = ["Golang", "data-structures"]
draft = true
+++

```
go f() // cria uma nova gorrotina que chama f()
```

# Canais
Os canais sãos os meios de comunicação entre as gorrotinas
Cada canal é um comunicador de um tipo particular
```
ch := make(chan int) // ch é do tipo chan int
```
Um canal é uma referência a estrutura criada por make

- instrução de envio: `ch <-x`
- instrução de recpção em uma instrução de atribuição: `x = <-ch`
- instrução de recepção com resultado descartado: `<-ch`

### Para fechar um canal
`close(ch)`

# Pipelines

# Canais unidirecionais


# Canais sem buffer
Uma gorrotina sem buffer bloquei a gorrotina que envia até o receptor executar a recepção e também bloquei a recptora até receber um envio.
- Canais sem buffer faz com que as gorotinas fiquem sincronizadas, isso é um dos casos de uso para utilização de canais sem buffer

```
func main(){
	conn, err := net.Dial("tcp", "localhost:8000")
	if err != nil {
		log.Fatal(err)
	}
	done := make(chan struct{}) // usamos uma struct vazia para enfatizar que o canal não transporta qualquer informação
	go func(){
		io.Copy(os.Stdout, conn)
		log.Println("done")
		done <- struct{}{}
	}
	mustCopy(conn, os.Stdin)
	conn.Close()
	<-done // espera a gorrotina em background terminar (sincronização)
}


```

# Pipelines
Gorrotinas podem ser conectadas de formar que a saida de uma seja a entrada de outra, isso se chama `pipeline`
```
func main(){
	naturals := make(chan int)
	squares := make(chan int)
	go func(){
		for x:=0; ;x++{
			naturals <- x
		}
	}()
	go func(){
		for {
			x := <- naturals
			squares <- x * x
		}
	}
	for {
		fmt.Println(<-squares)
	}
}
```

- Após o canal ser fechado e drenado, todas as instruções de recebimento no canal não serão mais bloqueadas, sempre retornando um valor zero.
- Intruções de envio em um canal fechado irá gerar pânico

### Tipos de canais

`chan<- int`  - canal somente para envio
`<-chan int` - canal somente para recebimento

- É um erro de tempo de compilação tentar fechar um canal de recebimento, pois o `close` só garante que não irá ocorrer mais envio em um canal

# Canais com buffer

Canais com buffers, garantem o envio de mensagens para uma fila com tamanho prefixado, desta forma caso a fila não esteja completa o canal de envio não será bloqueado

- `gorotinas com vazamento de memoria (Ex.: com bloqueio do canal) não serao coletadas automaticamente, ocupando permanentemente espaço de memória`

# Looping em paralelo
```
for _, f := range filenames {
	go func(){
		thumbnail.Imagefile(f) // *** INCORRETO ***
	}()
}

for _, f := range filenames {
	go func(f string){
		thumbnail.Imagefile(f) // *** INCORRETO ***
	}(f)
}
```
No exemplo acima acessamos a váriavel f internamente na gorrotina, porém o uso neste caso é incorreto pois a variavel `f` é atualizada a cada iteração do loop

```

for _, f := range filenames {
	go func(f string){
		_, err := thumbnail.Imagefile(f) // *** INCORRETO ***
		errors <- err
	}(f)
}

for range filenames {
	if err := <- errors; err != nil {
		return err // incorreto vazamento de gorrotina
	}
}

```

# Impondo limites em concorrencia
```
var tokens = make(chan struct{}, 20)

func crawl(url string)[] string {
	fmt.Println(url)
	token <- struct{}{} // adquire um token
	list, err := links.Extract(url)
	<-tokens // libera o token
}
```
O código acima implementa uma técnica de concorrencia chamada `semaforo contador` (counting semaphore), isso garante que no máximo 20 requisições sejam executadas em paralelo

# 📚 Referências
https://github.com/golang/go/wiki
