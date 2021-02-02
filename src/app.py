from datetime import datetime
from datetime import timedelta
import logging
import os
from time import sleep

from coinbase.wallet.client import Client

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)

# https://developers.coinbase.com/api/v2


class CBT:
    def __init__(self, api_key, api_secret, currency, lookback):

        self.api_key = api_key
        self.api_secret = api_secret
        self.currency = currency
        self.lookback = lookback
        self.holding = True
        self.current_spot_price = None
        self.historical_spot_prices = {}
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

        logging.info(f"Getting historical {self.currency} spot prices...")
        for date in self.yield_dates():
            date = date.strftime("%Y-%m-%d")
            if date not in self.historical_spot_prices:
                response = self.client.get_spot_price(
                    currency_pair=f"{currency}-USD", date=date
                )
                self.historical_spot_prices[date] = float(response["amount"])
        return self.historical_spot_prices

    def remove_old_prices(self):

        dates = [date.strftime("%Y-%m-%d") for date in self.yield_dates()]
        dates_to_remove = []
        for date, price in self.historical_spot_prices.items():
            if date not in dates:
                dates_to_remove.append(date)

        for date in dates_to_remove:
            self.historical_spot_prices.pop(date)

    def get_moving_average(self):

        prices = list(self.historical_spot_prices.values())
        self.moving_average = round(sum(prices) / len(prices), 2)
        return self.moving_average

    def buy(self):

        # this is just a dummy function

        if not self.holding:
            logging.info(f"Buying {bot.currency} at {bot.current_spot_price}!")
            self.holding = True
        else:
            raise Exception(f"I'm already holding {self.currency}!")

    def sell(self):

        # this is just a dummy function

        if self.holding:
            logging.info(f"Selling {bot.currency} at {bot.current_spot_price}!")
            self.holding = False
        else:
            raise Exception(f"I'm not holding any {self.currency}!")


if __name__ == "__main__":

    api_key = os.getenv("CB_API_KEY")
    api_secret = os.getenv("CB_API_SECRET")
    currency = os.getenv("CURRENCY")
    lookback = int(os.getenv("LOOKBACK"))
    sleep_seconds = int(os.getenv("SLEEP_SECONDS"))

    bot = CBT(api_key, api_secret, currency, lookback)
    bot.get_client()

    while True:

        yesterday = datetime.utcnow().date() - timedelta(days=1)

        if yesterday.strftime("%Y-%m-%d") not in bot.historical_spot_prices:
            bot.get_historical_spot_prices()
            bot.remove_old_prices()
            bot.get_moving_average()

        bot.get_current_spot_price()

        logging.info(
            f"The current spot price of {bot.currency} is {bot.current_spot_price}."
        )
        logging.info(f"The {bot.lookback} day moving average is {bot.moving_average}.")

        # from here down is just for demonstration
        # we would want to call the API to see what we're holding

        if bot.current_spot_price > bot.moving_average:
            if bot.holding:
                bot.sell()
            else:
                logging.info(
                    f"I'd sell {bot.currency} at these prices but I don't have any!"
                )
        else:
            if bot.holding:
                logging.info(
                    f"I'd buy {bot.currency} at these prices but I'm already holding!"
                )
            else:
                bot.buy()

        logging.info(f"Going to sleep for {sleep_seconds} seconds...")
        sleep(sleep_seconds)
