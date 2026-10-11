+++
title = "Understanding and validating AWS Cognito JWT tokens in Go"
date = "2024-05-16"
tags = ["aws", "aws cognito", "golang"]
categories = ["post"]
draft = false
+++

When your API sits behind AWS Cognito, every request arrives with a JWT, and it's up to you to decide whether to trust it. Decoding the token is easy. Validating it properly takes a few more steps, and skipping one of them is how people end up accepting tokens they shouldn't.

## What's inside a JWT

A JWT (JSON Web Token) has three parts separated by dots:

1. Header: which algorithm signed the token and which key (`kid`) was used.
2. Payload: the claims, such as who the user is, who issued the token and when it expires.
3. Signature: proof that header and payload weren't tampered with.

Header and payload are just base64. Anyone can read and edit them. The signature is what makes the token trustworthy, so it's the first thing to check.

## Where the keys come from

Cognito signs tokens with a private key and publishes the matching public keys as a JSON Web Key Set (JWKS):

```
https://cognito-idp.<Region>.amazonaws.com/<userPoolId>/.well-known/jwks.json
```

You use these keys to verify the signature. They rarely change, so download them once and cache them instead of fetching on every request.

## The code

I use the [`jwx`](https://github.com/lestrrat-go/jwx) library (v2 in the examples below), which handles key caching, parsing and validation. First, a verifier that registers the JWKS URL in a cache:

```go
import (
	"context"
	"errors"
	"fmt"
	"time"

	"github.com/lestrrat-go/jwx/v2/jwk"
	"github.com/lestrrat-go/jwx/v2/jwt"
)

type Verifier struct {
	cache    *jwk.Cache
	jwksURL  string
	issuer   string
	clientID string
}

func NewVerifier(ctx context.Context, region, userPoolID, clientID string) (*Verifier, error) {
	issuer := fmt.Sprintf("https://cognito-idp.%s.amazonaws.com/%s", region, userPoolID)
	jwksURL := issuer + "/.well-known/jwks.json"

	cache := jwk.NewCache(ctx)
	if err := cache.Register(jwksURL, jwk.WithMinRefreshInterval(15*time.Minute)); err != nil {
		return nil, err
	}
	// Fetch once at startup so a bad URL fails fast.
	if _, err := cache.Refresh(ctx, jwksURL); err != nil {
		return nil, fmt.Errorf("failed to fetch AWS JWKS: %w", err)
	}

	return &Verifier{cache: cache, jwksURL: jwksURL, issuer: issuer, clientID: clientID}, nil
}
```

Then the verification itself:

```go
func (v *Verifier) Verify(ctx context.Context, rawToken string) (jwt.Token, error) {
	keyset, err := v.cache.Get(ctx, v.jwksURL)
	if err != nil {
		return nil, err
	}

	token, err := jwt.Parse([]byte(rawToken),
		jwt.WithKeySet(keyset),
		jwt.WithValidate(true),
		jwt.WithIssuer(v.issuer),
	)
	if err != nil {
		return nil, err
	}

	if use, _ := token.Get("token_use"); use != "access" {
		return nil, errors.New("not an access token")
	}
	if clientID, _ := token.Get("client_id"); clientID != v.clientID {
		return nil, errors.New("invalid client_id")
	}

	return token, nil
}
```

## What each check does

- `WithKeySet` verifies the signature using the key whose `kid` matches the token header.
- `WithValidate(true)` checks the time claims, so an expired token (`exp`) is rejected.
- `WithIssuer` makes sure the token came from your user pool and not from some other Cognito pool, which would be signed with perfectly valid keys too.
- `token_use` separates access tokens from ID tokens. Cognito issues both, and an API should only accept access tokens.
- `client_id` makes sure the token was issued to your app client. Access tokens carry `client_id`; ID tokens use `aud` instead, so if you ever validate ID tokens, check `aud`.

With these five checks you only grant access to tokens that were signed by your pool, are still valid, and were issued for your app.

# References

- [Verifying a JSON Web Token (AWS docs)](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html)
- [lestrrat-go/jwx](https://github.com/lestrrat-go/jwx)
