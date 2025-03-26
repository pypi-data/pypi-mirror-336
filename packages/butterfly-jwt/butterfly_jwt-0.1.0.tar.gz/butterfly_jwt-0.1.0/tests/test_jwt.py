import time
import pytest
from butterfly.jwt import ButterflyJWT, encode, decode

def test_token_creation_and_verification():
    secret_key = "test_secret_key"
    payload = {"user_id": 123, "username": "testuser"}
    
    # Create token using ButterflyJWT class
    jwt_handler = ButterflyJWT(secret_key)
    token = jwt_handler.create_token(payload, dev_mode=True)
    
    # Verify token
    decoded_payload = jwt_handler.verify_token(token)
    
    assert decoded_payload['user_id'] == 123
    assert decoded_payload['username'] == 'testuser'
    assert 'iat' in decoded_payload
    assert 'exp' in decoded_payload

def test_token_creation_with_functions():
    secret_key = "test_secret_key"
    payload = {"user_id": 456, "username": "anotheruser"}
    
    # Create token using convenience functions
    token = encode(secret_key, payload, dev_mode=True)
    
    # Decode token
    decoded_payload = decode(secret_key, token)
    
    assert decoded_payload['user_id'] == 456
    assert decoded_payload['username'] == 'anotheruser'

def test_expired_token():
    secret_key = "test_secret_key"
    payload = {"user_id": 789}
    
    # Create a token that expires immediately
    jwt_handler = ButterflyJWT(secret_key)
    token = jwt_handler.create_token(payload, dev_mode=True, expires_in=0)
    
    # Wait a moment to ensure token is expired
    time.sleep(1)
    
    with pytest.raises(ValueError, match="Token has expired"):
        jwt_handler.verify_token(token)

def test_invalid_signature():
    secret_key = "test_secret_key"
    wrong_key = "wrong_secret_key"
    payload = {"user_id": 101}
    
    # Create token with one key
    jwt_handler = ButterflyJWT(secret_key)
    token = jwt_handler.create_token(payload, dev_mode=True)
    
    # Try to verify with wrong key
    wrong_jwt_handler = ButterflyJWT(wrong_key)
    
    with pytest.raises(ValueError, match="Invalid signature"):
        wrong_jwt_handler.verify_token(token)

# Additional test for email requirement in production mode
def test_email_requirement():
    secret_key = "test_secret_key"
    payload = {"user_id": 202}
    
    jwt_handler = ButterflyJWT(secret_key)
    
    # Should raise ValueError when email is not provided in production mode
    with pytest.raises(ValueError, match="Email is required in production mode"):
        jwt_handler.create_token(payload, dev_mode=False)