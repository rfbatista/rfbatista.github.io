+++
title = "Kubernetes"
tags = ["devops"]
categories = ["post"]
draft = false
+++

Kubernetes is like an operating system for computer clusters. It frees developers from implementation of infrastructure mechanisms like:
- service discovery
- horizontal scaling
- load balancing
- self-healing
- leader election

Kubernetes clusters are divided in **Control Plane** and **Workload Plane** or **Data Plane**


# Benefits of using kubernetes

- self service deployment of applications
- reducing costs via better infrastructure utilization (tightly applications together)
- automatically adjusting to changing Load: in cloud you can even provide more nodes through the cloud providers api
- keeping application running smoothly
- simplifying application development

# Control Plane Components

- scheduler: what node should run instance of an application
- controllers: each controller have different tasks
- api server: components that run in worker node and developer/operators communicate with this api
- etcd: distributed datastore, the server itself is stateless

# Worker node components

- kubelet: node agent manages applications running on this node and talks with the api server
- container runtime: typically docker
- kubeproxy: creates a virtually load balancer for each application that needs it

# Modern Application Architecture

- Cloud Native
- Modular
- Microservice Base
- Scalability
- Reliability
- Resilience

# Requirements for containers

- Packaging
- Versioning
- Isolation
- Fast startup
- Low overhead

# Requirements for Orchestration

- Clustering
- Discovery
- Configuration: allowing to reconfigure without a rebuild and redeploy
- Access control 
- Load balancing
- Monitoring: identify failed Microservice instaces
- Resilience: Automatically recover from failures


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


# Control Plane

- kublet
- kube-proxy
- container runtime
- etcd a key value distributed database

## API Server

- API Server Aggregation (Service Catalog, etc)
- Custom Resource Definition

### Open Service Broker

- Connect applications to hosted service and partner services using Kubernetes API

## Controller Manager

### Controller/Operator pattern

Examples:
- Prometheus Operator

## Scheduler

## Kubelet
