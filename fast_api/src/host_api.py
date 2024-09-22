from fastapi import FastAPI

import yfinance
import uvicorn

app = FastAPI()


# This is the root path of the API, what will be displayed when you access the API
@app.get("/")
async def root():
    return {"message": "Welcome to QuantFI API!"}


# This is the path that will return the data of a specific stock
@app.get("/{ticker}")
async def get_data(ticker: str = "AAPL"):
    data = yfinance.download(ticker)
    return data.to_dict()


# This is the path that will return the indicators data of a specific stock
@app.get("/indicators/{ticker}")
async def add_technical_indicators(ticker: str):
    data = yfinance.download(ticker)
    indicators = {
        "MA": data["Close"].rolling(window=50).mean().fillna(0).tolist(),
        "RSI": compute_rsi(data["Close"]).fillna(0).tolist(),
    }
    return indicators


# Auxiliary function to calculate the RSI
def compute_rsi(series, periods=14):
    delta = series.diff(1)
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def run_server():
    print('Connecting to server...')

    uvicorn.run(app, host="0.0.0.0", port=8001)

# Run the server
if __name__ == "__main__":
    run_server()
