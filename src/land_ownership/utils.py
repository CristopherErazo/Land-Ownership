import pandas as pd
import numpy as np

countries = {
    'names': ['Austria', 'Belgium', 'Bulgaria', 'Czechia', 'Germany','Denmark','Estonia', 'Spain',
              'Finland','France','United Kingdom' ,'Greece','Croatia','Hungary','Ireland','Italy','Lithuania',
              'Luxembourg','Latvia','Netherlands','Poland','Portugal','Romania','Sweden','Slovakia'],

    'abbreviations': ['at', 'be', 'bg', 'cz', 'de', 'dk', 'ee', 'es',
                      'fi', 'fr', 'gb', 'gr', 'hr', 'hu', 'ie', 'it', 'lt',
                      'lu', 'lv', 'nl', 'pl', 'pt', 'ro', 'se','sk']

}

# 'Cyprus', 'Malta'
# 'cy', 'mt'

def clean_dataframe(df: pd.DataFrame, columns_to_keep: list) -> pd.DataFrame:
    """
    Cleans the input dataframe by removing columns with all null values and keeping only the specified columns.
    
    :param df: Raw dataframe to be cleaned
    :param columns_to_keep: Description

    :return df: Cleaned dataframe with only the specified columns and no columns with all null values

    """
    # Eliminate all columns with 0 non-null count
    df = df.dropna(axis=1, how='all')
    
    # Columns to keep
    df = df[columns_to_keep]
    return df

def get_scheme_columns(df: pd.DataFrame) -> list:
    """
    Searches for all columns containing 'scheme' in their name and returns only those without NaN values.
    
    :param df: Dataframe to search for scheme columns
    
    :return valis_scheme_cols: List of scheme column names that have no NaN values
    """
    scheme_cols = [col for col in df.columns if 'scheme' in col.lower()]
    valid_scheme_cols = [col for col in scheme_cols if df[col].notna().any()]

    # Eliminate schemes with 'code' in their name
    valid_scheme_cols = [col for col in valid_scheme_cols if 'code' not in col.lower()]
    return valid_scheme_cols

def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates summary statistics for the given dataframe.
    
    :param df: Dataframe for which to generate summary statistics

    :return summary_df: Dataframe containing summary statistics such as mean, median, and standard deviation for numerical columns

    """
    summary_df = df.describe()
    return summary_df



def fmt_fraction(x, sci_threshold=1e-3):
    if x == 0 or abs(x) >= sci_threshold:
        return f"{x:.3f}"
    return f"{x:.3e}"

def fmt_amount(x):
    if x >= 1e9:
        return f"{x/1e9:.2f}B"
    elif x >= 1e6:
        return f"{x/1e6:.2f}M"
    elif x >= 1e3:
        return f"{x/1e3:.2f}K"
    else:
        return f"{x:.2f}"
