from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet, InvalidToken
import base64
import logging

logger = logging.getLogger(__name__)


class EncryptedField(models.Field):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        private_key = open(settings.MESSAGES_ENCRYPTION_PRIVATE_KEY, mode='rb').read()
        public_key = open(settings.MESSAGES_ENCRYPTION_PUBLIC_KEY, mode='rb').read()
        self.private_key = serialization.load_pem_private_key(
            private_key,
            password=None
        )
      
        self.public_key = serialization.load_pem_public_key(public_key)

    def get_prep_value(self, value):
        # Encrypt using the public key
        encrypted = self.public_key.encrypt(
            value.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def from_db_value(self, value, expression, connection):
        # Decrypt using the private key
        decrypted = self.private_key.decrypt(
            value,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()

