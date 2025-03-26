import base64
import hashlib
import hmac
import json
import time
import os
import secrets
import re

class ButterflyJWT:
    def __init__(self, secret_key):
        """
        Initialize JWT with a custom cryptographic implementation
        
        :param secret_key: Secret key for signing tokens
        """
        self.secret_key = secret_key.encode('utf-8')
    
    def _validate_email(self, email):
        """
        Validate email address using a comprehensive regex
        
        :param email: Email address to validate
        :return: Validated email or raises ValueError
        """
        # Comprehensive email validation regex
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # List of known temporary email domains to block
        temp_email_domains = [
            'temp-mail.org', 'tempmail.com', 'guerrillamail.com', 
            'mailinator.com', '10minutemail.com', 'throwawaymail.com'
        ]
        
        if not email:
            raise ValueError("Email address is required")
        
        if not re.match(email_regex, email):
            raise ValueError("Invalid email address format")
        
        # Check against temp email domains
        domain = email.split('@')[1].lower()
        if domain in temp_email_domains:
            raise ValueError("Temporary email addresses are not allowed")
        
        return email
    
    def _base64url_encode(self, input_bytes):
        """
        URL-safe base64 encoding
        
        :param input_bytes: Bytes to encode
        :return: URL-safe base64 encoded string
        """
        return base64.urlsafe_b64encode(input_bytes).rstrip(b'=').decode('utf-8')
    
    def _base64url_decode(self, input_str):
        """
        URL-safe base64 decoding
        
        :param input_str: URL-safe base64 encoded string
        :return: Decoded bytes
        """
        # Add padding back
        padding = 4 - (len(input_str) % 4)
        input_str += '=' * (padding if padding < 4 else 0)
        return base64.urlsafe_b64decode(input_str.encode('utf-8'))
    
    def _encrypt_email(self, email):
        """
        Encrypt email address
        
        :param email: Email to encrypt
        :return: Encrypted email
        """
        # Simple encryption using HMAC (in a real-world scenario, use a more robust encryption)
        encrypted = hmac.new(
            self.secret_key, 
            email.encode('utf-8'), 
            hashlib.sha256
        ).hexdigest()
        return encrypted
    
    def create_token(self, payload, dev_mode=False, email=None, expires_in=3600):
        """
        Create a JWT token with optional email encryption
        
        :param payload: Dictionary of claims
        :param dev_mode: Boolean to toggle strict email requirement
        :param email: Email address to encrypt
        :param expires_in: Token expiration time in seconds
        :return: JWT string
        """
        # Validate and encrypt email if not in dev mode
        encrypted_email = None
        if not dev_mode:
            if not email:
                raise ValueError("Email is required in production mode")
            
            # Validate and encrypt email
            validated_email = self._validate_email(email)
            encrypted_email = self._encrypt_email(validated_email)
        
        # Create header
        header = {
            "alg": "HS256",
            "typ": "JWT",
            "jti": secrets.token_hex(16)
        }
        
        # Add standard claims and encrypted email if applicable
        current_time = int(time.time())
        payload.update({
            "iat": current_time,  # Issued at
            "exp": current_time + expires_in,  # Expiration
        })
        
        # Add encrypted email to payload if applicable
        if encrypted_email:
            payload['encrypted_email'] = encrypted_email
        
        # Encode header and payload
        encoded_header = self._base64url_encode(json.dumps(header).encode('utf-8'))
        encoded_payload = self._base64url_encode(json.dumps(payload).encode('utf-8'))
        
        # Create signature
        signature_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
        signature = self._base64url_encode(
            hmac.new(self.secret_key, signature_input, hashlib.sha256).digest()
        )
        
        # Combine token parts
        return f"{encoded_header}.{encoded_payload}.{signature}"
    
    def verify_token(self, token):
        """
        Verify and decode a JWT token
        
        :param token: JWT token string
        :return: Decoded payload
        """
        # Split token into parts
        try:
            encoded_header, encoded_payload, signature = token.split('.')
        except ValueError:
            raise ValueError("Invalid token format")
        
        # Verify signature
        signature_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
        expected_signature = self._base64url_encode(
            hmac.new(self.secret_key, signature_input, hashlib.sha256).digest()
        )
        
        if not hmac.compare_digest(expected_signature, signature):
            raise ValueError("Invalid signature")
        
        # Decode payload
        try:
            decoded_header = json.loads(self._base64url_decode(encoded_header))
            decoded_payload = json.loads(self._base64url_decode(encoded_payload))
        except (json.JSONDecodeError, ValueError):
            raise ValueError("Invalid token")
        
        # Check expiration
        current_time = int(time.time())
        if current_time > decoded_payload.get('exp', 0):
            raise ValueError("Token has expired")
        
        return decoded_payload

# Alias functions with additional email parameter
def encode(secret_key, payload, dev_mode=False, email=None, expires_in=3600):
    """
    Convenience function to encode a JWT
    
    :param secret_key: Secret key for signing
    :param payload: Token payload
    :param dev_mode: Boolean to toggle strict email requirement
    :param email: Email address to encrypt
    :param expires_in: Token expiration time
    :return: Encoded JWT
    """
    return ButterflyJWT(secret_key).create_token(
        payload, 
        dev_mode=dev_mode, 
        email=email, 
        expires_in=expires_in
    )

def decode(secret_key, token):
    """
    Convenience function to decode a JWT
    
    :param secret_key: Secret key for signing
    :param token: JWT token to decode
    :return: Decoded payload
    """
    return ButterflyJWT(secret_key).verify_token(token)