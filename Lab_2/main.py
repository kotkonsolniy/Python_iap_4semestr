import socket
import os

# Узел для прослдушивания
HOST = '192.168.0.103' # Берем активный адрес

def main():
    # Создаем сырой сокет и привязываем к общедоступному интерфейсу
    if os.name == 'nt':
        socket.protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

    # Делаем так, чтобы захватывался IP-заголовок
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    # Читаем один пакет
    print(sniffer.recvfrom(65565))

    # # Если мы в Windows, выключаем неизбирательный режим
    # if os.name = 'nt':
    #     sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


if __name__ == '__main__':
    main()
