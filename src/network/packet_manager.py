# src/network/packet_manager.py

import struct
import hmac
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class PacketManager:
    def __init__(self):
        self.sequence_number = 0
        self.encryption_key = None
        self.mac_key = None
        self.cipher = None

    def set_encryption(self, encryption_key, mac_key):
        self.encryption_key = encryption_key
        self.mac_key = mac_key
        self.cipher = Cipher(
            algorithms.AES(encryption_key),
            modes.CTR(b"\x00" * 16),
            backend=default_backend(),
        )

    def create_packet(self, payload):
        """Create an SSH packet from the given payload."""
        padding_length = 8 - ((len(payload) + 5) % 8)
        if padding_length < 4:
            padding_length += 8

        padding = os.urandom(padding_length)
        packet_length = len(payload) + padding_length + 1
        packet = (
            struct.pack(">I", packet_length)
            + bytes([padding_length])
            + payload
            + padding
        )

        if self.encryption_key:
            encryptor = self.cipher.encryptor()
            packet = encryptor.update(packet) + encryptor.finalize()

        if self.mac_key:
            mac = hmac.new(
                self.mac_key,
                struct.pack(">I", self.sequence_number) + packet,
                hashlib.sha256,
            ).digest()
            packet += mac

        self.sequence_number += 1
        return packet

    def parse_packet(self, data):
        """Parse an SSH packet and return the payload."""
        if self.mac_key:
            mac_length = 32  # SHA256
            received_mac = data[-mac_length:]
            data = data[:-mac_length]
            expected_mac = hmac.new(
                self.mac_key,
                struct.pack(">I", self.sequence_number) + data,
                hashlib.sha256,
            ).digest()
            if received_mac != expected_mac:
                raise ValueError("MAC verification failed")

        if self.encryption_key:
            decryptor = self.cipher.decryptor()
            data = decryptor.update(data) + decryptor.finalize()

        packet_length = struct.unpack(">I", data[:4])[0]
        padding_length = data[4]
        payload = data[5 : packet_length - padding_length]

        self.sequence_number += 1
        return payload

    def create_kexinit_packet(
        self,
        cookie,
        kex_algorithms,
        server_host_key_algorithms,
        encryption_algorithms_client_to_server,
        encryption_algorithms_server_to_client,
        mac_algorithms_client_to_server,
        mac_algorithms_server_to_client,
        compression_algorithms_client_to_server,
        compression_algorithms_server_to_client,
        languages_client_to_server,
        languages_server_to_client,
    ):
        """Create a SSH_MSG_KEXINIT packet."""
        payload = (
            b"\x14"  # SSH_MSG_KEXINIT
            + cookie
            + self._create_name_list(kex_algorithms)
            + self._create_name_list(server_host_key_algorithms)
            + self._create_name_list(encryption_algorithms_client_to_server)
            + self._create_name_list(encryption_algorithms_server_to_client)
            + self._create_name_list(mac_algorithms_client_to_server)
            + self._create_name_list(mac_algorithms_server_to_client)
            + self._create_name_list(compression_algorithms_client_to_server)
            + self._create_name_list(compression_algorithms_server_to_client)
            + self._create_name_list(languages_client_to_server)
            + self._create_name_list(languages_server_to_client)
            + b"\x00"  # first_kex_packet_follows
            + b"\x00\x00\x00\x00"  # 0 (reserved for future extension)
        )
        return self.create_packet(payload)

    def _create_name_list(self, names):
        name_list = ",".join(names).encode("ascii")
        return struct.pack(">I", len(name_list)) + name_list


# Usage example:
# packet_manager = PacketManager()
# packet_manager.set_encryption(encryption_key, mac_key)
# packet = packet_manager.create_packet(b"Hello, SSH!")
# payload = packet_manager.parse_packet(packet)
