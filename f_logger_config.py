import logging
import logging.handlers
import os
from pathlib import Path

# مسیر پوشه لاگ‌ها (logs) در ریشه پروژه
LOG_DIR = Path(__file__).parent.parent / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

def get_logger(name: str, level=logging.INFO, log_to_file=True):
    """
    ساخت و بازگشت لاگر با نام مشخص.
    لاگ‌ها به کنسول و به فایل در پوشه logs ذخیره می‌شوند.
    
    پارامترها:
    - name: نام لاگر (معمولاً نام ماژول یا بخش)
    - level: سطح لاگ (مثلاً logging.INFO، logging.DEBUG)
    - log_to_file: اگر True باشد لاگ‌ها به فایل هم ذخیره می‌شوند
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # جلوگیری از اضافه شدن چندباره هندلرها
    if not logger.hasHandlers():
        # لاگ کنسول
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        if log_to_file:
            # لاگ فایل با چرخش روزانه و نگهداری ۷ روز
            fh = logging.handlers.TimedRotatingFileHandler(
                filename=LOG_DIR / f'{name}.log',
                when='midnight',
                backupCount=7,
                encoding='utf-8'
            )
            fh.setLevel(level)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

    return logger
