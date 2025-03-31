+++
title = "Installing tp-link ac 600 driver in arch linux"
date = "2025-03-31"
tags = ["linux"]
categories = ["post"]
draft = false
+++

First install dkms and linux-headers then restart.

Then from the AUR install rtl8821au-dkms-git then restart

If you've recently purchased a TP-Link AC600 wireless adapter and are trying to get it working on Arch Linux, you'll need to install the appropriate drivers. Here's a step-by-step guide to setting it up.

# Prerequisites

Before installing the driver, make sure you have dkms and linux-headers installed. These are essential for compiling and managing kernel modules.

## Step 1: Install DKMS and Linux Headers

Open a terminal and run the following command:

```
sudo pacman -S dkms linux-headers
```

Once the installation is complete, restart your system:

```
sudo reboot
```

## Step 2: Install the Driver from AUR

The driver for the TP-Link AC600 adapter is available in the Arch User Repository (AUR) under the package rtl8821au-dkms-git. To install it, use an AUR helper like yay:

```
yay -S rtl8821au-dkms-git
```

Alternatively, if you don’t have an AUR helper installed, you can manually clone and build the package:

```
git clone https://aur.archlinux.org/rtl8821au-dkms-git.git
cd rtl8821au-dkms-git
makepkg -si
```

## Step 3: Restart Your System

Once the driver is installed, reboot your system to apply the changes:

```
sudo reboot
```

Step 4: Verify the Installation

After restarting, check if the adapter is recognized by running:

```
ip link
```

or

```
lsmod | grep 8821
```

If everything is set up correctly, your TP-Link AC600 adapter should now be working on Arch Linux.
