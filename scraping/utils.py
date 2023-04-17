from datetime import datetime
import hashlib

def convert_date(date_str):
    """
    Convert a date string to Elasticsearch's date format.

    This function tries to detect the input date format automatically and convert it to
    Elasticsearch's format ("%Y-%m-%dT%H:%M:%S.%fZ"). If the input format is not one of
    the supported formats, a ValueError is raised.

    Args:
        date_str (str): The date string to convert.

    Returns:
        str: The converted date string in Elasticsearch's format.

    Raises:
        ValueError: If the input date format is not supported.

    Examples:
        >>> convert_date("April 13, 2023")
        '2023-04-13T00:00:00.000Z'

        >>> convert_date("2023-04-13T16:55:12.000Z")
        '2023-04-13T16:55:12.000Z'
    """
    if not date_str:
        return None
    
    # Try to parse the date string to a datetime object using each supported format
    supported_formats = ['%B %d, %Y', '%Y-%m-%dT%H:%M:%S.%fZ']
    for format_str in supported_formats:
        try:
            date_obj = datetime.strptime(date_str, format_str)
            break
        except ValueError:
            pass
    else:
        # If none of the formats worked, raise an error
        raise ValueError('Unsupported date format')

    # Convert the datetime object to Elasticsearch's date format
    es_date_str = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    return es_date_str

def create_unique_id(review):
    """
    Generate a unique ID for the review.
    
    Args:
    - review_data (dict): A dictionary containing the review data.

    Returns:
    - unique_id (str): A unique hexadecimal string generated from the review data using the SHA-256 algorithm.

    Note:
    - The uniqueness of the generated ID depends on the uniqueness of the input data. If two different sets of review data result in the same hash value, the generated IDs will not be unique.
    """
    # Convert the dictionary to a string
    review_string = str(review)

    # Create a hash object using the SHA-256 algorithm
    hash_object = hashlib.sha256()

    # Encode the review string as bytes and update the hash object
    hash_object.update(review_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    unique_id = hash_object.hexdigest()

    return unique_id