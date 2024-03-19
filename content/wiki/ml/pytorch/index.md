+++
title = "PyTorch"
date = "2023-10-15"
tags = ["neural-networks", "machine-learning", "ai", "pytorch"]
draft = false
+++

# How models work in PyTorch

 `nn.Module` - fornece uma base para a criação de modelos personalizados, junto com funcionalidades que ajudam no treinamento.

Duas funções precisam ser definidas:
1. `__init__` definimos as várias camadas que serão utilizadas
2. `forward` definem a sequencias em que as camdas serão utilizadas

# Camadas no PyTorch

- `nn.Conv2d` the convolutional layer
- `nn.BatchNorm2d` normalização da saida da camada de covolução
- `nn.ReLU` função de ativação
- `nn.MaxPool2d` aplica max pooling na saída com o tamanho do kernel
- `nn.Dropout` aplica `dropout` na saida com uma dada probabilidade
- `nn.Linear` camada totalmente conectada
- `nn.Sequential` não é tecnicamente uma camada mas ajuda na combinação de diferentes operações que são parte da mesma etapa

# Treinamento 

