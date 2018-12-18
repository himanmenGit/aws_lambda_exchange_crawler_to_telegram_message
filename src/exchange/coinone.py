import json
import os

from bs4 import BeautifulSoup as Bs4
from ..exchange.base import ExchangeBaseCrawler
from ..utils.other import COINONE

__all__ = (
    'CoinoneCrawler',
)


class CoinoneCrawler(ExchangeBaseCrawler):

    def __init__(self, url):
        super().__init__(url)
        self.filename = os.path.join('/tmp', '{}.txt'.format(COINONE))
        self.key = '{}.txt'.format(COINONE)
        self.exchange_name = '코인원'

    def parser_notice(self, html):
        soup = Bs4(html, 'html.parser')
        pre = soup.select_one(
            'body > pre'
        )
        html = pre.text
        json_val = json.loads(html)
        notices = json_val.get('results')

        for notice in notices:
            title = notice.get('title')
            url = 'https://coinone.co.kr/talk/notice/detail/{}'.format(notice.get('id'))
            self.current_notice_list.append('<a href="{}">{}</a>'.format(url, self.to_html(title)))
