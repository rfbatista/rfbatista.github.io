+++
title = "Instalando o driver do TP-Link AC600 no Arch Linux"
date = "2025-03-31"
tags = ["linux"]
categories = ["post"]
draft = false
+++

Comprei um adaptador Wi-Fi USB TP-Link AC600, espetei no meu Arch e nada aconteceu. O kernel não vem com driver para o chip Realtek dele, então você precisa instalar um por conta própria. A versão curta: instale o `dkms` e os headers do kernel, depois o `rtl8821au-dkms-git` do AUR. O resto do post é isso com os comandos.

## Passo 1: instalar o DKMS e os headers do kernel

O DKMS recompila módulos de kernel que não fazem parte da árvore oficial toda vez que o kernel atualiza, o que no Arch acontece com frequência. Ele precisa dos headers do kernel que você está rodando:

```sh
sudo pacman -S dkms linux-headers
```

Se você usa outro kernel, instale os headers correspondentes: `linux-lts-headers` para o `linux-lts`, `linux-zen-headers` para o `linux-zen`, e assim por diante. Errar isso é o motivo mais comum de o módulo não compilar sem avisar nada.

Reinicie para garantir que está rodando o kernel a que esses headers pertencem:

```sh
sudo reboot
```

## Passo 2: instalar o driver do AUR

O driver está empacotado como `rtl8821au-dkms-git`. Com um AUR helper como o `yay`:

```sh
yay -S rtl8821au-dkms-git
```

Sem helper, clone e compile na mão:

```sh
git clone https://aur.archlinux.org/rtl8821au-dkms-git.git
cd rtl8821au-dkms-git
makepkg -si
```

## Passo 3: reiniciar e conferir

Reinicie mais uma vez e veja se o módulo carregou e se a interface apareceu:

```sh
lsmod | grep 8821
ip link
```

Deve aparecer uma interface sem fio nova (normalmente começando com `wl`). Daí em diante é conectar do jeito de sempre, com `iwctl`, NetworkManager ou o que você usar.
