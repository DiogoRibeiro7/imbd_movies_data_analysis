from typing import Union
import pandas as pd


def currency_to_number(currency_str: str) -> int:
    """
    Convert a currency-formatted string to an integer.

    Parameters:
        currency_str (str): The currency-formatted string (e.g., "$2,320,250,281").

    Returns:
        int: The numerical value of the currency string.
    """
    if isinstance(currency_str, int):
        return currency_str
    # Remove the dollar sign and commas
    cleaned_str = currency_str.replace("$", "").replace(",", "")

    # Convert to integer
    return int(cleaned_str)


def replace_hyphen_in_columns(data_frame: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Replace hyphens '-' in specific columns of a Pandas DataFrame with "$,0".

    Parameters:
    df (pd.DataFrame): The input DataFrame with hyphens.
    columns (list): List of column names where hyphens should be replaced.

    Returns:
    pd.DataFrame: The DataFrame with hyphens replaced in specified columns.
    """
    for col in columns:
        data_frame[col] = data_frame[col].apply(
            lambda x: "$,0" if x == "-" else x)
    return data_frame


def extract_minutes(time_str: str) -> int:
    """
    Extract the integer value representing minutes from a string like "176 min".

    Parameters:
    time_str (str): The time string, e.g., "176 min".

    Returns:
    int: The integer value of the minutes, e.g., 176.
    """
    if isinstance(time_str, float):
        return int(time_str)
    if isinstance(time_str, int):
        return int(time_str)
    # Split the string by space and take the first part
    minutes_str = time_str.split(" ")[0]

    # Convert the string to an integer
    minutes_int = int(minutes_str)

    return minutes_int


def extract_first_category(category_str: str) -> str:
    """
    Extract the first category from a comma-separated string.

    Parameters:
    category_str (str): The comma-separated string, e.g., "Action, Crime, Drama".

    Returns:
    str: The first category, e.g., "Action".
    """
    # Split the string by comma and take the first part
    first_category = category_str.split(",")[0].strip()

    return first_category



from typing import Union

def convert_gross_to_numeric(gross: str) -> Union[int, float]:
    """
    Convert a string containing a gross amount to its numerical equivalent in dollars.

    Parameters:
    - gross (str): The string to convert, e.g., '$16.46M', '$0.01M', '5,581', '13', '32,131,830'.

    Returns:
    - Union[int, float]: The numerical equivalent of the gross amount in dollars.

    Example:
    >>> convert_gross_to_numeric('$16.46M')
    16460000
    >>> convert_gross_to_numeric('$0.01M')
    10000
    >>> convert_gross_to_numeric('5,581')
    5581
    >>> convert_gross_to_numeric('13')
    13
    >>> convert_gross_to_numeric('32,131,830')
    32131830
    """
    if isinstance(gross, float) or isinstance(gross, int):
        return gross
    # Remove the dollar sign and commas
    gross = gross.replace('$', '').replace(',', '')
    
    if gross[-1] == 'M':
        return int(float(gross[:-1]) * 1e6)
    else:
        try:
            return int(gross)
        except ValueError:
            try:
                return float(gross)
            except ValueError:
                return 0  # or None, depending on how you want to handle invalid cases

# Test cases
test_results = {
    '$16.46M': convert_gross_to_numeric('$16.46M'),  # Should return 16460000
    '5,581': convert_gross_to_numeric('5,581'),    # Should return 5581
    '13': convert_gross_to_numeric('13'),       # Should return 13
    '32,131,830': convert_gross_to_numeric('32,131,830')  # Should return 32131830
}

test_results







