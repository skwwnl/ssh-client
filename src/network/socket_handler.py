import socket
from src.utils.logger import Logger


class SocketHandler:
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
        self.socket = None

    def connect(self, host, port):
        self.logger.info(f"Attempting to connect to {host}:{port}")
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.logger.info(f"Successfully connected to {host}:{port}")
        except socket.error as e:
            self.logger.error(f"Failed to connect to {host}:{port}. Error: {str(e)}")
            raise

    def send(self, data):
        if not self.socket:
            raise ValueError("Socket is not connected")

        self.logger.debug(f"Sending data: {data}")
        try:
            self.socket.sendall(data)
            self.logger.debug("Data sent successfully")
        except socket.error as e:
            self.logger.error(f"Failed to send data. Error: {str(e)}")
            raise

    def receive(self, buffer_size=1024):
        if not self.socket:
            raise ValueError("Socket is not connected")

        self.logger.debug(f"Attempting to receive data (buffer size: {buffer_size})")
        try:
            data = self.socket.recv(buffer_size)
            self.logger.debug(f"Received data: {data}")
            return data
        except socket.error as e:
            self.logger.error(f"Failed to receive data. Error: {str(e)}")
            raise

    def close(self):
        if self.socket:
            self.logger.info("Closing socket connection")
            self.socket.close()
            self.socket = None
        else:
            self.logger.warning("Attempting to close a non-existent socket connection")
