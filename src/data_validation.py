# %%
import pandas as pd
from pandas.errors import EmptyDataError
import logging
import glob
import os

# %%
YFINANCE_PATH = r"C:\Users\Aamir Bin Abbas\Desktop\Research & Thesis\Stock-Price-Predictor-Close--LSTM\data\raw\yahoo_finance"  # top 20 csv files downloaded from nasdaq ticker
SECTOR_WISE_PATH = r"C:\Users\Aamir Bin Abbas\Desktop\Research & Thesis\Stock-Price-Predictor-Close--LSTM\data\raw\yahoo_finance\sector_wise_csv"  # 12 unique sector wise csv files
PROCESSED_PATH = r"C:\Users\Aamir Bin Abbas\Desktop\Research & Thesis\Stock-Price-Predictor-Close--LSTM\data\processed"  # process folder path

# %%
def path_profile(directory_path: str) -> dict | None:
    """A miscellaneous function to check the availability of csv files and their full directory

    Args:
        directory_path (str): path of the folder to inspect

    Returns:
        dict|None: returns a dictionary if all the directory or desired to be viewed else None
    """
    try:
        folder_metadata = {}

        search_pattern = os.path.join(directory_path, "*.csv")

        csv_file_paths = glob.glob(search_pattern)

        folder_metadata = {
            "path_provided": directory_path,
            "csv_exists": bool(csv_file_paths),
            "number_of_files": len(csv_file_paths),
        }

        show_paths_input = (
            str(input("Provide Yes/No for file paths : ")).strip().lower()
        )

        match show_paths_input:
            case "yes":
                print(csv_file_paths)
            case "no":
                print("Operation Completed")
            case _:
                print("Operation Completed")

        return folder_metadata

    except Exception as e:
        print(f"Unexpected Error Occurred : {e}")

        return None

# %%
"""# to inspect dataframe quickly and validate the expected structure of stock data

def get_df_profile(dataset:pd.DataFrame) -> dict|None:
    try:
        data_profile = {}

        data_profile['shape'] = dataset.shape

        data_profile['size'] = dataset.size

        data_profile['column_names'] = list(dataset.columns)

        data_profile['duplicates_rows'] = dataset.duplicated().sum() # duplicate rows across whole dataset

        data_profile['duplicate_columns'] = dataset.T.duplicated().sum()

        data_profile['missing_values_whole'] = dataset.isna().sum().sum() # this is across whole dataset and return sum

        data_profile['missing_values_pct'] = (dataset.isna().sum().sum() / (dataset.shape[0]*dataset.shape[1])) * 100 # this is across whole dataset and return percentage

        for col in dataset.columns:
            data_profile[col] = dataset[col].max() # returns max value from each columns
            data_profile[col] = dataset[col].min() # returns max value from each columns
            data_profile[col] = dataset[col].dtype # data type of each column

        #data_profile['start_data'] = dataset['Date'].min()
        #data_profile['end_data'] = dataset['Date'].max()

        return data_profile

    except (ZeroDivisionError,IndexError,ValueError,TypeError) as e:
        print(f' Unexpected Error occurred : {e}')

        return None

# all datasets downloaded from yfinance has their 'Date' in row"""

# %%
def validate_dataframe(dataset: pd.DataFrame) -> None:
    """Validate dataset in a function

    Args:
        dataset (pd.DataFrame): A pandas dataframe

    Raises:
        TypeError: raised if not a pandas dataframe
        EmptyDataError: raised if dataset is empty
    """
    
    if not isinstance(dataset, pd.DataFrame):
        raise TypeError(f"The arg {dataset} provided is not a pandas dataframe, got {type(dataset).__name__}")

    if dataset.empty:
        raise EmptyDataError("The provided dataset is empty")
    

