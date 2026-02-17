import pandas as pd


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

def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates summary statistics for the given dataframe.
    
    :param df: Dataframe for which to generate summary statistics

    :return summary_df: Dataframe containing summary statistics such as mean, median, and standard deviation for numerical columns

    """
    summary_df = df.describe()
    return summary_df