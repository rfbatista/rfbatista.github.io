+++
title = "Choosing your GPU for inference"
aliases = ["/lists/"]
tags = ["machine-learning"]
draft = false

+++

When defining and benchmarking an inference workload, two numbers end up
explaining most of what you see: ISL (input sequence length) and OSL (output
sequence length). They matter because an LLM request runs in two very different
phases, and each one stresses a different part of the GPU.

Prefill processes the whole prompt at once. It is driven by ISL and is
compute-bound. Decode generates the answer one token at a time. It is driven by
OSL and is memory-bandwidth-bound. Once you know which phase dominates your
workload, you know which GPU spec to look at first.

## ISL (Input Sequence Length)

ISL is the number of tokens in the model's input: system prompt, chat history,
retrieved documents and the user's message. It drives the prefill cost, because
every input token has to go through the whole model before the first output
token can be produced.

Two parts of that work grow with ISL, at different rates:

1. The dense layers grow linearly. Each token passes through every weight matrix
   (the QKV and output projections and the MLP). That costs about 2 FLOPs per
   parameter per token, so for a model with `N` parameters prefill costs roughly
   `2 · N · ISL` FLOPs. Double the prompt and you double the work.
2. Attention grows quadratically. In every layer, each token computes a score
   against every earlier token, so attention costs on the order of `ISL² · d`
   FLOPs per layer (`d` is the hidden size). For short prompts this is noise.
   Per token, the dense layers cost about `24 · d²` FLOPs per layer and
   attention about `2–4 · ISL · d`, so the two meet when ISL is around 6 to 12
   times `d`. For a model with `d = 4096` that is somewhere in the tens of
   thousands of tokens, and past that point longer prompts get
   disproportionately more expensive.

Prefill handles all ISL tokens in parallel as large matrix multiplications. That
keeps the GPU's compute units saturated, so prefill is compute-bound and time to
first token (TTFT) tracks FLOPs closely.

As an example, Llama-3-8B with an 8k-token prompt needs about
`2 × 8e9 × 8000 ≈ 1.3e14` FLOPs. An H100 delivers roughly 990 TFLOPS of dense
BF16, so at a realistic 50% utilization you wait about 0.26 s before the first
token appears.

## OSL (Output Sequence Length)

OSL is the number of tokens the model generates, and it drives the decode cost.
Decode is autoregressive: token `t+1` depends on token `t`, so the model has to
run OSL forward passes, one after another.

### Why decode is memory-bandwidth-bound

At batch size 1, each decode step multiplies every weight matrix by a single
vector. A model with `N` parameters in FP16 reads `2N` bytes from memory and
does about `2N` FLOPs, roughly 1 FLOP per byte loaded. An H100 can do about 990
TFLOPS but only moves about 3.35 TB/s from HBM, so it needs around 300 FLOPs per
byte to keep its compute units busy. Decode sits about 300× below that, and the
GPU spends most of each step waiting on memory.

Step time is therefore roughly bytes moved divided by memory bandwidth. For
Llama-3-8B in FP16 (16 GB of weights) on an H100:

```
16 GB / 3.35 TB/s ≈ 4.8 ms per token  →  ~200 tokens/s ceiling for one request
```

Adding FLOPS won't raise that ceiling. You need more bandwidth or fewer bytes
per step.

### The KV cache keeps growing

Each step also has to read the KV cache, which holds the keys and values of
every earlier token. At step `t` that is `ISL + t` tokens of cache, and it grows
with every token generated.

Llama-3-8B has 32 layers, 8 KV heads and head dimension 128. In FP16 that is
`2 × 32 × 8 × 128 × 2 bytes ≈ 128 KiB` per token, so an 8k-token context takes
about 1 GiB per request. Summed over the whole generation, the cache reads come
to about `OSL · ISL + OSL² / 2` token-reads, which is quadratic in OSL, so very
long generations get slower per token as they go.

### Batching and the KV cache

Serving `B` requests together turns the weight reads into matrix-matrix work:
one read of the weights serves `B` tokens, which is how inference servers get
decent utilization out of decode. The KV cache doesn't amortize that way,
because each request has its own. As batches grow, the bottleneck moves from
weight reads to KV reads, and memory capacity starts to cap how many requests
fit at once. A long OSL makes each cache bigger and keeps it in memory longer,
which lowers concurrency for everyone.

