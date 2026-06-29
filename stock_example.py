from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yfinance as yf

CHART_DIR = Path(__file__).resolve().parent / "charts"
CHART_DIR.mkdir(exist_ok=True)


def fetch_stock_data(ticker_symbol: str = "LMT", period: str = "1y"):
    ticker = yf.Ticker(ticker_symbol)
    return ticker.history(period=period)


def add_moving_averages(df):
    df["50_MA"] = df["Close"].rolling(window=50).mean()
    df["200_MA"] = df["Close"].rolling(window=200).mean()
    return df


def plot_stock_data(df, ticker_symbol: str = "LMT", output_name: str | None = None):
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df["Close"], label=f"{ticker_symbol} Close", color="royalblue", linewidth=1.6)
    plt.plot(df.index, df["50_MA"], label="50-Day MA", color="orange", linewidth=1.2, linestyle="--")
    plt.plot(df.index, df["200_MA"], label="200-Day MA", color="firebrick", linewidth=1.2, linestyle=":")
    plt.title(f"{ticker_symbol} Price Trend with Moving Averages", fontsize=14, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(alpha=0.3)
    plt.legend(loc="best")

    output_path = CHART_DIR / (output_name or f"{ticker_symbol}_moving_averages.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved chart to {output_path}")
    plt.close()


def plot_comparison(dfs):
    plt.figure(figsize=(14, 7))
    colors = {"LMT": "royalblue", "NOC": "darkorange", "BA": "forestgreen"}

    for ticker_symbol, df in dfs.items():
        plt.plot(df.index, df["Close"], label=f"{ticker_symbol} Close", color=colors.get(ticker_symbol, "gray"), linewidth=1.4)
        plt.plot(df.index, df["50_MA"], label=f"{ticker_symbol} 50-Day MA", color=colors.get(ticker_symbol, "gray"), linestyle="--", linewidth=1.0, alpha=0.85)
        plt.plot(df.index, df["200_MA"], label=f"{ticker_symbol} 200-Day MA", color=colors.get(ticker_symbol, "gray"), linestyle=":", linewidth=1.0, alpha=0.75)

    plt.title("Aerospace Company Comparison", fontsize=15, fontweight="bold")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(alpha=0.3)
    plt.legend(loc="best", ncol=2)

    output_path = CHART_DIR / "comparison_aerospace.png"
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved comparison chart to {output_path}")
    plt.close()


if __name__ == "__main__":
    tickers = ["LMT", "NOC", "BA"]
    data_by_ticker = {}

    for ticker_symbol in tickers:
        df = fetch_stock_data(ticker_symbol)
        df = add_moving_averages(df)
        print(df.head())
        print(f"\nLoaded {len(df)} rows for {ticker_symbol}")
        print("\nColumns:", df.columns.tolist())
        plot_stock_data(df, ticker_symbol)
        data_by_ticker[ticker_symbol] = df

    plot_comparison(data_by_ticker)
