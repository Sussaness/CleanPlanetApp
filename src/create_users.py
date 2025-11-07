import hashlib
import binascii
import os

def hash_password(password):
    """Генерация хеша пароля"""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

# Генерация хешей для тестовых паролей
print("Хеш для admin123:", hash_password('admin123'))
print("Хеш для manager123:", hash_password('manager123'))