import re
from .socket_handler import SocketHandler
from .packet_manager import PacketManager


class VersionExchange:
    def __init__(self, socket_handler: SocketHandler, packet_manager: PacketManager):
        self.socket_handler = socket_handler
        self.packet_manager = packet_manager
        self.client_version = "SSH-2.0-PythonSSHClient_1.0"
        self.server_version = None
        self.MAX_VERSION_LENGTH = 255  # RFC 4253 specifies max length of 255 chars

    def exchange_versions(self):
        """
        Perform the SSH version exchange with the server.
        """
        # Send client version
        self.socket_handler.send(self.client_version.encode() + b"\r\n")

        # Receive server version
        server_version_data = self.socket_handler.receive(
            self.MAX_VERSION_LENGTH + 2
        )  # +2 for \r\n
        self.server_version = self._parse_server_version(server_version_data)

        if not self._validate_server_version(self.server_version):
            raise ValueError("Invalid server version string")

        return self.server_version

    def _parse_server_version(self, version_data: bytes) -> str:
        """
        Parse the server version string from the received data.
        """
        version_str = version_data.decode("utf-8").strip()
        if len(version_str) > self.MAX_VERSION_LENGTH:
            raise ValueError(
                f"Server version string exceeds maximum length of {self.MAX_VERSION_LENGTH} characters"
            )

        match = re.match(r"^SSH-2.0-(\S+)", version_str)
        if match:
            return match.group(0)
        else:
            raise ValueError("Invalid server version format")

    def _validate_server_version(self, version: str) -> bool:
        """
        Validate the server version string.
        """
        return version.startswith("SSH-2.0-")


# Usage example (this would typically be in another file, e.g., main.py)
# if __name__ == "__main__":
#     socket_handler = SocketHandler("example.com", 22)
#     packet_manager = PacketManager()
#     version_exchange = VersionExchange(socket_handler, packet_manager)
#
#     try:
#         server_version = version_exchange.exchange_versions()
#         print(f"Server version: {server_version}")
#     except ValueError as e:
#         print(f"Error during version exchange: {str(e)}")
