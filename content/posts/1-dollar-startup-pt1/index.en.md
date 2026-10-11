+++
title = "1 dollar side project, part 1: setting up Lightsail"
date = "2023-10-02"
tags = ["aws", "lightsail", "devops", "golang"]
categories = ["post"]
draft = false
+++

# Some context

I've been using AWS Lightsail for my personal projects for a few months now, and it has turned out to be both capable and cheap. There's no shortage of backend-as-a-service, database-as-a-service or whatever-as-a-service options, but they tend to go one of two ways: either you become so dependent on the provider that leaving is painful, or the bill grows faster than the project.

What I care about most in side projects is having full control over what's running. That's what this setup is built around. My main goal with personal projects is to understand in detail what's going on, so I wouldn't necessarily make the same choices for a company project.

# What we'll be using

- Lightsail, for the server
- CodeBuild, CodeDeploy and CodePipeline, for build and deploy
- [Webmin](https://webmin.com/), to manage the server through a browser
- Go, for the application
- systemd, to keep the application running
- [Caddy](https://github.com/caddyserver/caddy), as the reverse proxy with automatic HTTPS

This first part covers the AWS account and getting the Lightsail instance ready to receive deploys from CodeDeploy.

# 1. AWS account

I won't go step by step through creating an AWS account. The official guide covers it: [https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)

Two recommendations before anything else. First, turn on two-factor authentication (2FA). An app like [Google Authenticator](https://apps.apple.com/br/app/google-authenticator/id388497605) is enough. Second, don't use the root account day to day. Create two users: one with full access, kept for emergencies, and another limited to what this project needs (Lightsail, CodeBuild, CodeDeploy, CodePipeline and Budgets). Do all the work with the second one.

While you're at it, set up a budget alert in AWS Budgets. The whole point of the project is to cost almost nothing, and the alert is what tells you when that stops being true.

# 2. IAM permissions for CodeDeploy

CodeDeploy needs two identities:

- A service role with the `AWSCodeDeployRole` policy, which lets CodeDeploy act on your behalf.
- An IAM user with programmatic access (access key and secret) and permission to read the S3 bucket where the build artifacts will live. This is the identity the CodeDeploy agent on the instance uses to talk to AWS.

Why a user with keys instead of an instance role? CodeDeploy doesn't see Lightsail instances as EC2. To CodeDeploy, a Lightsail instance is an "on-premises" server, just like a machine in your house, so it has to authenticate with credentials.

# 3. Creating the Lightsail instance

In the Lightsail console, create an instance on Linux and pick the plan. When I wrote this I used Amazon Linux 2, which has since reached end of support, so today I'd go with Amazon Linux 2023.

In the launch script field, add the CodeDeploy agent install so the instance comes up ready:

```sh
#!/bin/bash
yum update -y
yum install -y ruby wget
cd /home/ec2-user
wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
chmod +x ./install
./install auto
```

Swap `us-east-1` for your region in both places in the URL. Add a key-value tag to the instance (for example `app=DollarProject`), which will help when organizing deploys, and create the instance.

Once it's up, connect over SSH and check that the agent is running:

```sh
sudo service codedeploy-agent status
```

# 4. Registering the instance with CodeDeploy

Because it's an on-premises server, you have to tell CodeDeploy the instance exists. On the instance, create the file `/etc/codedeploy-agent/conf/codedeploy.onpremises.yml` with the credentials of the user from step 2:

```yaml
---
aws_access_key_id: <access key>
aws_secret_access_key: <secret key>
iam_user_arn: arn:aws:iam::<account id>:user/<user>
region: <region>
```

Then, from your machine with the AWS CLI configured, register the instance and tag it:

```sh
aws deploy register-on-premises-instance \
  --instance-name dollar-project \
  --iam-user-arn arn:aws:iam::<account id>:user/<user>

aws deploy add-tags-to-on-premises-instances \
  --instance-names dollar-project \
  --tags Key=app,Value=DollarProject
```

Restart the agent on the instance (`sudo service codedeploy-agent restart`) so it picks up the new configuration.

# 5. Creating the application in CodeDeploy

In the CodeDeploy console, create an application named `DollarProject` with the EC2/On-premises compute platform. Then create a deployment group named `DemoDeploymentGroup`, choose on-premises instances as the environment, and select the instance by the `app=DollarProject` tag.

With that, the instance is ready to receive deploys. In the next part I set up CodeBuild and CodePipeline so that a push to the repository triggers the whole flow.
