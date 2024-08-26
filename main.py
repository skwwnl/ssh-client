from src.network.socket_handler import SocketHandler
from src.utils.logger import Logger
import src.config


def main():
    logger = Logger.get_logger(__name__)
    handler = SocketHandler()
    try:
        # Replace with the actual SSH server address and port
        handler.connect("example.com", 22)

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
