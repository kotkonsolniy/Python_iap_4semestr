# синхронный
import time #замер времени исполнения
import requests #для http запросов

def main():
    sites = [
        "https://www.yandex.ru",
        "https://bmstu.ru",
    ] * 800 #создается 1600 сайтов
    start_time = time.perf_counter()
    download_all_sites(sites)
    duration = time.perf_counter() - start_time
    print(f"Download {len(sites)} sites in {duration} seconds")

def download_all_sites(sites):
    with requests.Session()as session:
        for url in sites:
            download_site(url, session)

def download_site(url, session):
    with session.get(url) as responce: #выполняется гет запрос
        print(f"Read {len(responce.content)} bytes from {url}") #инфа о колве загруженных байт

if __name__ == "__main__":
    main()

#каждый запрос ждет завершения предыдущего