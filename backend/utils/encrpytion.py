from cryptography.fernet import Fernet


def encrypt_file(file_path, key):
    """Шифрует файл с использованием ключа и сохраняет зашифрованное содержимое обратно в тот же файл."""
    # Открываем файл для чтения в бинарном режиме
    with open(file_path, 'rb') as file:
        data = file.read()

    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data)

    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as enc_file:
        enc_file.write(encrypted_data)


def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        encrypted_data_file = file.read()

    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data_file)

    return decrypted_data