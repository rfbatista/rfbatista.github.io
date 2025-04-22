+++
title = "Networking Basics"
date = "2025-01-02"
tags = ["network"]
draft = false
+++

Two or more computers connected together
DNS (Domain Name System)

# Types of netwok
- LAN
- WAN


# Topologies
- Ring
- Point-to-point
- Mesh
- Star
- BUS
- Tree
- HYbrid

# Building blocks
- Devices (MAC Address)
- Connections - type of connection Ex.: wireless
- Switches - connect various devices
- Routers
- Network servers

# OSI Model

# Network Services

DNS, email, internet chat, printer sharing...

# IP Addresses
- IPv4
- IPv6
- NAT
    public and private 
    - network address translation
    - private LAN
    - public WAN

## IPv4

```
192.168.2.14:80
```
- 192.168.2 = network id
- .14 = host id
- 80 = port

## IPv6
Written in hexadecimal
```
2001:0db8:3a4d:0016:0000:0000:1c2f:1a3b
```
- 2001:0db8:3a4d = site prefix
- 0016 = subnet id
- 0000:0000:1c2f:1a3b = interface id

## Subnet

octet octet octet octet

- class A = 16 million hosts
- class B = 65535 hosts
- class C = 254 hosts

# DNS
- Domain name
- DNS Records
- Recursive Name Server
- Root Name Server
- TLD Name Server
- Authoritative Name Server

## How a DNS query work

example.com
1. ask recursive name server
2. recursive server ask root name server
3. i dont know but can find in TLD name server for .com
4. i dont know but you can find in authoritative name server for example.com
5. ask authoritative name server for example.com and it returns the ip
6. recursive name server pass the ip to the client and remember the ip for sometime
7. the client receive the ip and remember for some time

# Routing
Routing is moving data from one network to another

- routing tables
- routing protocols
- static routes
- dynamic routes


# Network port
Associated with an ip address, there are 65535 ports

# Finding your network information
![]('./ip.png')
- IP address information: `ip address show`, legacy: `ifconfig`
- Routes: `route` and `netstat`
- dns: `nmcli`, view `/etc/resolv.conf`

# Finding remote network

- remote ip address information: `dig`
- routing: `traceroute`
