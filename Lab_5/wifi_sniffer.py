import ipaddress
import sys
import ipaddress
import socket
import os
import struct
import threading
import time

# сканируем подсеть
SUBNET = '192.168.0.0/24'
# волшебная строка, которую мы будем искать в ICMP ответах
MESSAGE = 'BMSTU'


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

        # сопоставляем константы протоколов с их названиями
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as e:
            print('%s No protocol for %s' % (e, self.protocol_num))
            self.protocol = str(self.protocol_num)


class ICMP:
    def __init__(self, buff=None):
        header = struct.unpack("<BBHHH", buff)
        self.type = header[0]
        self.code = header[1]
        self.sum = header[2]
        self.id = header[3]
        self.seq = header[4]


# эта функция добавляет в UDP-датаграммы наше волшебное сообщение
def udp_sender():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sender:
        for ip in ipaddress.ip_network(SUBNET).hosts():
            sender.sendto(bytes(MESSAGE, 'utf8'), (str(ip), 64212))


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

    def sniff(self):
        hosts_up = set([f'(str(self.hosts)) *'])
        try:
            while True:
                # читаем пакет
                raw_buffer = self.socket.recvfrom(65535)[0]
                # создаём IP-заголовок из первых 20 байт
                ip_header = IP(raw_buffer[0:20])
                # нас интересуют ICMP
                if ip_header.protocol == "ICMP":
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + 8]
                    icmp_header = ICMP(buf)
                    # ищем тип и код 3
                    if icmp_header.code == 3 and icmp_header.type == 3:
                        if ipaddress.ip_address(
                                ip_header.src_address
                        ) in ipaddress.IPv4Network(SUBNET):
                            # проверяем, содержит ди буфер наше волшебное сообщение
                            if raw_buffer[len(raw_buffer) - len(MESSAGE):
                               ] == bytes(MESSAGE, 'utf8'):
                                tgt = str(ip_header.src_address)
                                if tgt != self.host and tgt not in hosts_up:
                                    hosts_up.add(str(ip_header.src_address))
                                    print(f'Host Up: {tgt}')

        except KeyboardInterrupt:
            # если мы в виндоус, то отключаем неизбирательный режим
            if os.name == 'nt':
                self.socket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

            print('\nUser interrupted.')

        if hosts_up:
            print(f'\n\nSunnary: Hosts up on {SUBNET}')
        for host in sorted(hosts_up):
            print(f'{host}')
        print('')
        sys.exit()



if __name__ == '__main__':
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = '192.168.0.102'
        # host - '192.168.56.1'
    s = Scanner(host)

    time.sleep(1)
    t = threading.Thread(target=udp_sender)
    t.start()
    s.sniff()
