+++
title = "CosmosDB"
date = "2025-01-07"
tags = ["databases", "azure"]
draft = false
+++


Whats is NoSQL

- distributed
- schemafree

There is a `local emulator`
 w

- Primary key and secondary key are used to rotate access keys without loosing connection access

# Container


# Documents

zip_code

# Management 

- Azure portal
- Azure CLI
- PowerShell
- ARM Templates
- Bicep Templates
- Rest API

# Automatic indexing

The hierarchy of a json tree, is flatened as a list of keys and values:

``` 
/locations/0/contry: Germany
/locations/1/contry: Berlin
/exports: Examples
```

This structure is automatically indexed. But you can finetune with a custom policy

# APIs and Data Model


Non relational:
- NoSQL API
- MongoDB API
- Table API: key-value
- Gremlin API: Vertices and edges
- Cassandra API: columnar

All offer have:
1. global distribution
2. horizontal partitioning 
3. automatic indexing 
4. provisioned throughput

All data are stored as ARS (ATOM RECORD SEQUENCE)

It have relational with PostgreSQL API

# Container

## Container throughput
Container throughput determines the number of request units available per second, and the partition key determines how documents are partitioned within the container. These are the two key characteristics of a container, so that you can create multiple containers within a database, each with their own particular throughput and partitioning needs.

# Measuring performance

- Latency: how fast is the response for a given request
- Throughput: how many requests can be served within a specified period of time

# Requests units 

Throughput currency is a blend of memory, cpu and IOPs. Request units are deterministics

# Throughputs offer

- Provisioned throughput: you set a number o RUs
- Provisioned throughput autoscale: reserve maximum of RUs with scale up and down automatically, never prvision less then 10% of the maximum
- Servless: best suited for spike and most idle containers

You can provide throughput per container or database

## Throughput error

Exceeding reserverd throughput limits will give a HTTP 429 error 

## Burst capacity

Accumulate idle capacity over a rolling five-minute period to be spend on spikes

Limitations: physical parition with less than 3000 RU/s of throughput

# Cost and pricing

- throughput: request units
Read item: 1 RU
SQL query: ~2.8 RU
Write: ~7-9 RU
provisioned: 
0.008 /hr for 100 RU/sec per region
Minimum 400 RU ~ USD 23.424

autoscale: 
0.012 /hr for 100 RU/sec per region
Minimum 100 RU to 1000 RU/sec ~ USD 35.136

servless:
USD 0.25 per 1 million RUs

- storage
consumption based SSD storage, $0.25 for 1GB per month per region

# Achieving elastic scale

A container is a single logic resource composed of multiple physical partitions that is created by CosmosDB behind the scenes on multiple servers

## Logical partitions

partition key determine how documents are grouped in logical partitions
Every document have a maximum size of 2MB
Partitions have a maximum size of 2GB

## Avoid hot partitions

Partitions key should have similar number of documents and access to it.
The best partition key gives uniform storage and throuputh between physical partitions

## Cross partitions query

Queries that need to be run across the entire cluster and not just in one logical partition

## Transactions

Transactions are scoped by logical partition

## Syntetic partition

## Hierarchical partition

You can use multiple keys do create subgroups in a logical partition, in that way making the logical partition capable of beeing in more than one physical partitiona
so comporting more than 20Gb and avoiding cross cluster queries.

# Monitor and troubleshooting
