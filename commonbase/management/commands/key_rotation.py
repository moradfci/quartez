from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from commonbase.fields import EncryptedField
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Rotate encryption keys and re-encrypt data with new keys'

    def __init__(self):
        # Load old keys
        self.private_key_old = self.load_private_key(
            settings.OLD_MESSAGES_ENCRYPTION_PRIVATE_KEY)
        self.public_key_old = self.load_public_key(
            settings.OLD_MESSAGES_ENCRYPTION_PUBLIC_KEY)

        # Load new keys
        self.private_key_new = self.load_private_key(
            settings.NEW_MESSAGES_ENCRYPTION_PRIVATE_KEY)
        self.public_key_new = self.load_public_key(
            settings.NEW_MESSAGES_ENCRYPTION_PUBLIC_KEY)

    def load_private_key(self, key_path):
        private_key_data = open(key_path, mode='rb').read()
        return serialization.load_pem_private_key(private_key_data, password=None)

    def load_public_key(self, key_path):
        public_key_data = open(key_path, mode='rb').read()
        return serialization.load_pem_public_key(public_key_data)

    def encrypt_data_with_new_key(self, value):
        """Encrypt using the new public key"""
        if isinstance(value, str):
            value = value.encode()  # Convert string to bytes
        encrypted = self.public_key_new.encrypt(
            value,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def decrypt_data_with_old_key(self, value):
        """Decrypt using the old private key"""
        if isinstance(value, str):
            value = value.encode()  # Convert string to bytes, in case it's stored as a string
        decrypted = self.private_key_old.decrypt(
            value,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted.decode()  # Convert bytes back to string

    def handle(self, *args, **kwargs):
        
        all_models = apps.get_models()
        models_with_encrypted_fields = {}

        for model in all_models:
            for field in model._meta.get_fields():
                if isinstance(field, EncryptedField):
                    models_with_encrypted_fields[model] = field

        
        for model, field in models_with_encrypted_fields.items():
            encrypted_field_name = field.name
            instances_to_update = []
        EncryptedField.key_rotation_mode = True

        # Your existing code to fetch and decrypt/encrypt data
        for model, field in models_with_encrypted_fields.items():
            encrypted_field_name = field.name
            instances_to_update = []

            for instance in model.objects.all():
                old_encrypted_value = getattr(instance, encrypted_field_name)
                if old_encrypted_value:
                    try:
                        decrypted_value = self.decrypt_data_with_old_key(old_encrypted_value)
                        new_encrypted_value = self.encrypt_data_with_new_key(decrypted_value)

                        setattr(instance, encrypted_field_name, new_encrypted_value)
                        instances_to_update.append(instance)
                    except Exception as e:
                        logger.error(f"Error processing {model} instance {instance.pk}: {e}")
                        continue

            # Perform bulk update without triggering field encryption/decryption
            if instances_to_update:
                model.objects.bulk_update(instances_to_update, [encrypted_field_name])

        # Disable key rotation mode after the process is done
        EncryptedField.key_rotation_mode = False

        print('success')
