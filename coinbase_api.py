from datetime import datetime, timedelta
import pandas as pd
import json
import requests
def get_crypto_data(product_id, start_date, end_date, granularity):
  # Mount URL
  url = f"https://api.exchange.coinbase.com/products/{product_id}/candles"
  print(url)

  # Delta is the increment in time from one candle to another
  delta = timedelta(seconds=granularity)

  # Coinbase's limitation
  max_candles = 300

  # Start from the last second of last day to prevent duplications
  current_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S') - timedelta(seconds=1)
  end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S') - timedelta(seconds=1)

  # We'll add results in each iteration to this list
  results = []

  # Iterate over interval
  while current_date < end_date:
    # Get next date. It's the current date + increment if still within the interval,
    # else it's the end date
    next_date = current_date + max_candles * delta
    next_date = next_date if next_date < end_date else end_date

    # Make sure to pass dates as ISO
    params = {
        "start": current_date.isoformat(),
        "end": next_date.isoformat(),
        "granularity": granularity
    }

    headers = {"content-type": "application/json"}

    data = requests.get(url, params=params, headers=headers)
    data = data.json()

    # Make sure to add more recent data to the top of the list
    results = data + results

    # Update cursor
    current_date = next_date
  
  columns = ['timestamp', "low", "high", "open", "close", "volume"]

  # Create a dataframe with results
  df = pd.DataFrame(data=results, columns=columns)

  # Create datetime column, set it as index and drop timestamp column
  # df['datetime'] = df['timestamp'],
  # df.set_index('datetime', inplace=True)
  # df.drop('timestamp', axis=1, inplace=True)
  dict = df.to_dict(orient='index')
  
  return json.dumps(dict)

if __name__ == "__main__":
  print(get_crypto_data(
  product_id="BTC-USD",
  start_date="2024-04-20T10:59:59",
  end_date="2024-04-20T11:19:05",
  granularity=900
)
  )