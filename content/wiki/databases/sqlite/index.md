+++
title = "SQLite"
date = "2024-10-06"
tags = ["databases"]
draft = false
+++

SQLIte is faster than filesystem


```
PRAGMA journal_mode = WAL;
PRAGMA busy_timeout = 5000;
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = 1000000000;
PRAGMA foreign_keys = true;
PRAGMA temp_store = memory;
```

`PRAGMA journal_mode = WAL;` write and reader don't block

`PRAGMA synchronous = NORMAL;` 

`PRAGMA busy_timeout = 5000;` avoid `SQLITE_BUSY` errors to happen


Use IMMEDIATE transactions so sqlite respest the busy_timeout. It can be configure at pool level in GO `mydb.db?_txlock=immediate`
# SQL Index Storage

# Checkpoint Starvation

# References

- [https://www.youtube.com/watch?v=ZSKLA81tBis](https://www.youtube.com/watch?v=ZSKLA81tBis)
- [https://kerkour.com/sqlite-for-servers](https://kerkour.com/sqlite-for-servers)
- [https://github.com/mattn/go-sqlite3/issues/1179#issuecomment-1638083995](https://github.com/mattn/go-sqlite3/issues/1179#issuecomment-1638083995)
- [https://use.expensify.com/blog/scaling-sqlite-to-4m-qps-on-a-single-server](https://use.expensify.com/blog/scaling-sqlite-to-4m-qps-on-a-single-server)
