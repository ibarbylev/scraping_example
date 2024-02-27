import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCHEDULE = [
    # {
    #     'script': 'test_appmagic',
    #     # filename will be hashed into random-looking string
    #     'filename': 'appmagic',
    #     # https://crontab.guru/
    #     'when': '* * * * *',
    # },
    {
        'script': 'test_kazanexpress',
        # filename will be hashed into random-looking string
        'filename': 'kazanexpress',
        # https://crontab.guru/
        'when': '* * * * *',
    },
    # {
    #     'script': 'test_kazanexpress_drop',
    #     # filename will be hashed into random-looking string
    #     'filename': 'kazanexpress_drop',
    #     # https://crontab.guru/
    #     # 'when': '0 3 * * *',
    #     'when': '* * * * *',
    # },
    # {
    #     'script': 'test_mail_ru',
    #     # filename will be hashed into random-looking string
    #     'filename': 'mail_ru',
    #     # https://crontab.guru/
    #     'when': '0 * * * *',
    # },
    # {
    #     'script': 'test_mail_ru',
    #     # filename will be hashed into random-looking string
    #     'filename': 'mail_ru',
    #     # https://crontab.guru/
    #     'when': '0 * * * *',
    # },
    # {
    #     'script': 'test_sp500',
    #     # filename will be hashed into random-looking string
    #     'filename': 'sp500',
    #     # https://crontab.guru/
    #     'when': '0 * * * *',
    # },
    # {
    #     'script': 'test_irr',
    #     # filename will be hashed into random-looking string
    #     'filename': 'irr',
    #     # https://crontab.guru/
    #     'when': '0 * * * *',
    # },
]

OUT_DIR = os.path.join(os.path.dirname(BASE_DIR), 'media', 'scraping')