This is also why output tokens usually cost more than input tokens. An input
token is processed in parallel at high utilization. An output token occupies one
sequential, poorly utilized step, and its request holds KV memory for the whole
generation.

For decode, watch time per output token (TPOT, also called inter-token latency)
and total throughput in tokens/s.

## Looking at your use case

You usually know your workload's ISL/OSL shape before you pick hardware, and
that shape tells you which phase dominates:

| Workload                 | Typical ISL           | Typical OSL     | Dominant phase          |
| ------------------------ | --------------------- | --------------- | ----------------------- |
| Classification / tagging | Medium to long        | A few tokens    | Prefill (compute)       |
| Summarization            | Long                  | Short           | Prefill (compute)       |
| RAG / document Q&A       | Long (retrieved docs) | Short to medium | Prefill (compute)       |
| Chat (first turns)       | Short                 | Medium to long  | Decode (bandwidth)      |
| Chat (long sessions)     | Grows every turn      | Medium          | Mixed                   |
| Reasoning models         | Short to medium       | Very long       | Decode (bandwidth)      |
| Code completion          | Long (file context)   | Short           | Prefill, TTFT-sensitive |

Chat starts decode-heavy, but the history is resent every turn, so long
conversations drift toward prefill-heavy (prefix caching helps a lot here).
Reasoning models that "think" before answering can generate thousands of tokens
per request, which puts them among the most decode-heavy workloads you can run.

## Matching the GPU to the workload

For prefill-heavy work, compare dense TFLOPS at the precision you will serve
(BF16 or FP8). That sets TTFT and how many prompts per second you can ingest.
For decode-heavy work, compare HBM bandwidth, which sets TPOT. For long contexts
or high concurrency, look at memory capacity: whatever is left after the weights
becomes KV cache, and that caps your batch size.

Some reference points (dense BF16, without sparsity; check the vendor datasheet
for the exact SKU you are buying):

| GPU      | BF16 dense    | Memory | Bandwidth | FLOPs per byte | Llama-3-8B decode ceiling\* |
| -------- | ------------- | ------ | --------- | -------------- | --------------------------- |
| L40S     | ~362 TFLOPS   | 48 GB  | 0.86 TB/s | ~420           | ~55 tok/s                   |
| H100 SXM | ~990 TFLOPS   | 80 GB  | 3.35 TB/s | ~295           | ~210 tok/s                  |
| H200     | ~990 TFLOPS   | 141 GB | 4.8 TB/s  | ~205           | ~300 tok/s                  |
| MI300X   | ~1,300 TFLOPS | 192 GB | 5.3 TB/s  | ~245           | ~330 tok/s                  |
| B200     | ~2,250 TFLOPS | 180 GB | 8 TB/s    | ~280           | ~500 tok/s                  |

\* Single request, FP16 weights, `16 GB / bandwidth`, ignoring KV reads and
overhead. Real numbers are lower, but the ratios between cards hold.

H100 vs H200 shows the split most clearly. They have the same compute, so
prefill runs about the same on both. The H200 has about 43% more bandwidth and
76% more memory, though, so decode-heavy and long-context workloads run
noticeably better on it.

Memory size also sets concurrency. With Llama-3-8B in FP16, an H100 has about 64
GB left after the weights, enough for roughly 60 concurrent 8k-token requests,
and an H200 fits about twice that. If your bottleneck is how many users you can
serve at once, capacity can matter more than speed.

Cheaper cards can still make sense for prefill-heavy work. The L40S has poor
bandwidth for decode, but for classification or embedding-style jobs with tiny
outputs it can be very cost-effective per token.

Precision changes both sides. FP8 or INT4 weights cut the bytes per decode step,
so you get more tokens/s on the same card, and on hardware that supports them
they also raise usable FLOPS for prefill.

## Benchmark with your own ISL/OSL

Public benchmarks usually report a single ISL/OSL pair, often 1k/1k, which may
look nothing like your traffic. Before deciding, run a few pairs that bracket
your workload, for example:

- `8000 / 256` for a prefill-heavy shape
- `256 / 4000` for a decode-heavy shape
- your real production distribution, if you have logs

For each one, measure TTFT, TPOT and throughput at the concurrency you expect,
then compare cost per million tokens rather than raw speed alone.
