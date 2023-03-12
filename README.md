<h1>Machine Learning Stock Trading Model</h1>

This repository is to explore Machine Learning Models to create a trading algorithm based on Technical Indicators like SMA, EMA, RSI, etc.
The stocks looked at are stocks that belong to the SP500, and the data for this was retireved from Kaggle/Yahoo Finance.

Steps to reproduce:
1) conda env create -f environment.yaml
2) python load_data.py
    This data is loaded into a sqlite DB on my local machine so the data does not have to be ingested from CSV files everytime. The data is excluded from this repo due to size
3) python feature_engineering.py