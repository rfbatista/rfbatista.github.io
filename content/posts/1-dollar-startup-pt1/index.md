+++
title = "1 dollar side project Pt. 1 - Lightsail configuration "
date = "2023-10-02"
tags = ["aws", "lightsail", "devops", "golang"]
draft = false
+++

# Some context

I have been using AWS lightsail services for my personal projects for some months now, and it proved to me to be quite powerful and cheap. There is a lot of options for backend-as-a-service, database-as-a-service, or whatever-as-a-service, but, or it make you really dependent on that provider (make it hard to change afterwards) or it became too expensive. In my side projects the most important thing for me is the complete control of what is going on in my services. Based on that, I have to say that this setup I made is thinking in my objectives for my personal projects, that above all else is to learn in details whats is going on. I would not have the same approach if it was not a personal project.

# What we will be using

- Lightsail
- Codebuild
- Codedeploy
- CodePipeline
- [Webmin](https://webmin.com/)
- Golang
- Systemd
- [Caddy](https://github.com/caddyserver/caddy)

# 1. AWS account setup

I will not enter in a step by step, on how to create an AWS account, I will just point to a link that have more details on how to do that: [https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)

I recommend for you to install [Google Authenticator](https://apps.apple.com/br/app/google-authenticator/id388497605) and enable Two-Factor Authentication (2FA) in your AWS account to have another layer of security. And to create 2 users, one with complete control of your account and another with limited control (Lightsail, Codebuild, Codedeploy, Codepipeline, Budget) and just use the latter to do the work.


2. Create a IAM User

- Open the IAM console, create a role with policy as codedeploy. Also create a user with programmatic access with s3codedeploybucket policy.
- Open the lightsail console, create an instance with Amazon Linux 2 OS. Choose the instance plan and define the script for installation of codedeploy agent. Then give the key-value tag and click on create instance. Once the instance is created, we can see all the configuration of the instance and can check if the codedeploy agent service is running.

3. Register the Lightsail Instance with CodeDeploy and Configure of application in CodeDeploy

4. Create CodeDeploy Application 

 Create an application named DollarProject with EC2/On-premises compute platform. Also create a deployment group with required parameters named DemoDeploymentGroup.


