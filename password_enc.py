import json
import base64
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class InvalidKey(Exception):
    """Custom exception when the master password is invalid"""

    def __init__(self) -> None:
        super().__init__("Invalid master password")


class ConfigError(Exception):
    """Custom exception when the config file can't be read"""

    def __init__(self, e) -> None:
        super().__init__(f"Error:{e}")


class PasswordEnc:
    """Creates a PasswordEnc object with the given master password."""

    # using the same SALT for every password
    SALT = b"\x17\xde\xb0^xh\xc2&\x9as\xe36\x88W\r\xb7"

    def __init__(self, master_password: str):
        self.kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=PasswordEnc.SALT,
            iterations=390000,
        )
        self._master_password = bytes(master_password, encoding="ascii")
        self._key = base64.urlsafe_b64encode(self.kdf.derive(self._master_password))

    def encrypt(self, data: str | bytes) -> bytes:
        """Encrypts data with a key derived from the given master password"""
        if not isinstance(data, bytes):
            data = bytes(data, encoding="utf-8")

        fernet = Fernet(self._key)
        encrypted_bytes = fernet.encrypt(data)
        return encrypted_bytes

    def decrypt(self, encrypted_data: bytes) -> str:
        """Decodes passed encrypted data. Raise InvalidKey if master password is invalid"""

        fernet = Fernet(self._key)
        try:
            decrypted_data = fernet.decrypt(encrypted_data)
        except cryptography.fernet.InvalidToken:
            raise InvalidKey()

        return str(decrypted_data, encoding="utf-8")

    def validate_master(self):
        """Tries to decrypt a already encrypted string in the config file.
        If it can be decrypted, returns True otherwise False."""
        try:
            json_file = open("configs.json")
        except Exception as err:
            raise ConfigError(err)
        else:
            json_dict = json.load(json_file)
            if json_dict["checkPassword"]:
                try:
                    check_password = bytes(json_dict["checkPassword"], encoding="utf-8")
                    self.decrypt(check_password)
                    validate = True
                except InvalidKey:
                    validate = False
        finally:
            json_file.close()

        return validate

    def store_master(self):
        """Stores a random encrypted string in a config file"""
        encrypted_sample = str(self.encrypt("random"), encoding="utf-8")
        json_data = {"checkPassword": encrypted_sample}
        config_file = open("configs.json", "w")

        try:
            json.dump(json_data, config_file)
        except Exception as err:
            raise ConfigError(err)
        finally:
            config_file.close()


def main():
    # encrypted_str = bytes(
    #     "gAAAAABitInv-nm5LGSSIx9HerIQZL0ZPI97OAtFoGEQ8LjgDJy7f-dOQo6AFhtcXfqxQN67oESNyhrKT-bIOXQ1D32FKEhToXpd5VH1u8sxJZISKyV0_mM=",
    #     encoding="utf-8",
    # )
    pass

    # password_object = PasswordEnc("root")
    # print(password_object.validate_master())

    # try:
    #     print(password_object.decrypt(encrypted_str))
    # except InvalidKey:
    #     print("invalid master password")


if __name__ == "__main__":
    main()
