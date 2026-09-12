+++
title = "Why I'm building a local voice assistant in Portuguese"
date = "2026-08-06"
tags = ["local-ai", "voice", "pt-br", "privacy"]
categories = ["build-log"]
draft = true
+++

<!-- EXAMPLE OF A TRANSLATED POST.
     Pattern: the same folder as the PT-BR post, file named index.en.md.
     Hugo links both versions automatically (language switcher + hreflang).
     This is the English version of the PT-BR draft; it stays draft = true
     until the original is published. -->

There is a microphone switched on in the living room of millions of Brazilian homes. Amazon itself celebrates it: [29 million devices connected to Alexa in Brazil, 15 million in use every month](https://www.aboutamazon.com.br/noticias/dispositivos/alexa-em-2025-a-assistente-de-voz-cada-vez-mais-presente-no-dia-a-dia-dos-brasileiros). Whoever bought one controls neither what it hears nor where the audio goes. I think it can be done differently, and this article is the thesis of what I'm researching and building.

## The problem: convenience with an invisible wire

The deal looks simple: you speak, the little box answers. What isn't on the box is that the whole architecture depends on the cloud of a company whose business is not selling little boxes. The hardware is cheap because it is not the product.

Two episodes show how long the wire is. In 2023, Amazon reached a [US$ 25 million settlement with the FTC](https://www.ftc.gov/news-events/news/press-releases/2023/05/ftc-doj-charge-amazon-violating-childrens-privacy-law-keeping-kids-alexa-voice-recordings-forever), accused of keeping children's voice recordings forever. In March 2025, it [removed the "don't send voice recordings" option](https://techcrunch.com/2025/03/15/amazons-echo-will-send-all-voice-recordings-to-the-cloud-starting-march-28) from Echo devices: since then, all audio goes to the cloud, no alternative. The privacy setting that existed yesterday is gone today, because the decision was never yours.

Privacy in the terms of service is not privacy. Real privacy is architecture: audio that never leaves your home cannot be stored by anyone.

## Why Portuguese

Wake word, speech recognition and speech synthesis treat Brazilian Portuguese as a second-class citizen. Open models are trained mostly on English, and when one of them claims to "support Portuguese", almost nobody has measured what that means with a northeastern accent, music in the background and a two-dollar microphone.

That's the hole I want to dig in. The bet is not a mediocre bilingual assistant; it's excellence in PT-BR: measuring what Whisper, open TTS models and wake-word detectors deliver in Portuguese on cheap hardware, and publishing the numbers with scripts so anyone can reproduce them. If the result is "not yet", that becomes an article too.

## Why local

Local-first is an engineering choice, not marketing. Structural privacy: what runs at home doesn't depend on this quarter's data policy. Latency: the round trip to the cloud costs hundreds of milliseconds a local answer doesn't pay. And sovereignty: Brazil's LGPD exists because personal data processed by third parties is a risk, and the audio of your living room is the most personal data there is.

The technical question that interests me: what already runs today on a Raspberry Pi 5 or an ESP32-S3, and what doesn't yet? That frontier moves every quarter, and mapping it in Portuguese is a good part of what I'll publish here.

## Lessons from those who tried

Mycroft, the most serious attempt at an open assistant, [shut down in 2023](https://www.theregister.com/2023/02/13/linux_ai_assistant_killed_off/) without delivering its Kickstarter rewards, drained by a patent lawsuit and by a business that didn't add up: selling hardware against subsidized boxes, with no recurring revenue. Lesson: validate demand before manufacturing anything. That's why this blog exists before any product.

The [Home Assistant Voice Preview Edition](https://www.home-assistant.io/blog/2024/12/19/voice-preview-edition-the-era-of-open-voice/), at US$ 59, proved there is real demand for local voice. But it requires a Home Assistant server at home, fully local processing calls for an Intel N100 or better, and the team itself admits their cloud is still more accurate for most languages. It's a product for home-automation enthusiasts. The space I care about is what's left: a finished-product experience, no server to administer, with PT-BR as the first language rather than a checklist item.

## What I'm doing about it

As a personal project, I'm prototyping a voice assistant that runs 100% at home: wake word, speech recognition and synthesis in Portuguese, on off-the-shelf hardware. It's still research, not a product. I have no date, I'm not selling anything, and some of my hypotheses will turn out to be wrong.

The commitment is to research in public: every benchmark ships with the script and config for you to reproduce it, every architecture decision becomes a build-log post, failures included.

## Follow along

The series continues under [writing](/en/posts/) on this site. If you work with voice, run AI at home, or are just tired of talking to other people's clouds, write to me: contato@renandonato.com.br.
