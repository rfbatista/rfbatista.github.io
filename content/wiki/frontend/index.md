+++
title = "Frontend Development"
date = "2024-02-03"
tags = ["frontend"]
draft = false
+++

# Rendering patterns

- Static rendering - HTML are rendenred at build time, that way you can cache in CDN
- ISR
- SSR
- CSR

# Core Web Vitals

- TTFB
- FCP
- TTI
- FID
- CLS
- LCP

# Architecture

Application architecture:

1. component model
2. rendering and loading
3. routing and transitions
4. data/state management

## Rendering and loading

Bigger javascript bundle will always means a slower performance
Serverside rendering have a faster FTP

SSR:

1. Performance
2. SEO
3. Data fetching

Tecniques:

- SSR
- SSR with hydration
- SSR with hydration and streaming (TTFB improvement) beneficial for large websites
- Progressive hydration
- Pre-rendering
- Client side

- [Webframework performance report](https://astro.build/blog/2023-web-framework-performance-report/)
- [Rendering on the web](https://web.dev/articles/rendering-on-the-web?hl=pt-br)
- [Rendering on the Web: Performance Implications of Application Architecture (Google I/O ’19)
  ](https://www.youtube.com/watch?v=k-A2VfuUROg)
- [How to structure frontend applications](https://michalzalecki.com/elegant-frontend-architecture/)
- [About JIRA's frontend architecture](https://www.youtube.com/watch?v=CbHETl96qOk)
- [Building resilient frontend architecture](https://www.youtube.com/watch?v=TqfbAXCCVwE)
- [The Standard - User Interfaces](https://github.com/hassanhabib/The-Standard/blob/master/3.%20Exposers/3.2%20User%20Interfaces/3.2%20User%20Interfaces.md#32000-progress-loading)
- [The twilight zone: what happens before hydration](https://www.youtube.com/watch?v=PGLwRv64RzM)

## Data state management

### Web workers

# Libs

- https://github.com/developit/mitt

# Tools

- Dependency validation e visualization - [https://www.npmjs.com/package/dependency-cruiser](https://www.npmjs.com/package/dependency-cruiser)

# References

- [Frontend infrastructure](https://github.com/imteekay/frontend-infrastructure)
- [Webperformance research](https://github.com/imteekay/web-performance-research)
- Frontend challenges](https://github.com/imteekay/frontend-challenges)
- [Crafting frontend](https://github.com/imteekay/crafting-frontend)
- [React testing library recipes](https://github.com/imteekay/react-testing-library-recipes)
- [https://ui.dev/why-react-query](https://ui.dev/why-react-query)
