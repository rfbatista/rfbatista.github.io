+++
title = "NeuralSearchX: Serving a Multi-billion-parameter Reranker for Multilingual Metasearch at a Low Cost"
date = "2024-02-03"
tags = ["recomendation"]
draft = false
+++

## Multistage ranking

# Our solution

A multi-stage metasearcgh engine, stage:
1. candidade retrieval step using federated search over web search engines along with sparse and dense retrieval from private collection
2. reranking step based on previously selected documents with a neural model, score based on relavancy to a query
3. the best documents are sent to a highlighter model, that select s the most relevant sentecences from each document

## 1st stage candidates retrieval
Use sparse and dense retrieval methods (sparce to find exact matches and dense handles semantical meaning)
Before indexing we split the contents of long documents over multiple windows
windows of 150 words with stride of 75 words

## 2st stage reranking
merge all candidates in a single list and then rank such documents
mMiniLM reranker
mMARCO
MS MARCO
mT5

## 3st highlighting  (same model as reranking)
with results ordered by relevance, take the first ten ranked documents and performs a highlighting step
take long text and select the most important senteces to show


# Referece
[https://arxiv.org/pdf/2210.14837](https://arxiv.org/pdf/2210.14837)
[https://dl.acm.org/doi/10.1145/3447548.3469053](https://dl.acm.org/doi/10.1145/3447548.3469053)
