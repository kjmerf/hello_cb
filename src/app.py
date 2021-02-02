from datetime import datetime
from datetime import timedelta
import os

from coinbase.wallet.client import Client

if __name__ == "__main__":

    # https://developers.coinbase.com/api/v2

    client = Client(os.getenv("CB_API_KEY"), os.getenv("CB_API_SECRET"))
    currency = os.getenv('CURRENCY')
    today = datetime.today()

    for i in range(int(os.getenv("DAYS"))):
        dt = today - timedelta(days=i)
        dt = dt.strftime('%Y-%m-%d')
        response = client.get_spot_price(currency_pair=f"{currency}-USD", date=dt)
        price = response["amount"]
        if i == 0:
            print(f"The current spot price of {currency} is {price}")
        else:
            print(f"The spot price of {currency} on {dt} was {price}")
