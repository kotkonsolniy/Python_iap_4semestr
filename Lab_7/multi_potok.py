import threading
import time
from concurrent.futures import ThreadPoolExecutor

import requests

thread_local = threading.local()


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
    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(download_site, sites)


def download_site(url):
    session = get_session_for_thread()
    with session.get(url) as responce:
        print(f"Read {len(responce.content)} bytes from {url}")

def get_session_for_thread():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

if __name__ == "__main__":
    main()