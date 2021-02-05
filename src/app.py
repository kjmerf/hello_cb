from datetime import datetime
from datetime import timedelta
import logging
import os

from coinbase.wallet.client import Client

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

# https://developers.coinbase.com/api/v2


class CBT:
    def __init__(self, api_key, api_secret, currency, lookback):

        self.api_key = api_key
        self.api_secret = api_secret
        self.currency = currency
        self.lookback = lookback
        self.current_spot_price = None
        self.historical_spot_prices = []
        self.moving_average = None

    def yield_dates(self):

        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=self.lookback)
        delta = end_date - start_date
        for i in range(delta.days):
            yield start_date + timedelta(days=i)

    def get_client(self):

        logging.info("Getting an instance of the Coinbase client...")
        self.client = Client(self.api_key, self.api_secret)
        return self.client

    def get_current_spot_price(self):

        logging.info(f"Getting the current {self.currency} spot price...")
        response = self.client.get_spot_price(currency_pair=f"{self.currency}-USD")
        self.current_spot_price = float(response["amount"])
        return self.current_spot_price

    def get_historical_spot_prices(self):

        for date in self.yield_dates():
            date = date.strftime("%Y-%m-%d")
            logging.info(f"Getting the {self.currency} spot price for {date}...")
            response = self.client.get_spot_price(
                currency_pair=f"{currency}-USD", date=date
            )
            self.historical_spot_prices.append(float(response["amount"]))
        return self.historical_spot_prices

    def get_moving_average(self):

        self.moving_average = round(
            sum(self.historical_spot_prices) / len(self.historical_spot_prices), 2
        )
        return self.moving_average


if __name__ == "__main__":

    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    currency = os.getenv("CURRENCY")
    lookback = int(os.getenv("LOOKBACK"))

    bot = CBT(api_key, api_secret, currency, lookback)
    bot.get_client()
    bot.get_current_spot_price()
    bot.get_historical_spot_prices()
    bot.get_moving_average()

    logging.info(f"The current spot price is {bot.current_spot_price}.")
    logging.info(f"The {bot.lookback} day moving average is {bot.moving_average}.")
