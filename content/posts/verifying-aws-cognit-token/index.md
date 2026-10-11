+++
title = "Entendendo e validando tokens JWT do AWS Cognito em Go"
date = "2024-05-16"
tags = ["aws", "aws cognito", "golang"]
categories = ["post"]
draft = false
+++

Quando sua API fica atrás do AWS Cognito, toda requisição chega com um JWT, e é você quem decide se confia nele ou não. Decodificar o token é fácil. Validar direito dá um pouco mais de trabalho, e é pulando uma dessas etapas que muita gente acaba aceitando token que não deveria.

## O que tem dentro de um JWT

Um JWT (JSON Web Token) tem três partes separadas por pontos:

1. Header: qual algoritmo assinou o token e qual chave (`kid`) foi usada.
2. Payload: as claims, como quem é o usuário, quem emitiu o token e quando ele expira.
3. Assinatura: a prova de que header e payload não foram alterados.

Header e payload são só base64. Qualquer um consegue ler e editar. É a assinatura que torna o token confiável, então ela é a primeira coisa a verificar.

## De onde vêm as chaves

O Cognito assina os tokens com uma chave privada e publica as chaves públicas correspondentes num JSON Web Key Set (JWKS):

```
https://cognito-idp.<Region>.amazonaws.com/<userPoolId>/.well-known/jwks.json
```

São essas chaves que você usa para verificar a assinatura. Elas quase nunca mudam, então baixe uma vez e guarde em cache em vez de buscar a cada requisição.

## O código

Eu uso a biblioteca [`jwx`](https://github.com/lestrrat-go/jwx) (a v2 nos exemplos abaixo), que cuida do cache das chaves, do parse e da validação. Primeiro, um verificador que registra a URL do JWKS num cache:

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
	// Busca uma vez na inicialização para uma URL errada falhar logo.
	if _, err := cache.Refresh(ctx, jwksURL); err != nil {
		return nil, fmt.Errorf("falha ao buscar o JWKS da AWS: %w", err)
	}

	return &Verifier{cache: cache, jwksURL: jwksURL, issuer: issuer, clientID: clientID}, nil
}
```

Depois, a verificação em si:

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
		return nil, errors.New("não é um access token")
	}
	if clientID, _ := token.Get("client_id"); clientID != v.clientID {
		return nil, errors.New("client_id inválido")
	}

	return token, nil
}
```

## O que cada verificação faz

- `WithKeySet` verifica a assinatura usando a chave cujo `kid` bate com o header do token.
- `WithValidate(true)` confere as claims de tempo, então um token expirado (`exp`) é rejeitado.
- `WithIssuer` garante que o token veio do seu user pool, e não de outro pool do Cognito, que também seria assinado com chaves perfeitamente válidas.
- `token_use` separa access tokens de ID tokens. O Cognito emite os dois, e uma API deve aceitar só access tokens.
- `client_id` garante que o token foi emitido para o seu app client. Access tokens trazem `client_id`; ID tokens usam `aud`, então se um dia for validar ID tokens, confira o `aud`.

Com essas cinco verificações, você só libera acesso para tokens assinados pelo seu pool, ainda válidos e emitidos para o seu app.

# Referências

- [Verifying a JSON Web Token (documentação da AWS)](https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-tokens-verifying-a-jwt.html)
- [lestrrat-go/jwx](https://github.com/lestrrat-go/jwx)
