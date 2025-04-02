# test_sniffer_unittest.py
import unittest
import socket
import struct
import ipaddress
from unittest.mock import patch, MagicMock
from sniffer import IP, ICMP, Scanner, udp_sender, MESSAGE

# Ваши сетевые параметры
YOUR_IP = "192.168.0.102"
YOUR_SUBNET = "192.168.0.0/24"


class TestIP(unittest.TestCase):
    def setUp(self):
        self.raw_ip_header = struct.pack(
            "<BBHHHBBH4s4s",
            0x45, 0, 0, 0, 0, 0, 1, 0,
            socket.inet_aton(YOUR_IP),
            socket.inet_aton("192.168.0.1")  # Пример другого IP в вашей подсети
        )


class TestUDPSender(unittest.TestCase):
    @patch('socket.socket')
    def test_udp_sender(self, mock_socket):
        # Используем вашу подсеть
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        udp_sender(YOUR_SUBNET)

        network = ipaddress.ip_network(YOUR_SUBNET)
        hosts = list(network.hosts())

        # Для /24 подсети должно быть 254 хоста (исключая network и broadcast адреса)
        self.assertEqual(mock_sock_instance.sendto.call_count, len(hosts))

        for host in hosts:
            mock_sock_instance.sendto.assert_any_call(
                bytes(MESSAGE, 'utf8'),
                (str(host), 64212)
            )


class TestScanner(unittest.TestCase):
    @patch('socket.socket')
    def test_scanner_init(self, mock_socket):
        scanner = Scanner(YOUR_IP)  # Используем ваш IP
        mock_socket.assert_called_once_with(
            socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP
        )

    @patch('socket.socket')
    def test_scanner_sniff(self, mock_socket):
        # Настраиваем mock
        mock_sock_instance = MagicMock()
        mock_socket.return_value = mock_sock_instance

        # Тестовый пакет с вашим IP
        raw_ip_header = struct.pack(
            "<BBHHHBBH4s4s",
            0x45, 0, 0, 0, 0, 0, 1, 0,
            socket.inet_aton(YOUR_IP),
            socket.inet_aton("192.168.0.1")
        )
        raw_icmp_header = struct.pack("<BBHHH", 3, 3, 0, 0, 0)
        test_packet = raw_ip_header + raw_icmp_header + bytes(MESSAGE, 'utf8')

        mock_sock_instance.recvfrom.side_effect = [
            (test_packet, (YOUR_IP, 0)),
            KeyboardInterrupt()
        ]

        scanner = Scanner(YOUR_IP)
        with self.assertRaises(SystemExit):
            scanner.sniff(YOUR_SUBNET)


if __name__ == '__main__':
    unittest.main()