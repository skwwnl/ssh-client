import os
from dotenv import load_dotenv

# .evn 파일 load
load_dotenv()


class Config:
    VAULT_URL = os.getenv("VAULT_URL", "http://localhost:8200")
    VAULT_TOKEN = os.getenv("VAULT_TOKEN")
    VAULT_SECRET_PATH = os.getenv("VAULT_SECRET_PATH", "secret/data/server-info")

    SERVER_HOST = os.getenv("SERVER_HOST", "10.0.0.10")
    SERVER_PORT = int(os.getenv("SERVER_PORT"))

    @classmethod
    def get_vault_url(cls):
        return cls.VAULT_URL

    @classmethod
    def get_vault_token(cls):
        return cls.VAULT_TOKEN

    @classmethod
    def get_vault_secret_path(cls):
        return cls.VAULT_SECRET_PATH

    @classmethod
    def get_server_host(cls):
        return cls.SERVER_HOST

    @classmethod
    def get_server_port(cls):
        return cls.SERVER_PORT
