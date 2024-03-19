+++
title = "Database from scratch"
date = "2024-02-06"
tags = ["golang", "database"]
draft = false
+++

1. Persistence: como não perder dados
2. Indexing: como consultar dados
3. Concurrency: como lidar com multiplos clientes

# Persistence

# Indexing
Existem dois tipos de queries:
1. Analytical (OLAP): Geralmente envolvem um grande numéro de dados, com agregação, agrupamento, or joins.
2. Transactional (OLTP): consultas que envolvem apenas uma pequena parte dos dados.

## Transactional (OLTP)