# %%
# 1.0 : clearer code than before and in more detail inspection can be made
def df_profile(dataset: pd.DataFrame) -> dict | None:
    """
    Generate a structural profile of a DataFrame.

    Args:
        dataset (pd.DataFrame): DataFrame containing stock market data.

    Raises:
        ValueError: If the provided DataFrame is empty.

    Returns:
        dict: A dictionary containing:
            - dataset_info: General DataFrame metadata.
            - column_profile: Metadata for individual columns.
            - index_info: Metadata about the DataFrame index.
    """
    validate_dataframe(dataset)

    try:
        data_profile = {"dataset_info": {}, "column_profile": {}, "index_info": {}}

        data_profile["dataset_info"] = {
            "shape": dataset.shape,
            "size": dataset.size,
            "column_names": dataset.columns.to_list(),
            "duplicate_columns": dataset.T.duplicated().sum(),
            "duplicate_rows": dataset.duplicated().sum(),
            "memory_usage_bytes": dataset.memory_usage(deep=True).sum(),
            "missing_values": dataset.isna().sum().sum(),
            "missing_values_pct": (
                dataset.isna().sum().sum() / dataset.size * 100
                if dataset.size > 0
                else 0
            ),
        }

        for col in dataset.columns:
            data_profile["column_profile"][col] = {
                "dtype": dataset[col].dtype,
                "max": dataset[col].max(),
                "min": dataset[col].min(),
                "num_of_unique": dataset[col].nunique(),
                "missing_values": dataset[col].isna().sum(),
                "missing_values_pct": dataset[col].isna().mean() * 100,
            }

        data_profile["index_info"] = {
            "index_name": dataset.index.name,
            "index_type": type(dataset.index).__name__,
            "index_dtype": dataset.index.dtype,
            "index_unique": dataset.index.is_unique,
            "index_min": dataset.index.min() if len(dataset) > 0 else None,
            "index_max": dataset.index.max() if len(dataset) > 0 else None,
        }

        return data_profile

    except (ZeroDivisionError, IndexError, ValueError, TypeError, KeyError) as e:
        print(f"Unexpected Error occurred : {e}")

        return None

