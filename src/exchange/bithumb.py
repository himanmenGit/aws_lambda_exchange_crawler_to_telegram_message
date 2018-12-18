import os
import re

from bs4 import BeautifulSoup as Bs4

from ..exchange.base import ExchangeBaseCrawler
from ..utils.other import BITHUMB

__all__ = (
    'BithumbCrawler',
)


class BithumbCrawler(ExchangeBaseCrawler):

    def __init__(self, url):
        super().__init__(url)
        self.filename = os.path.join('/tmp', '{}.txt'.format(BITHUMB))
        self.key = '{}.txt'.format(BITHUMB)
        self.exchange_name = '빗썸'

    def parser_notice(self, html):
        soup = Bs4(html, 'html.parser')
        notices = soup.select(
            '#content  > div:nth-of-type(2) > div:nth-of-type(1) > div > table > tbody > tr > td.board-title > span')
        pks = soup.select('#content > div:nth-of-type(2) > div:nth-of-type(1) > div > table > tbody > tr')

        for index, pk in enumerate(pks):
            title = notices[index].text
            url = 'https://cafe.bithumb.com/view/board-contents/' + re.findall("'([a-zA-Z0-9,\s]*)'", pk['onclick'])[0]
            self.current_notice_list.append('<a href="{}">{}</a>'.format(url, self.to_html(title)))
