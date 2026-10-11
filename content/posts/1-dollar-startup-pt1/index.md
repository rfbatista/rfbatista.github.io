+++
title = "Side project de 1 dólar, parte 1: configurando o Lightsail"
date = "2023-10-02"
tags = ["aws", "lightsail", "devops", "golang"]
categories = ["post"]
draft = false
+++

# Um pouco de contexto

Faz alguns meses que uso o AWS Lightsail nos meus projetos pessoais, e ele se mostrou bem capaz e barato. Opção de backend-as-a-service, database-as-a-service ou qualquer-coisa-as-a-service não falta, mas elas costumam ir para um de dois lados: ou você fica tão dependente do fornecedor que sair dói, ou a conta cresce mais rápido que o projeto.

O que mais me importa em side project é ter controle total do que está rodando, e foi isso que guiou essa configuração. Meu principal objetivo com projetos pessoais é entender em detalhe o que está acontecendo, então eu não faria necessariamente as mesmas escolhas num projeto de empresa.

# O que vamos usar

- Lightsail, para o servidor
- CodeBuild, CodeDeploy e CodePipeline, para build e deploy
- [Webmin](https://webmin.com/), para administrar o servidor pelo navegador
- Go, para a aplicação
- systemd, para manter a aplicação no ar
- [Caddy](https://github.com/caddyserver/caddy), como proxy reverso com HTTPS automático

Esta primeira parte cobre a conta da AWS e a preparação da instância do Lightsail para receber deploys do CodeDeploy.

# 1. Conta da AWS

Não vou fazer o passo a passo de criação da conta. O guia oficial cobre isso: [https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)

Duas recomendações antes de qualquer coisa. Primeiro, ative a autenticação em dois fatores (2FA). Um app como o [Google Authenticator](https://apps.apple.com/br/app/google-authenticator/id388497605) já resolve. Segundo, não use a conta root no dia a dia. Crie dois usuários: um com acesso total, guardado para emergências, e outro limitado ao que o projeto precisa (Lightsail, CodeBuild, CodeDeploy, CodePipeline e Budgets). Faça todo o trabalho com o segundo.

Aproveite e configure um alerta no AWS Budgets. A graça do projeto é custar quase nada, e é o alerta que avisa quando isso deixa de ser verdade.

# 2. Permissões no IAM para o CodeDeploy

O CodeDeploy precisa de duas identidades:

- Uma service role com a policy `AWSCodeDeployRole`, que deixa o CodeDeploy agir em seu nome.
- Um usuário do IAM com acesso programático (access key e secret) e permissão para ler o bucket do S3 onde os artefatos do build vão ficar. É com essa identidade que o agente do CodeDeploy na instância conversa com a AWS.

Por que um usuário com chaves em vez de uma role na instância? O CodeDeploy não enxerga instâncias do Lightsail como EC2. Para ele, uma instância do Lightsail é um servidor "on-premises", igual a uma máquina na sua casa, então ela precisa se autenticar com credenciais.

# 3. Criando a instância no Lightsail

No console do Lightsail, crie uma instância Linux e escolha o plano. Quando escrevi este post usei Amazon Linux 2, que já chegou ao fim do suporte, então hoje eu iria de Amazon Linux 2023.

No campo de launch script, coloque a instalação do agente do CodeDeploy para a instância já subir pronta:

```sh
#!/bin/bash
yum update -y
yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
./install auto
```

Troque `us-east-1` pela sua região nos dois lugares da URL. Adicione uma tag chave-valor na instância (por exemplo `app=DollarProject`), que vai ajudar a organizar os deploys, e crie a instância.

Quando ela subir, conecte por SSH e confira se o agente está rodando:

```sh
sudo service codedeploy-agent status
```

# 4. Registrando a instância no CodeDeploy

Como é um servidor on-premises, você precisa avisar o CodeDeploy de que a instância existe. Na instância, crie o arquivo `/etc/codedeploy-agent/conf/codedeploy.onpremises.yml` com as credenciais do usuário do passo 2:

```yaml
---
aws_access_key_id: <access key>
aws_secret_access_key: <secret key>
iam_user_arn: arn:aws:iam::<id da conta>:user/<usuario>
region: <regiao>
```

Depois, da sua máquina com o AWS CLI configurado, registre a instância e coloque a tag:

```sh
aws deploy register-on-premises-instance \
  --instance-name dollar-project \
  --iam-user-arn arn:aws:iam::<id da conta>:user/<usuario>

aws deploy add-tags-to-on-premises-instances \
  --instance-names dollar-project \
  --tags Key=app,Value=DollarProject
```

Reinicie o agente na instância (`sudo service codedeploy-agent restart`) para ele ler a configuração nova.

# 5. Criando a aplicação no CodeDeploy

No console do CodeDeploy, crie uma aplicação chamada `DollarProject` com a plataforma EC2/On-premises. Depois crie um deployment group chamado `DemoDeploymentGroup`, escolha instâncias on-premises como ambiente e selecione a instância pela tag `app=DollarProject`.

Com isso, a instância está pronta para receber deploys. Na próxima parte eu configuro o CodeBuild e o CodePipeline para que um push no repositório dispare o fluxo inteiro.
