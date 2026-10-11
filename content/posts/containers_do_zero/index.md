+++
title = "Container do zero"
date = "2024-10-12"
tags = ["linux", "containers", "c"]
categories = ["post"]
draft = true
+++

A gente usa Docker todo dia e quase nunca para pra pensar no que é um container. A resposta curta é meio decepcionante: container não existe no kernel. Não tem uma syscall `create_container()`. O que existe é um punhado de recursos do Linux que, combinados, fazem um processo comum achar que está sozinho na máquina.

Neste post eu monto um container bem simples em C, peça por peça. A ideia não é substituir o Docker, é entender o que ele faz por baixo. Boa parte do que está aqui eu aprendi lendo o código do [barco](https://github.com/lucavallin/barco) e do [c_container](https://github.com/nathanagez/c_container/tree/master), recomendo os dois.

## O que você precisa

Uma máquina Linux (VM serve), `gcc` e a biblioteca do seccomp, que vamos usar mais para o final:

```sh
sudo apt-get install libseccomp-dev
```

Quase tudo aqui precisa rodar como root. Faça isso numa VM se não quiser arriscar sua máquina.

## As quatro peças

- **namespaces**: isolam o que o processo enxerga (árvore de processos, hostname, pontos de montagem, rede).
- **cgroups**: limitam quanto o processo consome (memória, CPU, disco).
- **capabilities**: quebram os poderes do root em pedaços, para que o uid 0 dentro do container não seja tão poderoso quanto o root de verdade.
- **seccomp** e **setrlimit**: restringem quais syscalls podem ser chamadas e alguns limites mais antigos, como número de arquivos abertos.

## Namespaces: o processo que acha que é o PID 1

A syscall `clone` cria um processo filho e aceita flags dizendo em quais namespaces novos ele deve nascer:

```c
#define _GNU_SOURCE
#include <sched.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

#define STACK_SIZE (1024 * 1024)

static int child(void *arg) {
    sethostname("container", 9);
    char *const argv[] = {"/bin/sh", NULL};
    execv(argv[0], argv);
    perror("execv");
    return 1;
}

int main(void) {
    char *stack = malloc(STACK_SIZE);
    int flags = CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS |
                CLONE_NEWIPC | CLONE_NEWNET | SIGCHLD;

    pid_t pid = clone(child, stack + STACK_SIZE, flags, NULL);
    if (pid == -1) {
        perror("clone");
        return 1;
    }

    waitpid(pid, NULL, 0);
    return 0;
}
```

```sh
gcc container.c -o container
sudo ./container
```

Dentro do shell que abrir, rode `hostname` e `echo $$`. O hostname é `container` e o PID é 1, mesmo que lá fora o processo tenha outro número qualquer. Mudar o hostname ali dentro não afeta a máquina, porque estamos num namespace UTS novo.

Tem uma pegadinha: se você rodar `ps`, vai ver todos os processos do host. Isso acontece porque o `ps` lê o `/proc`, e o `/proc` montado ainda é o do host. Para resolver, o container precisa de um sistema de arquivos próprio (um rootfs, que pode ser um Alpine descompactado numa pasta), trocar a raiz com `pivot_root` ou `chroot` e montar um `/proc` novo lá dentro. É mais código do que cabe aqui, mas é exatamente o que os dois projetos que citei fazem.

## Cgroups: colocando um teto

Namespace isola o que o processo vê, mas não impede que ele coma toda a memória da máquina. Para isso existem os cgroups. Na versão 2, que é o padrão nas distros atuais, tudo é arquivo dentro de `/sys/fs/cgroup`:

```sh
sudo mkdir /sys/fs/cgroup/meu-container
echo "100M" | sudo tee /sys/fs/cgroup/meu-container/memory.max
echo "50000 100000" | sudo tee /sys/fs/cgroup/meu-container/cpu.max
echo <PID> | sudo tee /sys/fs/cgroup/meu-container/cgroup.procs
```

A primeira linha limita o grupo a 100 MB de memória. A segunda diz que, a cada 100 ms, o grupo pode usar 50 ms de CPU, ou seja, meio núcleo. A última move o processo para dentro do grupo. No código C é a mesma coisa: abrir esses arquivos e escrever neles antes de liberar o filho para rodar.

Se o `cpu.max` não existir, o controlador de CPU provavelmente não está habilitado no grupo pai. Olhe o `cgroup.subtree_control` do diretório de cima.

## Capabilities: root, mas nem tanto

Root no Linux é na verdade um conjunto de umas quarenta capabilities. `CAP_SYS_ADMIN` deixa montar sistemas de arquivos, `CAP_NET_ADMIN` deixa mexer na rede, e assim por diante. Um container não precisa da maioria delas, então a gente remove do processo antes do `execv`:

```c
#include <sys/prctl.h>
#include <linux/capability.h>

prctl(PR_CAPBSET_DROP, CAP_SYS_ADMIN, 0, 0, 0);
prctl(PR_CAPBSET_DROP, CAP_SYS_MODULE, 0, 0, 0);
prctl(PR_CAPBSET_DROP, CAP_SYS_RAWIO, 0, 0, 0);
```

Isso tira as capabilities do bounding set, então nem o processo nem os filhos dele conseguem recuperá-las depois.

## Seccomp e setrlimit: o último filtro

Mesmo sem capabilities, o processo ainda pode chamar qualquer syscall. O seccomp deixa você montar uma lista do que é permitido ou proibido, e a `libseccomp` torna isso bem menos doloroso:

```c
#include <errno.h>
#include <seccomp.h>

scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_ALLOW);
seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EPERM), SCMP_SYS(mount), 0);
seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EPERM), SCMP_SYS(reboot), 0);
seccomp_rule_add(ctx, SCMP_ACT_ERRNO(EPERM), SCMP_SYS(kexec_load), 0);
seccomp_load(ctx);
seccomp_release(ctx);
```

Compile com `-lseccomp`. Aqui eu usei uma lista negra (libera tudo e bloqueia algumas) porque é mais fácil de entender. Em produção o certo é o contrário: bloquear tudo e liberar só o necessário, que é o que o perfil padrão do Docker faz.

O `setrlimit` é mais antigo que os cgroups e cobre coisas que eles não cobrem, como o número máximo de arquivos abertos:

```c
#include <sys/resource.h>

struct rlimit lim = {.rlim_cur = 64, .rlim_max = 64};
setrlimit(RLIMIT_NOFILE, &lim);
```

## Juntando tudo

A ordem que eu sigo é: `clone` com os namespaces, o pai coloca o filho no cgroup, o filho troca a raiz, monta o `/proc`, remove as capabilities, aplica o seccomp e os rlimits e só então chama `execv`. Seccomp sempre por último, porque depois dele algumas das syscalls que você precisaria para configurar o resto podem estar bloqueadas.

O que sobra para um container "de verdade" é bastante coisa: rede com um par de interfaces `veth`, user namespaces para não precisar de root, imagens em camadas com overlayfs. Mas depois de escrever essas linhas de C, o Docker deixa de parecer mágica. Ele é uma boa camada de conveniência em cima de recursos que o kernel já oferece.

# Referências

- [barco](https://github.com/lucavallin/barco)
- [c_container](https://github.com/nathanagez/c_container/tree/master)
- `man 7 namespaces`, `man 7 cgroups`, `man 7 capabilities`, `man 2 seccomp`
