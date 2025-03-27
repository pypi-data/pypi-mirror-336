# JWT Authentication Plugin for auth-proxy

A JWT (JSON Web Token) authentication plugin for the Modular Authenticating Reverse Proxy.

## Installation

```bash
pip install auth-proxy-jwt
```

## Features

- Validates JWT tokens from the Authorization header
- Configurable secret key and algorithm
- Optional audience and issuer validation
- Customizable claims mapping
- Forwards user identity and role information to backend services

## Configuration

Add the JWT plugin to your auth-proxy configuration:

```yaml
auth_plugins:
  jwt:
    secret: "your-secret-key"
    algorithm: "HS256"
    audience: "your-api"
    issuer: "your-identity-provider"
    require_exp: true
    leeway: 10
    header_prefix: "Bearer"
    user_claim: "sub"
    role_claim: "roles"
    forward_claims: ["email", "permissions"]

paths:
  - path: "^/api/.*$"
    regex: true
    authenticate: true
    plugins: [jwt]
```

## Configuration Options

| Option           | Description                                | Default    |
| ---------------- | ------------------------------------------ | ---------- |
| `secret`         | Secret key for validating token signatures | (required) |
| `algorithm`      | JWT algorithm to use                       | `"HS256"`  |
| `audience`       | Expected audience claim                    | `null`     |
| `issuer`         | Expected issuer claim                      | `null`     |
| `require_exp`    | Whether to require expiration time         | `true`     |
| `leeway`         | Leeway in seconds for expiration time      | `0`        |
| `header_prefix`  | Authorization header prefix                | `"Bearer"` |
| `user_claim`     | Claim to use for user identity             | `"sub"`    |
| `role_claim`     | Claim to use for role information          | `"role"`   |
| `forward_claims` | Additional claims to forward as headers    | `[]`       |

## Headers Added to Backend Requests

When authentication succeeds, the plugin adds the following headers to the proxied request:

- `X-Auth-User`: The user identity from the token (from the configured `user_claim`)
- `X-Auth-Role`: The role or roles from the token (from the configured `role_claim`)
- `X-Auth-Claim-{name}`: Additional claims specified in `forward_claims`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
