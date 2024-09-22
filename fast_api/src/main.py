from threading import Thread
from quixstreams import Application
import pandas as pd
import host_api  # Import your FastAPI server logic from `hostapi.py`
import requests
import time

def ingestion_1(tickers=["AAPL", "MSFT", "GOOGL", "AMZN"]):
    
    # Initialize the FastAPI server in a separate thread
    server_thread = Thread(target=host_api.run_server, daemon=True) 
    server_thread.start()

    # Wait for the server to start before making requests
    time.sleep(5)

    # URL for the API server
    api_base_url = "http://127.0.0.1:8001/"

    stock_data = []

    for ticker in tickers:
        # Make a GET request to the API to retrieve stock data
        response = requests.get(f"{api_base_url}{ticker}")
        data = response.json()
        trimmed_data = pd.DataFrame(data).head(10).to_dict()
      
        stock_data.append({
            'ticker': ticker,
            'data': trimmed_data
        })

        # Simulate a delay between requests
        #time.sleep(1)
        
    return stock_data



def redpandas_producer(stock_data: list[dict], broker: str = "localhost:9092"):
    
    app = Application(broker_address = broker)
    msg_topic = app.topic(name="OHLC", value_serializer="json")

    with app.get_producer() as producer:

        for stock in stock_data:

            kafka_msg = msg_topic.serialize(
                key = stock['ticker'], 
                value = stock['data']
            )
            producer.produce(
                topic=msg_topic.name, 
                value=kafka_msg.value,
                key=kafka_msg.key
            )
            print(f"Produced message for {stock['ticker']}")
            time.sleep(1)
    
    


if __name__ == "__main__":

    stock_data = ingestion_1()
    redpandas_producer(stock_data, broker="redpanda-0:9092")
