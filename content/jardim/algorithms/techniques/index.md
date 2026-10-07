+++
title = "Algorithms Tecniques"
date = "2024-04-09"
tags = ["algorithms"]
draft = false
aliases = ["/wiki/algorithms/techniques/"]
lastmod = "2025-01-02"
+++

## 2 pointers approachs
i points to the last unique element, j iterates through the array
```go
i := 0
for j := 1; j < len(nums); j++ {
    if nums[j] != nums[i] {
        i++
        nums[i] = nums[j]
    }
}
```
