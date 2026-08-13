+++
title = "Por que estou construindo um assistente de voz local em português"
date = "2026-08-06"
tags = ["ia-local", "voz", "pt-br", "privacidade"]
categories = ["diario"]
draft = true
+++

<!-- RASCUNHO (versão curta, <800 palavras) para revisão do Renan.
     Fontes verificadas em 06/08/2026. Trocar draft = false ao publicar. -->

Existe um microfone ligado na sala de milhões de casas brasileiras. A própria Amazon comemora: [29 milhões de dispositivos conectados à Alexa no Brasil, 15 milhões em uso todo mês](https://www.aboutamazon.com.br/noticias/dispositivos/alexa-em-2025-a-assistente-de-voz-cada-vez-mais-presente-no-dia-a-dia-dos-brasileiros). Quem comprou um não controla o que ele escuta nem para onde o áudio vai. Eu acho que dá para fazer diferente, e este artigo é a tese do que estou pesquisando e construindo.

## O problema: conveniência com fio invisível

O trato parece simples: você fala, a caixinha responde. O que não aparece na caixa é que a arquitetura inteira depende da nuvem de uma empresa cujo negócio não é vender caixinhas. O hardware é barato porque ele não é o produto.

Dois episódios mostram o tamanho do fio. Em 2023, a Amazon fechou um [acordo de US$ 25 milhões com o FTC](https://www.ftc.gov/news-events/news/press-releases/2023/05/ftc-doj-charge-amazon-violating-childrens-privacy-law-keeping-kids-alexa-voice-recordings-forever), acusada de guardar para sempre gravações de voz de crianças. Em março de 2025, [desligou a opção "não enviar gravações de voz"](https://techcrunch.com/2025/03/15/amazons-echo-will-send-all-voice-recordings-to-the-cloud-starting-march-28) dos Echo: desde então, todo áudio vai para a nuvem, sem alternativa. A configuração de privacidade que existia ontem sumiu hoje, porque a decisão nunca foi sua.

Privacidade nos termos de serviço não é privacidade. Privacidade de verdade é arquitetura: áudio que não sai da sua casa não pode ser guardado por ninguém.

## Por que em português

Wake word, reconhecimento de fala e síntese de voz tratam o português brasileiro como cidadão de segunda classe. Os modelos abertos são treinados majoritariamente em inglês, e quando um deles diz que "suporta português", quase nunca alguém mediu o que isso significa com sotaque nordestino, música no fundo e um microfone de dois dólares.

É nesse buraco que quero cavar. A aposta não é um assistente bilíngue mediano, é excelência em PT-BR: medir o que Whisper, os TTS abertos e os detectores de wake word entregam em português rodando em hardware barato, e publicar os números com scripts para qualquer um reproduzir. Se o resultado for "ainda não dá", isso também vira artigo.

## Por que local

Local-first é escolha de engenharia, não marketing. Privacidade estrutural: o que roda em casa não depende da política de dados do trimestre. Latência: o caminho até a nuvem e de volta custa centenas de milissegundos que uma resposta local não paga. E soberania: a LGPD existe porque dado pessoal processado por terceiros é risco, e o áudio da sua sala é o dado mais pessoal que existe.

A pergunta técnica que me interessa: o que já roda hoje num Raspberry Pi 5 ou num ESP32-S3, e o que ainda não roda? Essa fronteira se move a cada trimestre, e mapeá-la em português é boa parte do que vou publicar aqui.

## As lições de quem já tentou

O Mycroft, a tentativa mais séria de assistente aberto, [fechou em 2023](https://www.theregister.com/2023/02/13/linux_ai_assistant_killed_off/) sem entregar as recompensas do Kickstarter, drenado por um processo de patente e por uma conta que não fechava: vender hardware competindo com caixinhas subsidiadas, sem receita recorrente. Lição: validar demanda antes de fabricar qualquer coisa. É por isso que este blog existe antes de qualquer produto.

Já o [Home Assistant Voice Preview Edition](https://www.home-assistant.io/blog/2024/12/19/voice-preview-edition-the-era-of-open-voice/), de US$ 59, provou que existe demanda real por voz local. Mas exige um servidor Home Assistant em casa, o processamento totalmente local pede um Intel N100 ou melhor, e a própria equipe admite que a nuvem deles ainda é mais precisa para a maioria das línguas. É produto para entusiasta de automação. O espaço que me interessa é o que sobra: experiência de produto acabado, sem servidor para administrar, com PT-BR como primeira língua e não como item de checklist.

## O que estou fazendo a respeito

Estou prototipando, como projeto pessoal, um assistente de voz que roda 100% em casa: wake word, reconhecimento de fala e síntese em português, em hardware de prateleira. Ainda é pesquisa, não produto. Não tenho data, não estou vendendo nada, e algumas das minhas hipóteses vão se provar erradas.

O compromisso é pesquisar em público: cada benchmark sai com script e config para você reproduzir, cada decisão de arquitetura vira post do diário de construção, fracassos incluídos.

## Acompanhe

A série continua nos [escritos](/posts/) deste site. Se você trabalha com voz, roda IA em casa ou só está cansado de falar com a nuvem dos outros, me escreva: contato@renandonato.com.br.
