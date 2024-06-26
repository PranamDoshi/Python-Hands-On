from loggers import Logger
logger = Logger().get_logger('main')

import configuration

import quantstats as qs
qs.extend_pandas()

import pandas as pd
import yfinance as yf
import traceback

def read_stock_returns_data(tickers: list[str], start_date: str = None, end_date: str = None, period: str = None)-> pd.DataFrame:
    logger.info("Downloading {} data for {}".format(
        tickers, f"{start_date}-{end_date}" if start_date and end_date else period
    ))

    if start_date and end_date:
        return yf.download(tickers, start=start_date, end=end_date)['Close'].fillna(0)

    elif period:
        return yf.download(tickers, period=period, raise_errors=True)['Close'].fillna(0)

    else:
        raise RuntimeError(f"Either period or stard_date and end_date are required!")

def main(
    benchmark: str, tickers: list[str], rf: float, mutual_fund: str = None, **kwargs
)-> str:
    # output_file = f"{configuration.parent_path}/Strategy.html"

    try:
        benchmark_data = read_stock_returns_data([benchmark], **kwargs).to_frame(name='Benchmark')
        logger.info(benchmark_data)
    except Exception as e:
        logger.error(f"Couldn't download the Returns Data of Nifty for provided timeline! Error: {traceback.format_exc()}")
        raise RuntimeError(f"Couldn't download the Returns Data of Nifty for provided timeline!")

    try:
        stocks_data = read_stock_returns_data(tickers, **kwargs)
        logger.info(stocks_data)
    except Exception as e:
        logger.error(f"Couldn't download the Returns Data of {', '.join(tickers)} for provided timeline! Error: {traceback.format_exc()}")
        raise RuntimeError(f"Couldn't download the Returns Data of {', '.join(tickers)} for provided timeline!")
    
    if mutual_fund:
        try:
            mutual_funds_data = read_stock_returns_data(mutual_fund, **kwargs).to_frame(name='Mutual Fund')
            logger.info(mutual_funds_data)
            logger.info(mutual_funds_data.columns)
            # mutual_funds_data['Mutual Fund'] = mutual_funds_data['Close']
            # mutual_funds_data.drop('Close')
            # logger.info(mutual_funds_data)
        except Exception as e:
            logger.error(f"Couldn't download the Returns Data of {', '.join(tickers)} for provided timeline! Error: {traceback.format_exc()}")
            raise RuntimeError(f"Couldn't download the Returns Data of {', '.join(tickers)} for provided timeline!")
    else:
        mutual_funds_data = None

    try:
        if len(tickers) > 1:
            merged_stocks_data = stocks_data.mean(axis=1).to_frame(name='Stocks Portfolio')
        else:
            merged_stocks_data = stocks_data.to_frame(name='Stocks Portfolio')

        logger.info(merged_stocks_data)
        logger.info(merged_stocks_data.columns)

        if mutual_funds_data is not None:
            merged_data = pd.concat([merged_stocks_data, mutual_funds_data], axis=1)
            # merged_stocks_data[mutual_fund] = mutual_funds_data['Close']
            logger.info(merged_data)
            logger.info(merged_data.columns)
        else:
            merged_data = merged_stocks_data

        return qs.reports.html(merged_data, benchmark_data, rf=rf)

    except Exception as e:
        logger.error(f"Some error occured when processing your request, Please try after sometime! Error: {traceback.format_exc()}")
        raise RuntimeError(f"Some error occured when processing your request, Please try after sometime!")

    # stock1: pd.Series = qs.utils.download_returns('RELIANCE.NS')
    # logger.info(stock1.to_frame().columns)
    # stock2: pd.Series = qs.utils.download_returns('TCS.NS')
    # logger.info(stock2.to_frame().columns)

    # merged_stocks = pd.merge(stock1, stock2, left_index=True, right_index=True)
    # merged_stock_returns = merged_stocks.mean(axis=1)
    # logger.info(merged_stock_returns)

    # # qs.reports.html(pd.concat([stock1, stock2]), nifty, output='reliance&tcs.html')
    # qs.reports.html(merged_stock_returns, nifty, output='reliance&tcs.html', rf=0.0615)

def get_available_tickers()-> list[str]:
    df = pd.read_csv(configuration.NSE_BSE_Stocks_Details_File)
    return df['NSE Code'].to_list()

def get_period_values()-> list[str]:
    return [
        "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"
    ]

def get_benchmark_indices()-> dict[str, str]:
    return {
        "Nifty 50": "^NSEI", 
        "Nifty Bank": "^NSEBANK", 
        "Nifty Midcap 100": "NIFTY_MIDCAP_100.NS",
        "Nifty Next 50": "^NSMIDCP",
        "Nifty 100": "^CNX100",
        "Nifty 200": "^CNX200",
        "NIFTY 500": "^CRSLDX",
        "Nifty Midcap 50": "^NSEMDCP50",
        "Nifty Small Cap 50": "NIFTYSMLCAP50.NS"
    }

if __name__ == "__main__":
    html_content = main(benchmark='^NSEI', tickers=["RELIANCE.NS", "TCS.NS"], rf=0.0615, mutual_fund="0P0001BA3I.BO", start_date='2024-04-30', end_date='2024-06-20')
    if html_content:
        with open(f"{configuration.parent_path}/Strategy.html", "r") as f:
            f.write(html_content)
