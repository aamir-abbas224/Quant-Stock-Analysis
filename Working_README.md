
- [Important notes and points for professional read me](#important-notes-and-points-for-professional-read-me)
  - [What each folder is responsible for: initial structure which shall be modified as needed](#what-each-folder-is-responsible-for-initial-structure-which-shall-be-modified-as-needed)
  - [created venv (virtual environment) inside the project folder and downloaded simple libraries which shall be used to download analyze data](#created-venv-virtual-environment-inside-the-project-folder-and-downloaded-simple-libraries-which-shall-be-used-to-download-analyze-data)
  - [yfinance shall be used to extract stock data](#yfinance-shall-be-used-to-extract-stock-data)
  - [goal (initial) :](#goal-initial-)
- [Meaning of Stock data](#meaning-of-stock-data)
- [A critical ML concept: data leakage](#a-critical-ml-concept-data-leakage)
- [Source](#source)
- [yf.download rate limiter](#yfdownload-rate-limiter)
- [File size and slowness](#file-size-and-slowness)
- [change plan : individual files rather than whole data together](#change-plan--individual-files-rather-than-whole-data-together)
- [change plan : limited single files to be downloaded since 6998 files of single download and analysis cannot be done](#change-plan--limited-single-files-to-be-downloaded-since-6998-files-of-single-download-and-analysis-cannot-be-done)
- [data validation](#data-validation)
  - [formatting](#formatting)
- [EDA findings and stuff](#eda-findings-and-stuff)

# Important notes and points for professional read me

## What each folder is responsible for: initial structure which shall be modified as needed

*Folder*		    *Responsibility*

data/raw	        Original data downloaded from Yahoo Finance
data/processed	    Cleaned and transformed datasets
notebooks	        Data understanding, EDA and experiments
src		            Reusable Python modules
app		            Streamlit application
exports		        Generated CSV, Excel and PDF reports
tests		        Tests for our Python modules

## created venv (virtual environment) inside the project folder and downloaded simple libraries which shall be used to download analyze data

## yfinance shall be used to extract stock data

## goal (initial) :

1. examine the data and do professional EDA on data sets.
2. generate meaningful analysis on the data and demonstrate via graphs for visual understanding.
3. apply ML techniques and deploy via streamlit.
4. the initial decided goal is to **Predict the next trading session's closing price using historical stock market data.** .
5. markets/companies can be choice of the user based on appropriate ticker provided
6. compare multiple forecasting report on multiple different algorithms and show metric generated via the applied algorithms.
7. top 5 or 3 shall be shown and the trained model can be saved via user!
8. trained , untrained , extracted raw csv , processed csv's  and appropriate graphs can be saved via user (the file extension can be of choice of the user).
9. File choices for data to user : csv , pdf and xlsx

# Meaning of Stock data

Our dataset will contain historical market information:

*Feature	*                 *Meaning*
Open	        Price when the trading session opened
High	        Highest price during the session
Low	Lowest      price during the session
Close	        Closing price 
Volume	        Number of shares traded

**note: The close price was used as the primary target for analysis, prediction and forecasting.**

# A critical ML concept: data leakage

Suppose we're predicting Tuesday's close.

We cannot use Tuesday's actual:

- High
- Low
- Open
- Volume

Because those values aren't fully known when we're making the prediction.

Using them would give our model information from the future. That's called data leakage. This is one of the biggest mistakes in time-series ML projects.

# Source

 Ticker Data will be downloaded from using yfinance

1. Ticker (US Companies) : ['https://www.nasdaq.com/market-activity/stocks/screener'] (this is not historical dataset and only be used for reference and tickers)

# yf.download rate limiter

Hourly IP Caps: Yahoo's underlying global rate limit sits at roughly 2,000 requests per hour per IP address. If yf.download() is run with threads=True (which is the default), it sends concurrent requests for each ticker under the hood. A single pass of 2,000 tickers can immediately burn through your entire hourly allowance and flag your IP.

# File size and slowness

The tickers were of total 6997 and 1987 could be downloaded of 5 years data with consecutive day. Only 1987 tickers data history was downloaded due to rate limiter by yf.download() limit of approx 2000. the file after downloading contained 39997 columns with

# change plan : individual files rather than whole data together

this plan avoids delays during loading of data set and provides comfort in analyzing due to size constraint

# change plan : limited single files to be downloaded since 6998 files of single download and analysis cannot be done

to be selected across different sector companies such as health , tech , energy , finance , large companies ,Stocks with different trading histories and volatility etc

also to exclude stocks with missing historical data or unreliable price histories

---

---

**path_profile**: to check and access different types of file availability and get metadata of files available inside the directory

**Standardized data** : it transform the given dataset in regard of a  pattern which was recognized during visual inspection of of the dataset downloaded via yfinance

# data validation

1. *get_df_profile* func : created to have a quick look on the column names , size , memory usage , missing values in the whole data set and percentage of missing, min and max value in each dataset and also the range of data(initially , error was observed in date so commented it and observed the date column is not in header and rather in row 0).Later created dictionary with 3 keys 1st describes dataset information, 2nd describes columns info and third gives index information.
2. *column profile func* : takes two arguments := the dataset and a column name(as string) to be inspected. it only runs successfully when the dataset has been standardized. it returns a dictionary containing profile of the whole column such as missing values , min , max , name of column etc.
3. *get_missing_values func*: takes in two datasets 1 which is pre-standardization and another is post-standardization. it returns a data frame with the difference of missing values before and after.
4. *structure validation*: it takes in single argument of data frame. it checks and validates such as column names match and their availability , data types off all types columns. ideally run it post-standardization.
5. *validate dates func*: it takes in single argument of data frame. it returns a dictionary containing details and summary of the dates arrangement , duplication, missing , start and end date etc.

**save_processed **: it takes in single argument of dataset and returns a bool. it saves the file in processed directory and names the file in respect of its ticker name.

-  manually created two files in the processed folder to store datasets in a organized way.
-  1. yahoo finance folder contains two folder named `first_20_companies` & `sector_wise_datasets`
-  2. first_20_companies contains ticker datasets of initial company datasets appeared in the nasdaq tickers 
-  3. sector_wise_datasets contains datasets of unique sectors available in in the nasdaq dataset (total is 12)


## formatting
used ruff , black for formatting code files


# EDA findings and stuff

Please refer `stock_market-eda-business-questions.md` for the questions that were answered in the eda section


df2['Open'].corr(df2['Close']) has correlation of 0.989762511379519 # pic Linear_relation(Open_vs_Close).png

`How are daily stock returns distributed, and how frequently does the stock experience unusually large gains or losses?`



variables :
`return_df `: returns dataset with ((close-open) /open) data frame 
