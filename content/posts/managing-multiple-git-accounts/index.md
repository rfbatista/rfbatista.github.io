+++
title = "Managing multiple git accounts"
draft = true
+++

Para listar as chaves ssh existentes use o comando:
``` 
ls $HOME/.ssh 
```
Serão exibidas as chaves existentes como por exemplo as listas a baixo:
```
config  id_ed25519  id_ed25519.pub
```

Selectione uma delas para executar no comando

```
git config core.sshCommand "ssh -i ~/.ssh/<ssh file name> -F /dev/null"
```

Esse comando ira adicionar uma diretiva no arquvo do repositório local `.git/config` na secção `[core]` como isso o git passa a executar o comando
nas operações ssh com o repositório.
