import sys
import os

# 현재 스크립트의 디렉토리를 얻습니다
current_dir = os.path.dirname(os.path.abspath(__file__))
# 프로젝트 루트 디렉토리를 sys.path에 추가합니다
sys.path.insert(0, os.path.dirname(current_dir))

from utils.logger import Logger


class CryptoManager:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)

    def some_method(self):
        self.logger.info("This is an info message")
        self.logger.debug("This is a debug message")

    def encrypt(self, data):
        self.logger.debug("Encrypting data")
        # Implement encryption logic here
        pass

    def decrypt(self, data):
        self.logger.debug("Decrypting data")
        # Implement decryption logic here
        pass


print(CryptoManager().some_method())
