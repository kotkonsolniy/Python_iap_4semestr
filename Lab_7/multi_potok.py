#многопоточность
import threading # для работы с потоками
import time
from concurrent.futures import ThreadPoolExecutor #пул потоков для параллельного выполнения задач
import requests

thread_local = threading.local() #хранилище данных кажого потокаё


def main():
    sites = [
        "https://www.yandex.ru",
        "https://bmstu.ru",
    ] * 800
    start_time = time.perf_counter()
    download_all_sites(sites)
    duration = time.perf_counter() - start_time
    print(f"Download {len(sites)} sites in {duration} seconds")

def download_all_sites(sites):
    with ThreadPoolExecutor(max_workers=5) as executor: #создает пул из 5 потоков
        executor.map(download_site, sites) #каждый поток поллуч свою часть url


def download_site(url):
    session = get_session_for_thread() #получение сессия для текущего потока
    with session.get(url) as responce:
        print(f"Read {len(responce.content)} bytes from {url}")

#создает уникальтную версию для каждого потока
def get_session_for_thread():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

if __name__ == "__main__":
    main()