# hello_cb

This purpose of this repo is to explore the Coinbase API.

## Setup

To use the repo, you first need to create a Coinbase account.
Then create an API key associated with the account and set the following environment variables accordingly:
```CB_API_KEY``` and ```CB_API_SECRET```.

## Running locally

Once the setup is complete, simply run ```/up.sh``` to start the bot.
The bot does access the Coinbase API but does not buy or sell any crypto.

## Thoughts

We should also check Coinbase Pro: https://docs.pro.coinbase.com/.
The API may be more complex to use as there is no official Python library, but Coinbase Pro charges signficantly less in fees.
