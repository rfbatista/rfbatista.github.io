+++
title = "Installing the TP-Link AC600 driver on Arch Linux"
date = "2025-03-31"
tags = ["linux"]
categories = ["post"]
draft = false
+++

I bought a TP-Link AC600 USB Wi-Fi adapter, plugged it into my Arch machine and nothing happened. The kernel doesn't ship a driver for its Realtek chip, so you have to install one yourself. The short version: install `dkms` and the kernel headers, then install `rtl8821au-dkms-git` from the AUR. The rest of this post is the same thing with the commands.

## Step 1: install DKMS and the kernel headers

DKMS rebuilds out-of-tree kernel modules every time your kernel updates, which on Arch is often. It needs the headers for the kernel you are running:

```sh
sudo pacman -S dkms linux-headers
```

If you run a different kernel, install the matching headers instead: `linux-lts-headers` for `linux-lts`, `linux-zen-headers` for `linux-zen`, and so on. Getting this wrong is the most common reason the module silently fails to build.

Reboot so you are sure to be running the kernel those headers belong to:

```sh
sudo reboot
```

## Step 2: install the driver from the AUR

The driver is packaged as `rtl8821au-dkms-git`. With an AUR helper like `yay`:

```sh
yay -S rtl8821au-dkms-git
```

Without a helper, clone and build it by hand:

```sh
git clone https://aur.archlinux.org/rtl8821au-dkms-git.git
cd rtl8821au-dkms-git
makepkg -si
```

## Step 3: reboot and check

Reboot once more, then see whether the module is loaded and the interface showed up:

```sh
lsmod | grep 8821
ip link
```

You should see a new wireless interface (usually something starting with `wl`). From there, connect the way you normally would, with `iwctl`, NetworkManager or whatever you use.
