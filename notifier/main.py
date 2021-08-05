import logging
from reminder import start_reminder

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

log = logging.getLogger()

if __name__ == "__main__":
    try:
        start_reminder()
    except Exception as e:
        log.exception(e)
