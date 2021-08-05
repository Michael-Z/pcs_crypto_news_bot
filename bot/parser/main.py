import requests
from config import CRYPTOPANIC_TOKEN, COINMARKETCAP_TOKEN
import logging
from bs4 import BeautifulSoup
import re


class CryptoPanic:
    """Data getter for cryptopanic.com ."""

    def __init__(self):
        self.url = f'https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTOPANIC_TOKEN}'
        self.limit_news = 5

    def _request(self, news_type: str):
        """
        Send request to API.
        Returns:
          json data
        """
        params = {
            'kind': 'news',
            'filter': news_type,
        }
        logging.info(f'Requested: {news_type}')
        return requests.request('GET', self.url, params=params).json()

    def format_data(self, news_type: str):
        """From a message for bot."""
        data = self._request(news_type)
        text = "📰Today in Crypto"
        if news_type == 'hot':
            text += ' 🔥News\n\n'
        elif news_type == 'bullish':
            text += ' 📈<News\n\n'
        elif news_type == 'bearish':
            text += ' 📉News\n\n'
        elif news_type == 'important':
            text += ' ❗News'
        for i in data['results']:
            if self.limit_news:
                text += f"{i['title']}\n"
                text += f"<a href=\"{i['url']}\">link</a>\n\n"
            else:
                break
            self.limit_news -= 1
        return text


class CoinMarketCap:
    def __init__(self):
        self.api_url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.bs_url = 'https://coinmarketcap.com'
        self.limit_positions = 5

    def _request(self, crypto_type: str):
        """
        Send request to API.
        Returns:
          json data
        """

        params = {
            'aux': 'cmc_rank',
            'limit': 100,
            'sort': 'market_cap',
            'volume_24h_min': 50000,
        }
        headers = {
            'X-CMC_PRO_API_KEY': COINMARKETCAP_TOKEN
        }

        data = requests.request('GET', self.api_url, headers=headers, params=params).json()['data']
        if crypto_type == 'losers':
            data = sorted(data, key=lambda x: x['quote']['USD']['percent_change_24h'], reverse=False)[:5]

        elif crypto_type == 'gainers':
            data = sorted(data, key=lambda x: x['quote']['USD']['percent_change_24h'], reverse=True)[:5]

        return data

    def _parse(self, param: str):
        """Parse trending coins page."""
        html = requests.request('GET', self.bs_url).text
        soup = BeautifulSoup(html, 'html.parser')
        res = []
        if not param == 'stats':
            for pos in soup.tbody.find_all('tr'):
                if self.limit_positions:
                    title = pos.find(class_='iJjGCS').get_text()
                    coin_symbol = pos.find(class_='coin-item-symbol').get_text()
                    td = pos.find_all('td')
                    percent_change = td[4].get_text()
                    volume = td[-3].get_text()
                    res.append(f'{title} ${coin_symbol} | {percent_change} Volume (24h): {volume}\n')
                else:
                    break
                self.limit_positions -= 1
        else:
            data = soup.find_all(class_='cVPJov')
            market_cap = data[2].get_text()
            pattern = re.compile(r'BTC: (?P<percent>\d+.\d+%)')
            dominance = f"BTC Dominance: {pattern.search(data[4].get_text()).group('percent')}"
            volume = data[3].get_text()
            res.extend([f'{market_cap}\n', f'{dominance}\n', f'{volume}\n'])

        return res

    def format_data(self, param: str):
        """"""
        text = ''
        if param in ['losers', 'gainers']:
            if param == 'losers':
                text = '📉'
            else:
                text = '📈'
            text += f'{param.capitalize()} in Top 100 (24h)\n\n'
            data = self._request(param)
            data = [(x['name'], x['symbol'], x['quote']['USD']['percent_change_24h'], x['quote']['USD']['price']) for x in data]
            for pos in data:
                text += f"{ pos[0]} ${pos[1]} | {round(pos[2], 2)}%, ${float(pos[3])}\n\n"
        elif param == 'trending':
            data = self._parse(param)
            text = 'Trending📊\n\n'
            text += ''.join(data)
        elif param == 'stats':
            data = self._parse(param)
            text += '<b>Crypto Market Stats</b>  👀\n'
            text += ''.join(data)
        return text
