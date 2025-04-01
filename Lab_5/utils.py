# utils.py
import logging
import argparse


def setup_logging(log_file='scanner.log'):
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),  # Логи в файл
            logging.StreamHandler()  # Логи в консоль
        ]
    )
    return logging.getLogger()


def parse_arguments():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(description="Network scanner")
    parser.add_argument('--host', type=str, default='192.168.119.176',
                       help='Host to scan from')
    parser.add_argument('--subnet', type=str, default='192.168.119.0/24',
                       help='Subnet to scan')
    parser.add_argument('--log', type=str, default='scanner.log',
                       help='Log file name')
    return parser.parse_args()