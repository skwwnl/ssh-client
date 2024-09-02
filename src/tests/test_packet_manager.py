# tests/test_packet_manager.py

import unittest
from unittest.mock import patch
from src.network.packet_manager import PacketManager
import os


class TestPacketManager(unittest.TestCase):
    def setUp(self):
        self.packet_manager = PacketManager()

    def test_create_packet_without_encryption(self):
        payload = b"Test payload"
        packet = self.packet_manager.create_packet(payload)

        # Packet structure: packet_length (4 bytes) + padding_length (1 byte) + payload + padding
        self.assertTrue(len(packet) > len(payload) + 5)

        # Check packet length
        packet_length = int.from_bytes(packet[:4], "big")
        self.assertEqual(packet_length, len(packet) - 4)

        # Check padding length
        padding_length = packet[4]
        self.assertTrue(4 <= padding_length <= 255)

        # Check payload
        extracted_payload = packet[5 : 5 + len(payload)]
        self.assertEqual(extracted_payload, payload)

    @patch("os.urandom")
    def test_create_packet_with_encryption(self, mock_urandom):
        mock_urandom.return_value = b"\x00" * 32  # Mock random padding

        self.packet_manager.set_encryption(b"\x00" * 32, b"\x00" * 32)  # Set dummy keys

        payload = b"Encrypted payload"
        packet = self.packet_manager.create_packet(payload)

        # Packet should be encrypted and have MAC
        self.assertNotEqual(packet[5 : 5 + len(payload)], payload)
        self.assertEqual(
            len(packet), 4 + 1 + len(payload) + 32 + 32
        )  # length + padding length + payload + padding + MAC

    def test_parse_packet_without_encryption(self):
        original_payload = b"Test payload"
        packet = self.packet_manager.create_packet(original_payload)
        parsed_payload = self.packet_manager.parse_packet(packet)

        self.assertEqual(parsed_payload, original_payload)

    def test_parse_packet_with_encryption(self):
        self.packet_manager.set_encryption(b"\x00" * 32, b"\x00" * 32)  # Set dummy keys

        original_payload = b"Encrypted payload"
        packet = self.packet_manager.create_packet(original_payload)
        parsed_payload = self.packet_manager.parse_packet(packet)

        self.assertEqual(parsed_payload, original_payload)

    def test_create_kexinit_packet(self):
        cookie = os.urandom(16)
        kex_algorithms = ["diffie-hellman-group14-sha1"]
        server_host_key_algorithms = ["ssh-rsa"]
        encryption_algorithms = ["aes128-ctr"]
        mac_algorithms = ["hmac-sha2-256"]
        compression_algorithms = ["none"]
        languages = []

        kexinit_packet = self.packet_manager.create_kexinit_packet(
            cookie,
            kex_algorithms,
            server_host_key_algorithms,
            encryption_algorithms,
            encryption_algorithms,
            mac_algorithms,
            mac_algorithms,
            compression_algorithms,
            compression_algorithms,
            languages,
            languages,
        )

        # Basic structure check
        self.assertTrue(len(kexinit_packet) > 16)  # At least longer than the cookie
        self.assertEqual(kexinit_packet[5], 20)  # SSH_MSG_KEXINIT is 20
        self.assertEqual(kexinit_packet[6:22], cookie)  # Check cookie

    def test_sequence_number_increment(self):
        initial_seq = self.packet_manager.sequence_number
        self.packet_manager.create_packet(b"Test")
        self.assertEqual(self.packet_manager.sequence_number, initial_seq + 1)

        self.packet_manager.parse_packet(self.packet_manager.create_packet(b"Test"))
        self.assertEqual(self.packet_manager.sequence_number, initial_seq + 2)


if __name__ == "__main__":
    unittest.main()
