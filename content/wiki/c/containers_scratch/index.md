+++
title = "Containers from scratch"
date = "2024-10-12"
tags = []
categories = []
draft = false
+++

- namespaces: kernel groups accessed by specific processes. There are different kind of namespaces
- capabilities: set limits to uid 0
- cgroups: mechanism to limit usage of memory, disk, cpu-time and other resources.
- setrlimit: similar mechanism to cgroups but is older and can do somethings cgroups cant.


need to isntall sudo apt-get install libseccomp-dev

# References
- https://github.com/nathanagez/c_container/tree/master
- https://github.com/lucavallin/barco
