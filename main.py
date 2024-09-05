from src.network.socket_handler import SocketHandler
from src.network.version_exchange import VersionExchanger
from src.utils.logger import Logger
from src.config.config import Config

SSH_CLIENT_VERSION = "SSH-2.0-PythonSSHClient_1.0"

def main():
    logger = Logger.get_logger(__name__)
    handler = SocketHandler()
    version = VersionExchanger()

    try:
        # Replace with the actual SSH server address and port
        handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)

        # Send a simple message (this is not a valid SSH message, just for testing)
        handler.send(b"Hello, SSH Server!")

        # Receive response
        response = handler.receive()
        logger.info(f"Received: {response}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        handler.close()


if __name__ == "__main__":
    main()
