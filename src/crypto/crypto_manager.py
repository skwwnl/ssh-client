from src.utils.logger import Logger


class CryptoManager:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def encrypt(self, data):
        self.logger.debug("Encrypting data")
        # Implement encryption logic here
        pass

    def decrypt(self, data):
        self.logger.debug("Decrypting data")
        # Implement decryption logic here
        pass
