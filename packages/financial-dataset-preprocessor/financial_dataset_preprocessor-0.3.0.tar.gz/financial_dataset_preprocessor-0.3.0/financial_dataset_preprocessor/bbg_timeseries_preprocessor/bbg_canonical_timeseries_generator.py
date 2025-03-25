from financial_dataset_loader import load_index, load_currency
from financial_dataset_preprocessor.timeseries_basis import extend_timeseries_by_all_dates

def get_preprocessed_timeseries_of_bbg_index(ticker_bbg_index):
    df = load_index(ticker_bbg_index=ticker_bbg_index)
    df_extended = extend_timeseries_by_all_dates(df)
    return (
        df_extended
        .rename(columns={'date': ticker_bbg_index})
    )
    

def get_preprocessed_timeseries_of_bbg_currency(ticker_bbg_currency):
    df = load_currency(ticker_bbg_currency=ticker_bbg_currency)
    df_extended = extend_timeseries_by_all_dates(df)
    return (
        df_extended
        .rename(columns={'date': ticker_bbg_currency})
    )