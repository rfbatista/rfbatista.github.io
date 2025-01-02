+++
title = "Protocol Buffers"
date = "2023-10-02"
tags = ["Golang"]
draft = true
+++

When you are building public APIs the first option that comes to mind to sen data over network is JSON. It's readable most people already know it, but if you have complete control of the clients that will consume this data, you can explore different aproaches to comunnication. That's is where Protocol buffers can shine, is `language-neutral, platform-neutral extensible mechanisms for serializing structured data.`
There are some advantages of using protobufs:
- Fast serialization
- Backward compatibility
- Type safity
- Compact data storage
- Compile the Protobuf in code 

