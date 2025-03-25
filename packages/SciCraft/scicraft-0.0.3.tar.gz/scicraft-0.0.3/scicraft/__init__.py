import pandas as pd

def time_shift(variables, dataframe, id='id', time='time', shift=1):
    """
    Creates lagged or lead variables for the specified variables in the time series data.

    This function generates lagged (_lag, _lag2, etc.) or lead (_lead, _lead2, etc.) variables based on the 
    specified `shift` value. Positive values of `shift` generate lagged variables, while negative values 
    generate lead variables.

    Parameters:
    ----------
    dataframe : pandas.DataFrame, optional, default=df
        The input DataFrame containing time-series data.

    id : str, optional, default='id'
        The unit or company identifier column name in the DataFrame.

    time : str, optional, default='time'
        The time period identifier column name in the DataFrame.

    variables : list of str
        A list of column names for which lagged or lead variables will be created.

    shift : int, optional, default=1
        The number of time periods to shift. A positive integer creates lagged variables, while a negative 
        integer creates lead variables.

    Returns:
    -------
    pandas.DataFrame
        A DataFrame with the original columns plus the new lagged or lead variables.

    Raises:
    ------
    Exception
        If `shift` is not an integer or if `shift` is 0.
    
    Notes:
    -----
    - Lagged variables are created by shifting data backwards (positive `shift`).
    - Lead variables are created by shifting data forwards (negative `shift`).
    """
    
    if not isinstance(shift, int):
        raise Exception ("Shift value needs to be an integer")
    if shift==0:
        raise Exception ("Shift value cannot be equal to 0, as it would not change the data.")
    
    df_lag=dataframe[[time]+[id]+variables].copy()
    df_lag[time]=df_lag[time]+shift

    if shift > 0:  # Lag
        suffix = f'_lag{shift}' if shift > 1 else '_lag'
        df_merged = pd.merge(dataframe, df_lag, how="left", left_on=[id, time], right_on=[id, time], suffixes=['', suffix])
    elif shift < 0:  # Lead
        suffix = f'_lead{abs(shift)}' if shift < -1 else '_lead'
        df_merged = pd.merge(dataframe, df_lag, how="left", left_on=[id, time], right_on=[id, time], suffixes=['', suffix])
    return df_merged

def pipe_list(x):
    return [int(i) for i in x.split("|") if i]