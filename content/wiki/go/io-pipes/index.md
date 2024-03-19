+++
title = "IO Pipes"
date = "2023-10-15"
tags = ["Golang"]
draft = false
+++

With io.Pipe we have a convenient way to connect a writer to a reader, really similar to how channels work

```go
pr, pw := io.Pipe()
```

# References

[justforfunc #19: mastering io.Pipes](https://www.youtube.com/watch?v=LHZ2CAZE6Gs&t=102s&ab_channel=justforfunc%3AProgramminginGo)
