# tests/test_network.py

import unittest
from unittest.mock import Mock, patch
from src.network.version_exchange import VersionExchange


class TestVersionExchange(unittest.TestCase):
    def setUp(self):
        self.mock_socket_handler = Mock()
        self.mock_packet_manager = Mock()
        self.version_exchange = VersionExchange(
            self.mock_socket_handler, self.mock_packet_manager
        )

    def test_successful_version_exchange(self):
        # Arrange
        self.mock_socket_handler.receive.return_value = (
            b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n"
        )

        # Act
        server_version = self.version_exchange.exchange_versions()

        # Assert
        self.mock_socket_handler.send.assert_called_once_with(
            b"SSH-2.0-PythonSSHClient_1.0\r\n"
        )
        self.assertEqual(server_version, "SSH-2.0-OpenSSH_8.2p1")

    def test_invalid_server_version(self):
        # Arrange
        self.mock_socket_handler.receive.return_value = b"Invalid-SSH-Version\r\n"

        # Act & Assert
        with self.assertRaises(ValueError):
            self.version_exchange.exchange_versions()

    def test_server_version_too_long(self):
        # Arrange
        long_version = "SSH-2.0-" + "X" * 256
        self.mock_socket_handler.receive.return_value = long_version.encode() + b"\r\n"

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            self.version_exchange.exchange_versions()

        self.assertIn("exceeds maximum length", str(context.exception))

    @patch("src.network.version_exchange.SocketHandler")
    @patch("src.network.version_exchange.PacketManager")
    def test_integration(self, mock_packet_manager, mock_socket_handler):
        # Arrange
        mock_socket = mock_socket_handler.return_value
        mock_socket.receive.return_value = (
            b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5\r\n"
        )

        # Act
        version_exchange = VersionExchange(
            mock_socket, mock_packet_manager.return_value
        )
        server_version = version_exchange.exchange_versions()

        # Assert
        mock_socket.send.assert_called_once_with(b"SSH-2.0-PythonSSHClient_1.0\r\n")
        self.assertEqual(server_version, "SSH-2.0-OpenSSH_8.2p1")


if __name__ == "__main__":
    unittest.main()
