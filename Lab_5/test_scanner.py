import unittest
from unittest.mock import patch, MagicMock
import io
import sys
import ipaddress
import socket
import struct
import logging
from scanner import IP, ICMP, Scanner, udp_sender, MESSAGE  # Импортируем ваш код


class TestIP(unittest.TestCase):
    def setUp(self):
        # Создаем фиктивный IP-заголовок (20 байт)
        self.ip_header = struct.pack(
            "<BBHHHBBH4s4s",
            0x45,  # ver=4, ihl=5
            0,  # tos
            20,  # total length
            0,  # id
            0,  # offset
            64,  # ttl
            1,  # protocol (ICMP)
            0,  # checksum
            socket.inet_aton("192.168.1.1"),  # src
            socket.inet_aton("192.168.1.2")  # dst
        )

    def test_ip_initialization(self):
        ip = IP(self.ip_header)
        self.assertEqual(ip.ver, 4)
        self.assertEqual(ip.ihl, 5)
        self.assertEqual(ip.protocol, "ICMP")
        self.assertEqual(str(ip.src_address), "192.168.1.1")
        self.assertEqual(str(ip.dst_address), "192.168.1.2")

    def test_unknown_protocol(self):
        # Меняем протокол на неизвестный (99)
        bad_header = self.ip_header[:9] + bytes([99]) + self.ip_header[10:]
        ip = IP(bad_header)
        self.assertEqual(ip.protocol, "99")


class TestICMP(unittest.TestCase):
    def setUp(self):
        # Создаем фиктивный ICMP-заголовок (8 байт)
        self.icmp_header = struct.pack("<BBHHH", 3, 3, 0, 12345, 0)

    def test_icmp_initialization(self):
        icmp = ICMP(self.icmp_header)
        self.assertEqual(icmp.type, 3)
        self.assertEqual(icmp.code, 3)
        self.assertEqual(icmp.id, 12345)


class TestUDPSender(unittest.TestCase):
    @patch('socket.socket')
    def test_udp_sender(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock

        subnet = "192.168.1.0/24"
        udp_sender(subnet)

        # Проверяем, что сокет был создан и закрыт
        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_DGRAM)
        mock_sock.__enter__.assert_called_once()

        # Проверяем, что sendto вызывался для каждого хоста в подсети
        network = ipaddress.ip_network(subnet)
        self.assertEqual(mock_sock.sendto.call_count, len(list(network.hosts())))


class TestScanner(unittest.TestCase):
    @patch('socket.socket')
    def test_scanner_initialization(self, mock_socket):
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock

        scanner = Scanner("192.168.1.1")

        mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        mock_sock.bind.assert_called_once_with(("192.168.1.1", 0))
        mock_sock.setsockopt.assert_called_once_with(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    @patch('socket.socket')
    @patch('builtins.print')
    def test_sniff(self, mock_print, mock_socket):
        # Настраиваем мок сокета
        mock_sock = MagicMock()
        mock_socket.return_value = mock_sock

        # Создаем фиктивный ответ ICMP (тип 3, код 3)
        icmp_header = struct.pack("<BBHHH", 3, 3, 0, 12345, 0)
        ip_header = struct.pack(
            "<BBHHHBBH4s4s",
            0x45, 0, 20 + len(icmp_header) + len(MESSAGE), 0, 0, 64, 1, 0,
            socket.inet_aton("192.168.1.100"), socket.inet_aton("192.168.1.1")
        )
        raw_buffer = ip_header + icmp_header + MESSAGE.encode('utf8')

        # Настраиваем recvfrom для возврата нашего фиктивного пакета
        mock_sock.recvfrom.return_value = (raw_buffer, ("192.168.1.100", 0))

        scanner = Scanner("192.168.1.1")

        # Запускаем sniff в отдельном потоке с таймаутом
        import threading
        def run_sniff():
            scanner.sniff("192.168.1.0/24")

        thread = threading.Thread(target=run_sniff)
        thread.daemon = True
        thread.start()
        thread.join(timeout=1)  # Ждем не более 1 секунды

        # Проверяем, что хост был обнаружен
        mock_print.assert_any_call('Host Up: 192.168.1.100')


class TestIntegration(unittest.TestCase):
    @patch('scanner.Scanner')
    @patch('scanner.udp_sender')
    @patch('scanner.threading.Thread')
    def test_main(self, mock_thread, mock_udp_sender, mock_scanner):
        # Мокаем sys.argv
        with patch('sys.argv', ['scanner.py', '--host', '192.168.1.1', '--subnet', '192.168.1.0/24']):
            # Импортируем и запускаем main
            import scanner
            if hasattr(scanner, '__main__'):
                scanner.__main__()

        # Проверяем, что Scanner был создан с правильными параметрами
        mock_scanner.assert_called_once_with('192.168.1.1')

        # Проверяем, что udp_sender был запущен в отдельном потоке
        mock_thread.assert_called_once_with(target=mock_udp_sender, args=('192.168.1.0/24',))


if __name__ == '__main__':
    # Настраиваем логирование для тестов
    logging.basicConfig(level=logging.CRITICAL)  # Отключаем логи во время тестов
    unittest.main()