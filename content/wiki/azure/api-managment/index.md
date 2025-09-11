+++
title = "API Managment"
date = "2025-01-07"
tags = ["api", "azure"]
draft = false
+++

# Load balancing Azure OpenAI

Normal scenario:

- token and model quota is available
- api return 200
  Throttled scenario:
- quota limits is applied
- api managment retry to a different resource

# References

[https://learn.microsoft.com/en-us/azure/developer/python/get-started-app-chat-scaling-with-azure-api-management?tabs=github-codespaces%2Cinitial-deployment](https://learn.microsoft.com/en-us/azure/developer/python/get-started-app-chat-scaling-with-azure-api-management?tabs=github-codespaces%2Cinitial-deployment)
