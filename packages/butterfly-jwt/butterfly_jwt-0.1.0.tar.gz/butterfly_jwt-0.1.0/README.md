# Butterfly JWT

A lightweight, pure Python JSON Web Token (JWT) library with no external dependencies.

## Installation

```bash
pip install butterfly-jwt
```

## Usage

### Encoding a Token

```python
from butterfly import jwt

# Create a token
secret_key = "your_secret_key"
payload = {"user_id": 123, "username": "example_user"}
token = jwt.encode(secret_key, payload)
```

### Decoding a Token

```python
from butterfly import jwt

try:
    payload = jwt.decode(secret_key, token)
    print(payload)
except ValueError as e:
    print("Token verification failed:", str(e))
```

### Using the ButterflyJWT Class

```python
from butterfly.jwt import ButterflyJWT

# Create a JWT instance
jwt_handler = ButterflyJWT(secret_key)

# Create a token
token = jwt_handler.create_token(payload)

# Verify a token
payload = jwt_handler.verify_token(token)
```

## Features

- Pure Python implementation
- No external dependencies
- URL-safe Base64 encoding
- HMAC-SHA256 signature
- Token expiration checking
- Constant-time signature verification

## License

MIT License