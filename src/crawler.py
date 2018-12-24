from src.exchange.bithumb import BithumbCrawler
from src.exchange.coinone import CoinoneCrawler

from src.utils import (
    BITHUMB, COINONE
)


def crawler_func(event, context):
    print(event)
    site = event.get('site', BITHUMB)
    crawler = None
    if site == BITHUMB:
        crawler = BithumbCrawler('https://cafe.bithumb.com/')
    elif site == COINONE:
        crawler = CoinoneCrawler('https://coinone.co.kr/api/talk/notice/?ordering=-created_at')
        crawler.selenium = True
        crawler.wait_selector = "body > pre"
    crawler.start()

    return site
