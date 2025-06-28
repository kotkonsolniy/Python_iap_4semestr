import ipaddress

def find_subnet(ip_str, mask_str):
    # Формируем сеть из IP и маски
    network = ipaddress.ip_network(f"{ip_str}/{mask_str}", strict=False)
    return network

if __name__ == '__main__':
    ip = input("Введите IP-адрес: ")
    mask = input("Введите маску подсети (например, 24 или 255.255.255.0): ")

    # Если маска в форме 255.255.255.0, преобразуем в префикс
    try:
        # Если маска числом (префикс)
        prefix = int(mask)
    except ValueError:
        # Если маска в формате 255.255.255.0
        prefix = ipaddress.IPv4Network(f"0.0.0.0/{mask}").prefixlen

    subnet = find_subnet(ip, prefix)
    print(f"Подсеть для IP {ip} с маской {mask}: {subnet}")
