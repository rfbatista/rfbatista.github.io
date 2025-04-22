+++
title = "Terraform"
tags = ["devops"]
categories = ["post"]
draft = false
+++

## Remote State

In projects that have more than one contributor it is important to have a remote backend for terraform
so the `tfstate` (that is the representation of real resources) are not lost or have some race condition when
two or more people apply modifications.
To have a remote backend you a state and a locking storage, in AWS the best approach is to have `S3` and `DynamoDB`.

The first step is to deploy the resource before defining the backend, so

```tf
provider "aws" {
  region                      = "us-east-2"
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "tf-backend-state"
  # Prevent accidental deletion of this S3 bucket
  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state_encryption" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_versioning" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_dynamodb_table" "terraform_locks" {
  name         = "tf-backend-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

Now you can deploy those resources `terraform apply`. After successfully applying the resources you can change the local backend for the remote one:

```tf
terraform {
  backend "s3" {
    bucket = "tf-neuralmind-state"
    key    = "global/s3/terraform.tfstate"
    region = "us-east-2"
    dynamodb_table = "tf-neuralmind-locks"
    encrypt        = true
  }
}
```

## Different Environments

Errors can happen while managing infrastructure with terraform, so you need strategies to experiment new approaches and to protect production environments. Terraform provide us with some approaches:

### Workspaces

Terraform can create different workspace that have isolation of resources, each workspace would have their own state, so nothing that you do on that workspace will affect another.

```sh
$ terraform workspace new <workspace name>
```

You can see available workspaces by running:

```sh
$ terraform workspace list
```

And to switch between them:

```sh
$ terraform workspace select example1
```

### File Layout

Put configuration files for each environment in different folders.
Configure diferent backend for each environment. Using different authentication mechanism and access control. Ex.: separete AWS account with separe S3 as backend
To avoid deployment errors it is recommended to separate futher by components like: vpc, services and datas-storages.

Each component is organized with 3 files:

- vars.tf
- output.tf
- main.tf

### Secret Stores

You can define passwords in AWS Secret Manager and access it in terraform

```tf
provider "aws" {
    region = "us-east-2"
}
resource "aws_db_instance" "example" {
    identifier_prefix = "terraform-up-and-running"
    engine = "mysql"
    allocated_storage = 10
    instance_class = "db.t2.micro"
    name = "example_database"
    username = "admin"
    password = data.aws_secretsmanager_secret_version.db_password.secret_string
}
data "aws_secretsmanager_secret_version" "db_password" {
    secret_id = "mysql-master-password-stage"
}
```

### terraform_remote_state data source

If you have different components, each one with its state and backend, how do you provide some variables, like database addres, to a web service. For this you use terraform_remote_state.

The first step is to add output variables to your component:

```tf
output "address" {
    value = aws_db_instance.example.address
    description = "Connect to the database at this endpoint"
}
output "port" {
    value = aws_db_instance.example.port
    description = "The port the database is listening on"
}
```

When you run `terraform apply` those variables values will be stored in the terraform state. To read from terraform state in S3 you could do this:

```tf
data "terraform_remote_state" "db" {
    backend = "s3"
}

config = {
    bucket = "(YOUR_BUCKET_NAME)"
    key = "stage/data-stores/mysql/terraform.tfstate"
    region = "us-east-2"
}
```

Using `terraform_remote_state` implie access to the entire state snapshot, which could post a security risk. The alterantive
is to use an external tool (https://developer.hashicorp.com/terraform/language/state/remote-state-data#alternative-ways-to-share-data-between-configurations)[https://developer.hashicorp.com/terraform/language/state/remote-state-data#alternative-ways-to-share-data-between-configurations] like Amazon SSM Parameter Store or HashiCorp Consul

# References

[20 Terraform Best Practices to Improve your TF workflow](https://spacelift.io/blog/terraform-best-practices)
