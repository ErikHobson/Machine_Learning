#### This is a combination of functions that I use for convenience.

import pandas as pd
import numpy as np


def alpha_filter(data, alpha):

    alpha=1-alpha
    """
    Applies an alpha filter to a Pandas DataFrame time series.
    
    Parameters:
        data (DataFrame): The input time series data.
        alpha (float): The alpha value used in the filter.
    
    Returns:
        DataFrame: The filtered time series data.
    """
    # Create an empty DataFrame to hold the filtered data
    filtered_data = pd.DataFrame(columns=data.columns)
    
    # Apply the alpha filter to each column in the data
    for col in data.columns:
        filtered_col = [data[col].iloc[0]]
        for i in range(1, len(data)):
            filtered_val = alpha * data[col].iloc[i] + (1 - alpha) * filtered_col[-1]
            filtered_col.append(filtered_val)
        filtered_data[col] = filtered_col
    
    return filtered_data