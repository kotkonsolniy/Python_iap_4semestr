import socket

IP = '0.0.0.0'
PORT = 13377


def main():
    # Создаем UDP сокет
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Привязываем сокет к адресу и порту
    sock.bind((IP, PORT))
    print(f'[*] Listening on {IP}: {PORT}')
    while True:
        # Получаем данные и адрес отправителя
        data, addr = sock.recvfrom(1024)  # Буфер размером 1024 байта
        print(f"Получено сообщение от {addr}: {data.decode()}")
        sock.sendto(b"ANSWER FROM SERVER", addr)


if __name__ == '__main__':
    main()
