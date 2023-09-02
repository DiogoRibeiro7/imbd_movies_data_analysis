def currency_to_number(currency_str: str) -> int:
    """
    Convert a currency-formatted string to an integer.
    
    Parameters:
        currency_str (str): The currency-formatted string (e.g., "$2,320,250,281").
        
    Returns:
        int: The numerical value of the currency string.
    """
    # Remove the dollar sign and commas
    cleaned_str = currency_str.replace("$", "").replace(",", "")
    
    # Convert to integer
    return int(cleaned_str)

