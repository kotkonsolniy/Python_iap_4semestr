import ipaddress  #работа с айпи адресами
import sys
import socket #работа с сетевыми соединенями
import os
import struct #распаковка бинарных заголовков ip/icmp
import threading
import time
import logging
from utils import setup_logging, parse_arguments

# Волшебная строка, которую мы будем искать в ICMP ответах(константа)
MESSAGE = 'BMSTU'

#разбираем ip заголовк пакета,  распаковывает бинарные адреса
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

        # IP-адреса, понятные человеку
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # Сопоставляем константы протоколов с их названиями
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            logging.error(f'{e} No protocol for {self.protocol_num}')
            self.protocol = str(self.protocol_num)

#разбирает ICMP заголовок
class ICMP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHH", buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]

#создает udp сокет с широковещательной рассылкой

#изначальная функция не совсем корректна, тесты сразу же падали при недоступном хосте
def udp_sender(subnet):
    logging.info(f'Starting UDP sender for subnet {subnet}')
    try:
        #сздаем udp-сокет
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # разрешаем широковещательную рассылку
        sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) #разрешение широковещательной рассылки

        #перебираем все айпи адреса подсети
        for ip in ipaddress.ip_network(subnet).hosts():
            try:
                sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 64212))
                logging.debug(f'Sent message to {ip}')
                time.sleep(0.01)  # небольшая задержка после каждой отправки
                #отсуствие задержки могло вызывать переполнение буффера
                #ошибки не прерываются а только логируются
            except Exception as e:
                #если отправка не удалась
                logging.warning(f"Failed to send to {ip}: {e}")
                continue

    except Exception as e:
        #ошибка при создании сокетаили другая критическая ошибка
        logging.error(f"UDP sender error: {e}")
    finally:
        sender.close()


#настраивает сокет для захвата пакетов
class Scanner:
    def __init__(self, host):
        self.host = host
        if os.name == 'nt':
            socket_protocol = socket.IPPROTO_IP
        else:
            socket_protocol = socket.IPPROTO_ICMP

        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_RAW, socket_protocol
        )
        self.socket.bind((host, 0))
        self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        if os.name == 'nt':
            self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
        logging.info(f'Scanner initialized on host {host}')

#захватывает сырые пакет, разюивает ip заголовки, добавляет хост в список в случае выполнения всех условий
    def sniff(self, subnet):
        hosts_up = set() #множество для хранения активных хостов
        try:
            while True:
                raw_buffer = self.socket.recvfrom(65535)[0]
                ip_header = IP(raw_buffer[0:20])
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(ip_header.src_address) in ipaddress.IPv4Network(subnet):
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):] == bytes(MESSAGE, 'utf8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    logging.info(f'Host Up: {tgt}')
                                    print(f'Host Up: {tgt}')

        except KeyboardInterrupt:
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            logging.warning('User interrupted the scan.')

        if hosts_up:
            logging.info(f'\n\nSummary: Hosts up on {subnet}')
            print(f'\n\nSummary: Hosts up on {subnet}')
            for host in sorted(hosts_up):
                logging.info(f'{host}')
                print(f'{host}')
        else:
            logging.info('No hosts found.')

        sys.exit()

#пасит аргументы строки, настраивает логирование, создает сканер, запускает udp рассылку
if __name__ == '__main__':
    args = parse_arguments()
    logger = setup_logging(args.log)
    logging.info(f'Starting scanner on host {args.host} for subnet {args.subnet}')

    s = Scanner(args.host)
    time.sleep(1)
    t = threading.Thread(target=udp_sender, args=(args.subnet,))
    t.start()
    s.sniff(args.subnet)
