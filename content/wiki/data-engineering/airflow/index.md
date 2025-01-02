+++
title = "Airflow"
date = "2024-11-20"
tags = ["data-engineering", "airflow"]
draft = false
+++

# Airflow Components

![Airflow architecture](./arch-diag-basic.png)

- Scheduler: keep track of dags
- Workers:

Executors:

- Local
- Celery <-- always on
- Kubernetes <-- on demand
- Celery + Kubernetes


Database
- pgboucer vs max_connections

Pipeline design:

- workflows
- tasks
- inputs
- outputs

Local development:

- spend time setting up your locals
- try to debug in local

# Infrastructure

Kubernetes
- use iac

ci/cd pipeline
- scheduler (mount volume)
- scheduler pull github
- scheduler docker image

Logging


Monitoring and alerting
- monitor resources and events
- prometheus and grafana to monitor
- airflow stats

Resource allocation
- badly written pipeline code can be resource-hungry
- resource constraints can negatively affect the development experience of DAG authores

# Deployment

To avoid the restart of the scheduler and workers every time some one make a change in a DAG, every DAG
ends up in a bucket

# Configuration

## Worker concurrency configuration

For custom jobs that require more resources we can use `KubernetesPodOperator`
that gives runtime isolation this way we can isolate dependencies from airflow image


# Problems

- Library conflicts with airflow
- everything use metadatabase
- tasks use the same airflow Database have some performance inpact based 
- security every single secret is on database
- releases não serão imediatas

# References
- [What we learned after running Airflow on Kubernetes for 2 years](https://medium.com/apache-airflow/what-we-learned-after-running-airflow-on-kubernetes-for-2-years-0537b157acfd)