# %%
def standardize_data(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Standardizes the datasets for analysis.

    Args:
        dataset (pd.DataFrame): DataFrame containing stock market data.

    Raises:
        TypeError: If the provided DataFrame is empty.
        EmptyDataError: If the provided dataset is empty

    Returns:
        pd.DataFrame : a organized dataframe for stock analysis and None upon failure
    """

    validate_dataframe(dataset)

    try:
        dataset["Ticker"] = dataset.iloc[0, 1]  # contains the ticker in row

        dataset["Date"] = dataset["Price"]  # making new columns named 'Date'

        dataset = dataset.drop(dataset.iloc[[0, 1]].index)  # dropping the top 2 rows

        dataset["Date"] = pd.to_datetime(dataset["Date"])  # converting to Datetime

        dataset = dataset.drop(columns="Price")  # price contains ticker and date

        dataset = dataset.reset_index(
            drop=True
        )  # resetting index of the dataset after dropping of the top 2 rows

        numerical_cols = dataset.columns.drop(
            ["Date", "Ticker"]
        )  # selecting columns excluding date and ticker which are stored as str

        for col in numerical_cols:
            dataset[col] = pd.to_numeric(
                dataset[col], errors="coerce"
            )  # converting columns to numeric from string

        return dataset

    except (ValueError, IndexError, TypeError) as e:
        print(f"Unexpected Error Occurred : {e}")
        raise

# %%
# takes in dataframe column to give max,min ,mean,mode of a column series
def column_profile(dataset: pd.DataFrame, columns_name: str) -> dict | None:
    """
    Generates a dictionary containing metadata of the whole dataframe

    Args:
        dataset (pd.DataFrame): A pandas dataframe.
        columns_name (str): specific column for inspection

    Raises:
        EmptyDataError: If the provided dataset is empty
        TypeError : if the dataset is not dataframe

    Returns:
        dict: a dictionary containing metadata.

    """

    validate_dataframe(dataset)

    # check if the column exists
    if columns_name not in dataset.columns:
        print(f'No such column was found "{columns_name}"')
        return None

    try:
        column_summary = {}

        # condition to make the function data type aware and perform specific calculations
        if pd.api.types.is_numeric_dtype(
            dataset[columns_name]
        ):  # numerical calculation on numeric dtype condition
            column_summary = {
                "Company Ticker": dataset["Ticker"].iat[
                    0
                ],  # for understanding which company dataset is being analyzed
                "Name of column": dataset[columns_name].name,
                "Size of column": dataset[
                    columns_name
                ].size,  # including missing values
                "Data Type of column": dataset[
                    columns_name
                ].dtypes,  # returns data type of the column
                "Missing values": dataset[columns_name]
                .isna()
                .sum(),  # returns missing values count
                "Max value in column": dataset[columns_name].max(),  # returns max value
                "Min value in the column": dataset[
                    columns_name
                ].min(),  # return minimum value
                "Average": dataset[columns_name].mean(),  # return average value
                "Mode of the column": dataset[columns_name]
                .mode()
                .iloc[
                    0
                ],  # kept the first mode (frequent) value , remove iloc to change to series ,
                "Standard Deviation": dataset[columns_name].std(),
                "Number of Unique Values": dataset[
                    columns_name
                ].nunique(),  # return number of unique values
                "Total duplicates": dataset[columns_name]
                .duplicated()
                .sum(),  # total duplicate values
            }

        elif pd.api.types.is_datetime64_any_dtype(
            dataset[columns_name]
        ):  # datetime calculation on date data type
            column_summary = {
                #'Company Ticker' : dataset['Ticker'].iat[0] , # for understanding which company dataset is being analyzed
                "Name of column": dataset[columns_name].name,
                "Size of column": dataset[
                    columns_name
                ].size,  # including missing values
                "Data Type of column": dataset[
                    columns_name
                ].dtypes,  # returns data type of the column
                "Missing values": dataset[columns_name]
                .isna()
                .sum(),  # returns missing values count
                "Start date in the column": dataset[
                    columns_name
                ].min(),  # returns the start date
                "End date in column": dataset[
                    columns_name
                ].max(),  # returns the end date
                "Number of Unique dates": dataset[
                    columns_name
                ].nunique(),  # unique dates
                "duplicate dates": dataset[columns_name]
                .duplicated()
                .sum(),  # total duplicate dates
            }

            # checking the number of weekdays and weekends in the date column 0-6 (where 5 and 6 are Saturday and Sunday)
            weekend = dataset[columns_name].dt.day_of_week >= 5
            column_summary["Weekends"] = weekend.sum()
            column_summary["Weekdays"] = (~weekend).sum()

        else:
            column_summary = {
                "Company Ticker": dataset["Ticker"].iat[
                    0
                ],  # for understanding which company dataset is being analyzed
                "Name of column": dataset[columns_name].name,
                "Size of column": dataset[
                    columns_name
                ].size,  # including missing values
                "Data Type of column": dataset[
                    columns_name
                ].dtypes,  # returns data type of the column
                "Missing values": dataset[columns_name]
                .isna()
                .sum(),  # returns missing values count
                "Total duplicate dates": dataset[columns_name]
                .duplicated()
                .sum(),  # total duplicate dates
            }

        return column_summary

    except (TypeError, ValueError, IndexError, KeyError) as e:
        print(f"Unexpected Error Occurred : {e}")

        return None

# %%
def get_missing_values(
    dataset: pd.DataFrame, converted_dataset: pd.DataFrame
) -> pd.DataFrame | None:
    """
    Generates a dataframe to verify if creation of missing value due to standardization(if any).

    Args:
            dataset (pd.DataFrame): A pandas dataframe .
            converted_dataset (pd.DataFrame): A pandas dataframe post-standardization.

    Raises:
            EmptyDataError: If the provided dataset is empty
            TypeError : If any of the args is not pandas dataframe
            ValueError : If duplicate columns are found in any dataset or either dataset is empty.Also raises error if any dataframe has unique columns

    Returns:
            pd.DataFrame: a dataframe showing the difference of missing values before and after

    """
    
    validate_dataframe(dataset)
    validate_dataframe(converted_dataset)
    
    # checking if both have valid columns structure
    if not dataset.columns.is_unique or not converted_dataset.columns.is_unique:
        raise ValueError("Duplicate columns were detected")

    # checking if columns in dataframes are different than expected
    if set(dataset.columns) != set(converted_dataset.columns):
        raise ValueError("Both dataframes must have same columns")

    combined_dataset = None

    try:
        initial_missing = pd.Series(
            dataset.isna().sum()
        )  # series which returns missing values before conversion

        final_missing = pd.Series(
            converted_dataset.isna().sum()
        )  # series which returns missing values before conversion

        combined_dataset = pd.concat([initial_missing, final_missing], axis=1)

        combined_dataset.columns = [
            "Before_Conversion",
            "After_Conversion",
        ]  # naming columns accordingly

        combined_dataset["Difference"] = (
            combined_dataset["After_Conversion"] - combined_dataset["Before_Conversion"]
        )  # calculating missing difference

    except Exception as e:
        print(f"Unexpected Error Occurred : {e}")
        return None
    return combined_dataset

# %%
def structure_validation(dataset: pd.DataFrame) -> bool:
    """
    Validates a dataset after standardization.

    Args:
            dataset (pd.DataFrame): A pandas dataframe .

    Raises:
            EmptyDataError: If the provided dataset is empty
            TypeError : If any of the args is not pandas dataframe
    Returns:
            bool: True if the dataset has required/expected attributes,columns and datatype else False

    """
    validate_dataframe(dataset)

    # the below variables are the required validation test a dataset must pass
    # req_cols = ['Close', 'High', 'Low', 'Open', 'Volume', 'Ticker', 'Date'] # these are required in this stock analysis in any order

    # if set(req_cols).issubset(dataset.columns):
    #    print('The required columns are available in the dataset')
    # else:
    #    print('Required Columns are missing')

    req_cols = {"Close", "High", "Low", "Open", "Volume", "Ticker", "Date"}
    missing_cols = req_cols - set(dataset.columns)

    if missing_cols:
        print(f"Validation failed ! missing column : {missing_cols}")
        return False
    print("All columns are available")

    try:
        if not pd.api.types.is_datetime64_any_dtype(dataset["Date"]):
            print(f"The Date Column has failed")
            return False
        print("The Date column has passed")

        # Price validation (Allows both float and int types)
        price_cols = ["Close", "High", "Low", "Open", "Volume"]

        if not all(
            pd.api.types.is_float_dtype(dataset[col])
            or pd.api.types.is_numeric_dtype(dataset[col])
            for col in price_cols
        ):
            print(f"The Price Columns has passed")
            return False
        print("Price Columns has passed! ")

        # ticker(string) validation
        if not pd.api.types.is_string_dtype(dataset["Ticker"]):
            print("ticker has failed validation")
            return False
        print(f"The Ticker Column has passed")

        print("The Dataset has passed the validation")
        return True

    except Exception as e:
        print(f"Unexpected Error : {e}")
        raise

# %%
def validate_dates(dataset: pd.DataFrame) -> dict:
    """
    Generates a dictionary on validation of dates column.

    Args:
            dataset (pd.DataFrame): A pandas dataframe .

    Raises:
            EmptyDataError: If the provided dataset is empty
            TypeError : If any of the args is not pandas dataframe
    Returns:
            dict: A dictionary containing metadata of the 'Dates' column

    """
    validate_dataframe(dataset)

    valid_summary = {}

    for col in dataset.columns:
        if pd.api.types.is_datetime64_any_dtype(dataset[col]):
            valid_summary[col] = {
                "missing_date": dataset[col].isna().sum(),
                # checking whether your dates are arranged from oldest to newest.
                "is_in_ascending": dataset[
                    col
                ].is_monotonic_increasing,  # arranged in oldest to newest
                "is_in_descending": dataset[
                    col
                ].is_monotonic_decreasing,  # arranged in oldest to newest
                "start_date": dataset[col].min(),
                "end_date": dataset[col].max(),
                "minimum_days_gap": dataset[col].sort_values().diff().min(),
                "max_days_gap": dataset[col].sort_values().diff().max(),
                "contains_future": (
                    dataset[col] > pd.Timestamp.today()
                ).sum(),  # returns number of future dates
                "unique_dates": dataset[col].nunique(),
                "duplicate_date": dataset[col].duplicated().sum(),
            }

    return valid_summary

# %%
# saves file in the processed folder after validating the dataset
def save_processed(dataset: pd.DataFrame) -> bool:
    """
    Saves the given dataset in the 'processed' folder.

    Args:
            dataset (pd.DataFrame): A pandas dataframe .

    Raises:
            EmptyDataError: If the provided dataset is empty
            TypeError : If any of the args is not pandas dataframe
    Returns:
            dict: A dictionary containing metadata of the 'Dates' column

    """
    validate_dataframe(dataset)

    try:
        # folder path
        folder_path = f"{PROCESSED_PATH}/yahoo_finance"

        # creating directory
        os.makedirs(folder_path, exist_ok=True)

        # obtain the ticker name from dataset
        ticker = dataset["Ticker"].iloc[0]

        # name the file with with ticker in prefix
        filename = f"{ticker}.csv"

        # join the path
        save_file = os.path.join(folder_path, filename)

        dataset.to_csv(save_file, mode="x", index=False)

        print(f"The file {filename} has been saved!")

        return True

    except Exception as e:
        print(f"Unexpected Error Occurred : {e}")

        return False

# %%
def pipeline() -> str:
    """
    A pipeline that saves the dataset upon success

    Returns:
        str: details on how many files were saved
    """

    logging.info("Starting Pipeline")

    access_list = [
        file
        for file in glob.glob(
            f"{SECTOR_WISE_PATH}/*.csv",
        )
    ]  # change the path

    saved_file_count = 0

    if not access_list:
        logging.error("The folder contains no csv files")

    logging.info("Accessing each dataset in the folder named 'yahoo_finance'")

    for i in range(len(access_list)):
        try:
            df = pd.read_csv(access_list[i])

        except Exception as e:
            logging.error(f"Unable to access dataset: {e}")

        else:
            logging.info("Standardizing dataset and assigning a new variable")
            df_stand = standardize_data(df)

            if df_stand is None:
                logging.warning("Failed to standardized the dataset")

            if df_stand is not None:
                logging.info("Validating Structure")

                temp = structure_validation(df_stand)

                if temp:
                    logging.info("Saving dataset!")
                    save_processed(df_stand)
                    saved_file_count += 1

                else:
                    logging.error("Structure Validation has failed")

    return f"Saved {saved_file_count} in the processed folder out of {len(access_list)}"

# %%
# pipeline()

# %%
access_list = [
    file
    for file in glob.glob(
        f"{SECTOR_WISE_PATH}/*.csv",
    )
]

df = pd.read_csv(access_list[1])

# %%


# %%



