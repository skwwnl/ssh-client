from src.network.socket_handler import SocketHandler
from src.network.version_exchange import VersionExchanger
from src.utils.logger import Logger
from src.config.config import Config


def main():
    logger = Logger.get_logger(__name__)
    handler = SocketHandler()
    version = VersionExchanger(Config.SSH_CLIENT_VERSION)

    # =========== Total Connection Block ===========
    # socket_handler.py
    try:
        # Replace with the actual SSH server address and port
        handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)

        # =========== Total Version Exchange Block ===========
        # version_exchange.py

        # SSH client version output
        client_version = version.get_client_version_string()
        logger.info(f"Client version: {client_version}")

        # Exchange SSH Server version
        server_version = version.exchange_versions(handler)
        logger.info(f"Server version: {server_version}")

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
