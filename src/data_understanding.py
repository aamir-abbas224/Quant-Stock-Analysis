# %%
import os
import time
import pandas as pd
import yfinance as yf

# %%
nasdaq_df = pd.read_csv(
    r"C:\Users\Aamir Bin Abbas\Desktop\Research & Thesis\Stock-Price-Predictor-Close--LSTM\data\raw\nasdaq_screener_1793773127340.csv"
)

# %%
nasdaq_df.groupby(
    ["Symbol", "Name", "Sector"],
    dropna=True,
).size().reset_index()

# %%
sector_type = set()

for st in nasdaq_df["Sector"]:
    if isinstance(st, str):
        sector_type.add(st.strip())

# %%
nasdaq_df.groupby("Sector").sample(n=1)


# %%
# this function downloads datasets sector wise for EDA. it names the file according to its name in original dataframe
def get_sector_files(period: str, interval: str) -> None | int:

    count = 0  # for keeping account of data collected

    try:
        # new folder for sector wise data
        full_path = r"C:\Users\Aamir Bin Abbas\Desktop\Research & Thesis\Stock-Price-Predictor-Close--LSTM\data\raw\yahoo_finance\sector_wise_csv"

        # to make directory named 'sector_wise_csv'
        os.makedirs(full_path, exist_ok=True)

        # obtaining random sample 'Sector' wise to analyze data
        df = nasdaq_df.groupby("Sector").sample(n=1)

        # Process each selected company
        for _, row in df.iterrows():
            # Extract company info
            target_name = row["Name"]
            target_sector = row["Sector"]
            ticker = row["Symbol"]

            # validate ticker
            if not isinstance(ticker, str) or not ticker.strip():
                print(f"Invalid ticker for {target_sector}")
                continue

            # generate file names
            file_name = f"{target_name}_{target_sector}_data_file.csv".replace(" ", "_")

            # joining and storing the data files in full_path with respective names
            sector_path = os.path.join(full_path, file_name)

            time.sleep(2)

            data = yf.download(
                ticker, period=period, interval=interval, auto_adjust=True
            )

            if data is None or data.empty:
                print("Data is not available")
                continue

            # saving the obtained data to csv
            data.to_csv(sector_path, mode="x")
            print(f"Data file named {file_name} has been saved !")
            count += 1

        return count

    except Exception as e:
        print(f"Could not fetch data :  {e}")
        return None


# %%
get_sector_files("5y", "1d")

# %%
# extracting ticker symbols from the nasdaq csv file (this is not historical dataset and only be used for reference and tickers)
ticker_list = []
for sym in nasdaq_df["Symbol"]:
    if isinstance(sym, str) and sym.strip():
        ticker_list.append(sym.strip())

# %%
# extracting ticker symbols from the nasdaq csv file (this is not historical dataset and only be used for reference and tickers)
name_list = []
for sym in nasdaq_df["Name"]:
    name_list.append(sym)


# %%
# below function extracts singular file data via yahoo finance and the data will be saved in raw data subfolder in data.
def get_data_file(
    ticker: str, period: str, interval: str, f_name: str
) -> pd.DataFrame | None:

    full_path = r"C:\Users\Aamir Bin Abbas\Desktop\Research & Thesis\Stock-Price-Predictor-Close--LSTM\data\raw\yahoo_finance"

    try:
        # create a file inside "full_path"
        os.makedirs(full_path, exist_ok=True)

        # naming structure of individual files
        file_name = f"{f_name}_stock_data.csv".replace(" ", "_")

        # csv file to be saved in raw subfolder in data folder
        raw_path = os.path.join(full_path, file_name)

        time.sleep(2)  # precaution to avoid rate limiter by yf.download
        data = yf.download(ticker, period=period, interval=interval, auto_adjust=True)

        if data is None or data.empty:
            print("No data was found in ")
            return None

        data.to_csv(
            raw_path, mode="x"
        )  # the mode can be changed after downloading to x if file already exits

        print(f"Data file named {file_name} has been saved !")

        return data

    except Exception:
        print(f"Error : Either the file exists or Unavailable")


# %%
# run this when file is required to be downloaded : first 20 files shall be downloaded
for i in range(0, 20):
    target_ticker = ticker_list[i]
    target_filename = name_list[i]

    try:
        get_data_file(target_ticker, "5y", "1d", target_filename)
    except Exception as e:
        print(f"File Already Exists : {e}")
