from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import base64

def encrypt_with_public_key(content: str, public_key_str: str) -> str:
    try:
        # Remove any whitespace and newlines from the key string
        public_key_str = public_key_str.replace(" ", "").replace("\n", "")
        
        # Add PEM headers if they're not present
        if not public_key_str.startswith("-----BEGIN"):
            public_key_str = f"-----BEGIN PUBLIC KEY-----\n{public_key_str}\n-----END PUBLIC KEY-----"
            
        # Create RSA key object
        key = RSA.importKey(public_key_str)
        cipher = PKCS1_v1_5.new(key)
        
        # Encrypt and encode
        encrypted = cipher.encrypt(content.encode())
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt content: {str(e)}")