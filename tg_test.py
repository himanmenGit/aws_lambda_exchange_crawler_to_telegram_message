import telegram


def main():
    with open('.aws.env', 'r') as f:
        lines = f.readlines()
        env = dict(s.rstrip().split('=') for s in lines)
        token = env.get('TG_BOT_API_KEY')
        chat_id = env.get('TG_CHANNEL_LINK')
        bot = telegram.Bot(token=token)
        chat_id = chat_id
        bot.sendMessage(chat_id=chat_id, text='<b>안녕하세요?</b>',
                        parse_mode=telegram.ParseMode.HTML,
                        disable_web_page_preview=True
                        )


if __name__ == '__main__':
    main()
