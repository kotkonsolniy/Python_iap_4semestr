# sniffer.py
import ipaddress
import sys
import socket
import os
import struct
import threading
import time
from utils import setup_logging, parse_arguments
import logging

# Константы
MESSAGE = 'BMSTU'
UDP_PORT = 64212
SOCKET_TIMEOUT = 2  # seconds


class IP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHHBBH4s4s", buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF
        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            logging.error(f'{e} No protocol for {self.protocol_num}')
            self.protocol = str(self.protocol_num)


class ICMP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHH", buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]


def udp_sender(subnet):
    """Отправка UDP-пакетов на все хосты в подсети"""
    logging.info(f'Starting UDP sender for subnet {subnet}')
    sender = None
    try:
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sender.settimeout(SOCKET_TIMEOUT)

        for ip in ipaddress.ip_network(subnet).hosts():
            try:
                sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), UDP_PORT))
                logging.debug(f'Sent message to {ip}')
                time.sleep(0.01)  # Задержка для избежания перегрузки
            except socket.error as e:
                logging.warning(f"Failed to send to {ip}: {e}")
                continue
    except Exception as e:
        logging.error(f"UDP sender error: {e}")
    finally:
        if sender:
            sender.close()


class Scanner:
    def __init__(self, host):
        self.host = host
        socket_protocol = socket.IPPROTO_IP if os.name == 'nt' else socket.IPPROTO_ICMP

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        logging.info(f'Scanner initialized on host {host}')

    def sniff(self, subnet):
        """Основной цикл сканирования сети"""
        hosts_up = set()
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])

                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)

                    if (icmp_header.code == 3 and icmp_header.type == 3 and
                            ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(subnet) and
                            raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8')):

                        tgt = str(ip_header.src_address)
                        if tgt != self.host and tgt not in hosts_up:
                            hosts_up.add(tgt)
                            logging.info(f'Host Up: {tgt}')
                            print(f'Host Up: {tgt}')

        except KeyboardInterrupt:
            logging.warning('User interrupted the scan.')
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

        self._print_results(subnet, hosts_up)
        sys.exit()

    def _print_results(self, subnet, hosts_up):
        """Вывод результатов сканирования"""
        if hosts_up:
            logging.info(f'\n\nSummary: Hosts up on {subnet}')
            print(f'\n\nSummary: Hosts up on {subnet}')
            for host in sorted(hosts_up):
                logging.info(host)
                print(host)
        else:
            logging.info('No hosts found.')
        print('')


if __name__ == '__main__':
    args = parse_arguments()
    logger = setup_logging(args.log)
    logging.info(f'Starting scanner on host {args.host} for subnet {args.subnet}')

    scanner = Scanner(args.host)
    time.sleep(1)

    sender_thread = threading.Thread(target=udp_sender, args=(args.subnet,))
    sender_thread.start()

    scanner.sniff(args.subnet)