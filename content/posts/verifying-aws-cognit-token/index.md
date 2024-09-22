+++
title = "Understanding and Validating JWT Tokens with AWS Cognito"
date = "2023-12-03"
tags = ["neovim"]
categories = ["post"]
draft = false
+++

A **JWT (JSON Web Token)** is composed of three parts:

1. **Header**
2. **Payload**
3. **Signature**

To validate a JWT issued by AWS Cognito, you first need to download the JSON Web Key Set (JWKS), which contains the public keys used to verify the token's signature. You can obtain the JWKS from the following URL:

```sh 
https://cognito-idp.<Region>.amazonaws.com/<userPoolId>/.well-known/jwks.json
```

## Verifying the Token

To simplify the process of verifying a JWT, you can use the [`jwx`](https://github.com/lestrrat-go/jwx) library, which handles the token parsing and validation.

## Creating a JWK Cache

A JWK cache helps you avoid repeatedly downloading the keys for each token validation. Here’s how to refresh the cache with the public keys:

```go
_, err := c.jwkCache.Refresh(ctx, c.publicKeysURL)
if err != nil {
    fmt.Printf("Failed to fetch AWS JWKS: %s\n", err)
    return false
}

## Parsing the JWT Token
Once you have the JWKS, you can parse the token using the cached keys. This ensures the token's signature is valid:

```go
token, err := jwt.Parse(rawToken, jwt.WithKeySet(keyset), jwt.WithValidate(true))
if err != nil {
    c.logger.Error("Failed to parse token", zap.Error(err))
    return err
}
```

## Validating the Token Claims
After parsing the token, you need to verify the claims it contains. Start by checking the client_id claim to ensure the token was issued for the correct client:

```go 
clientID, _ := token.Get("client_id")
if clientID != "client_id" {
    return errors.New("Invalid access token")
}
```
Next, confirm the iss (issuer) claim to ensure the token was issued by your Cognito user pool:

```go 
iss, _ := token.Get("iss")
if iss != "https://cognito-idp.<Region>.amazonaws.com/<userPoolId>" {
    return errors.New("Invalid access token")
}
```

You can securely validate JWT tokens issued by AWS Cognito using the jwx library. This ensures the token’s signature and claims are valid before granting access to your protected resources.

```
# References
[https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html)
