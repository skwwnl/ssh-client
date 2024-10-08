import unittest
import socket
from unittest.mock import patch, MagicMock
from src.network.socket_handler import SocketHandler
from src.config.config import Config

# give when then
class TestSocketHandler(unittest.TestCase):

    def setUp(self):
        self.handler = SocketHandler()

    @patch("socket.socket")
    def test_connect_success(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        self.handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)

        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)
        mock_socket_instance.connect.assert_called_once_with(
            (Config.SERVER_HOST, Config.SERVER_PORT)
        )

    @patch("socket.socket")
    def test_connect_failure(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket_instance.connect.side_effect = socket.error("Connection refused")
        mock_socket.return_value = mock_socket_instance

        with self.assertRaises(socket.error):
            self.handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)

    @patch("socket.socket")
    def test_send_success(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        self.handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)
        self.handler.send(b"Test data")

        mock_socket_instance.sendall.assert_called_once_with(b"Test data")

    @patch("socket.socket")
    def test_send_failure(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket_instance.sendall.side_effect = socket.error("Connection lost")
        mock_socket.return_value = mock_socket_instance

        self.handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)
        with self.assertRaises(socket.error):
            self.handler.send(b"Test data")

    @patch("socket.socket")
    def test_receive_success(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket_instance.recv.return_value = b"Test response"
        mock_socket.return_value = mock_socket_instance

        self.handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)
        response = self.handler.receive()

        self.assertEqual(response, b"Test response")
        mock_socket_instance.recv.assert_called_once_with(1024)

    @patch("socket.socket")
    def test_receive_failure(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket_instance.recv.side_effect = socket.error("Connection lost")
        mock_socket.return_value = mock_socket_instance

        self.handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)
        with self.assertRaises(socket.error):
            self.handler.receive()

    @patch("socket.socket")
    def test_close(self, mock_socket):
        mock_socket_instance = MagicMock()
        mock_socket.return_value = mock_socket_instance

        self.handler.connect(Config.SERVER_HOST, Config.SERVER_PORT)
        self.handler.close()

        mock_socket_instance.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
