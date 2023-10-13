+++
title = "Funcoes em Golang"
date = "2023-10-02"
tags = ["Golang", "data-structures"]
draft = true
+++

# Declaração de funções

```
func nome(lista-de-parametros) (lista-de-resultados)
```

# Estratégias de tratamento de erro
- Propagar o error de forma que a falha em uma subrotina torne-se uma falha na rotina que fez a chamada

```
fmt.Errorf("novo error %s", variavel_string, err) // cria erros descritivos ao prefixar sucessivamento informações adicionais
```

- As strings das mensagens de erro não devem começar com a letra maiusculas pois as mensagens de erro com frequencia são encadeadas

# Funções variádicas
É uma função que pode ser chamda com um número váriavel de argumentos.
```
func sum(vals ...int) int {
	total := 0
	for _, val := range vals {
		total += val
	}
	return total
}
```

# `defer`  
- Instrução utilizada para adiar a excução de uma função até o término da função onde está incluida.
- É frequentemente incluida em pares? lock/unlock, garantir que recursos alocados sejam liberados
- depuração de funções complexas
```
func bigSlowOperation(){
	defer trace("op")() 
	// ... tarefas executadas
}
func trace(msg string) func(){
	start := time.Now() 
	log.Printf("enter %s, msg") // até essa linha o código é executado no inicio da operação em bigSlowOperation
	return func()... // quando bigSlowOperation é finalizada essa função é invocada
}
```

# Pânico
Muitos erros são capturados em tempo de execução, porém outros como desreferenciar um ponteiro `nil` exige verificações em tempo de execução. Quando o runtime do Go identifica esses erros, um pânico é gerado.

# Recuperação
```
func Parse(input string) (s *Syntax, err error){
	defer func(){
		if p := recover(); p != nil {
			err = fmt.Errorf("internal error: %v", p)
		}
	}
}
```
