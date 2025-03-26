import dotenv
from dotenv.crypt import Crypt


def test_dotenv_with_secret_values__should_not_encrypt__due_to_no_key(dotenv_path):
    secret_key = Crypt.generate_key()
    secret_value = 'my super secret secret'
    secret_value_decrypted = Crypt.encrypt_value(secret_value, secret_key)
    assert secret_value_decrypted != secret_value

    dotenv_path.write_text(f'my_secret={secret_value_decrypted}')

    with dotenv_path.open() as f:
        result = dotenv.dotenv_values(stream=f)

    assert result == {"my_secret": secret_value_decrypted}


def test_dotenv_with_secret_values__should_encrypt(dotenv_path):
    secret_key = Crypt.generate_key()
    secret_value = 'my super secret secret'
    secret_value_decrypted = Crypt.encrypt_value(secret_value, secret_key)
    assert secret_value_decrypted != secret_value

    dotenv_path.write_text(f'my_secret={secret_value_decrypted}')

    with dotenv_path.open() as f:
        result = dotenv.dotenv_values(stream=f, secret_key=secret_key)

    assert result == {"my_secret": secret_value}
