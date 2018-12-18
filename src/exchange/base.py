import requests
import telegram

from src.utils.webdriver_wrapper import WebDriverWrapper
from ..utils import S3Controller

__all__ = (
    'ExchangeBaseCrawler'
)


class ExchangeBaseCrawler:
    def __init__(self, url):
        self.s3 = S3Controller()

        self.crawl_url = url

        self.exchange_name = None
        self.new_notice_list = list()
        self.current_notice_list = list()

        self.key = None
        self.filename = None
        self.method = None
        self.selenium = False
        self.wait_selector = None

    def start(self):
        html = self.process()
        self.parser_notice(html)
        self.check_new()

    def process(self):
        if not self.selenium:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
            }

            if self.method == 'post':
                html = requests.post(self.crawl_url, headers=headers).text
            else:
                html = requests.get(self.crawl_url, headers=headers).text
            return html
        else:
            driver = WebDriverWrapper()
            html = driver.get(self.crawl_url, self.wait_selector)
            driver.close()
            return html

    def check_new(self):
        if self.s3.download(self.key, self.filename):
            with open(self.filename, 'r') as f:
                self.set_new_notice_list(f.read())
            if self.set_new_notice_s3():
                self.send_tg()
        else:
            self.new_notice_list = self.current_notice_list
            self.set_new_notice_s3()

    def set_new_notice_list(self, old_notice_list):
        old_notice_list = old_notice_list.split('\n')
        for current_notice in self.current_notice_list:
            if current_notice not in old_notice_list:
                self.new_notice_list.append(current_notice)

    def set_new_notice_s3(self):
        if self.make_file():
            if self.s3.upload(self.filename, self.key):
                return True
        return False

    def send_tg(self):
        token = '<텔레그램 봇 API 키>'
        chat_id = '<텔레그램 채널 링크>'
        for notice in self.new_notice_list:
            bot = telegram.Bot(token=token)
            chat_id = chat_id
            bot.sendMessage(chat_id=chat_id, text=self.to_str(notice),
                            parse_mode=telegram.ParseMode.HTML,
                            disable_web_page_preview=True
                            )

    def make_file(self):
        try:
            if self.new_notice_list:
                with open(self.filename, 'wt') as f:
                    for notice in self.current_notice_list:
                        f.write('{}\n'.format(notice))
                    return True
            return False
        except Exception as e:
            print('make_file.error:', e)
            return False

    def to_str(self, notice):
        import datetime
        now = datetime.datetime.now() + datetime.timedelta(hours=9)
        base_str = '<b>{}</b> - {}\n{}'
        message = base_str.format(self.to_html(self.exchange_name), notice, now.strftime('%Y-%m-%d %H:%M:%S'))
        return message

    @staticmethod
    def to_html(text):
        import html
        return html.escape(text)
