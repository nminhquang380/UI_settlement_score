import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

def preprocess_data(scoring_df):
    # Fill missing values
    scoring_df['Client ID (Clients)'] = scoring_df['Client ID (Clients)'].fillna(method='ffill')
    scoring_df['Session Delivered By (Outcomes)'] = scoring_df['Session Delivered By (Outcomes)'].fillna(method='ffill')
    scoring_df['Session ID (Outcomes)'] = scoring_df['Session ID (Outcomes)'].fillna(method='ffill')
    scoring_df['Session Date (Outcomes)'] = scoring_df['Session Date (Outcomes)'].fillna(method='ffill')
    scoring_df['Question Type (Outcomes)'] = scoring_df['Question Type (Outcomes)'].fillna(method='ffill')
    scoring_df['Question (Outcomes)'] = scoring_df['Question (Outcomes)'].fillna(method='ffill')

    # Drop last column
    last_index = len(scoring_df)-1
    scoring_df.drop(last_index, inplace=True)

    # Handle Datetime values
    scoring_df['Session Date (Outcomes)'] = pd.to_datetime(scoring_df['Session Date (Outcomes)'], format="%d %b. %Y")

    # Transform Numerical values
    scoring_df['Response (Outcomes)'] = pd.to_numeric(scoring_df['Response (Outcomes)'], errors='coerce')

    # Normalise Question texts
    scoring_df['Question (Outcomes)'] = scoring_df['Question (Outcomes)'].apply(lambda x : re.sub(r'\s*-\s*', ' - ', x))

    # Drop unecessary rows
    scoring_df = scoring_df[(scoring_df['Question (Outcomes)'] != '1 - A lot difficulties.  5 - Good at managing this issue') &\
                            (scoring_df['Question (Outcomes)'] != '1 - Strongly Disagree. 5 - Strongly Agree')]
    
    return scoring_df