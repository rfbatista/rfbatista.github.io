+++
title = "Kubernetes"
tags = ["devops"]
categories = ["post"]
draft = false
+++

## Pods

Is the smallest building block in kubernetes. A pod is made up of one or more container that share network and storage resources. Pods are incorporated in a higher level abstraction like ReplicaSet.

## ReplicaSet
Are used to keep fixed number of identical pods. You need it if you want to create a orchestration behavior.

## Deployments
Is a resource that manage pods and ReplicaSets. The main job is to maintain the state that is configured in its manifest

## StatefulSets

Resource to manage stateful applications like MongoDB, Postgres and etcd. Like deployments it can manage the state of a pod in a manifest.

## Services

Used to expose application in a pod withing the kubernetes or the internet. There are the following services types:
- ClusterIP
- Headless
- NodePort: Expose the service in the node ip address and port
- LoadBalacer: Expose the service externally
- ExternalName


## Volume

Basically a directory or file that all container in a pod can access. If the entire POD is killed the Volume and its data will be removed. If needed to persist data use Persistent Volume. A PV is a resource in a cluster just like a node. If running in AWS you can use Amazon Elastic Block Storage (Amazon EBS)

## Secrets

## ConfigMaps

## Namespaces

It provides a logical separation of resources. If you dont specify while creating a resource it will be named `default`
