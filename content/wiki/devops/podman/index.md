+++
title = "Podman"
tags = ["devops", "podman"]
categories = ["post"]
draft = false
+++

# What are containers

Technologies that allow you to package and isolage application

# Container orchestation

- kubernetes
- openshift
- docker swarm

# What is a pod

A group of one or more containers with shared storage and network resources and specification for how to run the containers.
By default a pod has a infra container

## Why use pods

- shared resources: containers in the same pod will share same resources and local network
- communications: can easily communicate with others in the same pod
- scalability: as demand for services increase you can deploy additional pods

# What is podman

- no daemon
- kubernetesinteroperability
- create systemd containers with podman
- interoperability with docker

- local repository is in `/var/lib/containers/` or `~/.local/share/containers/`
- podman talks directly to `runc`

You can configure a local container registry

# What is skopeo

- CLI to perform operation on container images and image repositories

# Whats is buildah

- CLI for building open caontainer initiative-compatibility

# Installing podman


## Installation in Manjaro

 [https://computingforgeeks.com/how-to-install-podman-on-arch-linux-manjaro/](https://computingforgeeks.com/how-to-install-podman-on-arch-linux-manjaro/)

## Configuration

Configuration file are located at `/etc/containers/`

## Managing images

### podman
- podman image
- podman images
- podman inspect
- podman login/logout
- podman pull/push
- podman rmi
- podman search
- podman tag/untag

Add `--help` in any command to get more information

### skopeo
- skopeo inspect
- skopeo login/logout
- skopeo copy
- skopeo sync
- skopeo list-tags

# References

2 [Hands-on with Podman Containers on Linux]()
