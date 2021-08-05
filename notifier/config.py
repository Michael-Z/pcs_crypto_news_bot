import os
from dateutil import tz
from dotenv import load_dotenv

load_dotenv()

COINMARKETCAP_TOKEN = os.getenv("COINMARKETCAP_TOKEN")
CRYPTOPANIC_TOKEN = os.getenv("CRYPTOPANIC_TOKEN")
TOKEN = os.getenv("TOKEN")
admin_id = int(os.getenv("ADMIN_ID"))
IP_WHITELIST = [int(os.getenv("ADMIN_ID"))]
host = os.getenv("PG_HOST")
PG_USER = os.getenv("PG_USER")
PG_PASS = os.getenv("PG_PASS")
PG_DATABASE = os.getenv("PG_DB")
timezone = tz.gettz('UTC')
CHANNEL_ID = os.getenv('CHANNEL_ID')
ADMINS = list(map(int, os.getenv("ADMINS").split(', ')))