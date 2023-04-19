from elasticsearch import Elasticsearch, exceptions
import json
from . import config

es = Elasticsearch(hosts=config["elasticsearch_hosts"], basic_auth=(config["elasticsearch_username"], config["elasticsearch_password"]), ca_certs=config["elasticsearch_ca_certs_path"])

def create_index():
    """
    This function creates Elasticsearch indices for storing company reviews, company information, and the timestamp of the last web scraping.
    The mappings for these indices are loaded from JSON files and passed to the `create` method of the Elasticsearch `indices` object.
    
    Usage: 
    create_index()

    Args: 
    None

    Returns:
    None

    Note:
    - The JSON mapping files should be located in the "./mappings" directory relative to the current working directory.
    - If an index already exists, it will not be created again.
    """
    
    # Load mapping for the "companies_reviews" index
    with open('./mappings/companies_reviews_mapping.json') as f:
        companies_reviews_mapping = json.load(f)

    # Create the "companies_reviews" index if it does not exist
    if not es.indices.exists(index="companies_reviews"):
        es.indices.create(index="companies_reviews", mappings=companies_reviews_mapping)

    # Load mapping for the "companies_infos" index
    with open('./mappings/companies_infos_mapping.json') as f:
        companies_infos_mapping = json.load(f)

    # Create the "companies_infos" index if it does not exist
    if not es.indices.exists(index="companies_infos"):
        es.indices.create(index="companies_infos", mappings=companies_infos_mapping)

    # Load mapping for the "last_scraping" index
    with open('./mappings/last_scraping_mapping.json') as f:
        last_scraped_at_mapping = json.load(f)

    # Create the "last_scraping" index if it does not exist
    if not es.indices.exists(index="last_scraping"):
        es.indices.create(index="last_scraping", mappings=last_scraped_at_mapping)

def insert_review(reviews):
    """
    This function inserts review documents into the "companies_reviews" index in Elasticsearch.
    
    Usage: 
    insert_review(reviews)

    Args: 
    - reviews (list of dict): A list of review documents to be inserted.

    Returns:
    None

    Note:
    - The review documents should have a unique identifier stored under the "unique_hash" key.
    - The Elasticsearch index should already exist before inserting documents into it.
    - If a document with the same unique identifier already exists in the index, it will be updated instead of inserted.
    """
    for review in reviews:
        
        # Extract the unique identifier and remove it from the document
        unique_hash = review['unique_hash']
        del review['unique_hash']

        # Insert or update the document in the "companies_reviews" index using the unique identifier as the document ID
        es.index(id=unique_hash, index="companies_reviews", document=review)


def insert_company_infos(company):
    """
    This function inserts a company information document into the "companies_infos" index in Elasticsearch.
    
    Usage: 
    insert_company_infos(company)

    Args: 
    - company (dict): A company information document to be inserted.

    Returns:
    None

    Note:
    - The company information document should have a unique identifier stored under the "unique_hash" key.
    - The Elasticsearch index should already exist before inserting documents into it.
    - If a document with the same unique identifier already exists in the index, it will be updated instead of inserted.
    """
    # Extract the unique identifier and remove it from the document
    unique_hash = company['unique_hash']
    del company['unique_hash']

    # Insert or update the document in the "companies_infos" index using the unique identifier as the document ID
    es.index(id=unique_hash, index="companies_infos", document=company)


def get_last_scraping_time(company_name):
    """
    This function retrieves the last scraping time for a company from the "last_scraping" index in Elasticsearch.
    
    Usage: 
    last_scraped_at = get_last_scraping_time(company_name)

    Args: 
    - company_name (str): The name of the company to retrieve the last scraping time for.

    Returns:
    - date_last_scrap (str or None): The timestamp of the last web scraping for the specified company, or None if the company is not found.

    Note:
    - This function requires the Elasticsearch library to be imported.
    - The Elasticsearch index should already exist and contain documents with IDs corresponding to the company names.
    """
    try:
        # Get the last time scraped document for the specified company
        last_time_scraped = es.get(index="last_scraping", id=company_name)
        date_last_scrap = last_time_scraped['_source']['last_scraped_at']
    except exceptions.NotFoundError:
        # If the company is not found in the "last_scraping" index, return None
        date_last_scrap = None

    return date_last_scrap


def set_last_scraped_at(company_name, time):
    """
    This function updates the last scraping time for a company in the "last_scraping" index in Elasticsearch.
    
    Usage: 
    set_last_scraped_at(company_name, time)

    Args: 
    - company_name (str): The name of the company to update the last scraping time for.
    - time (str): The timestamp of the last web scraping.

    Returns:
    None

    Note:
    - This function requires the Elasticsearch library to be imported.
    - The Elasticsearch index should already exist and contain documents with IDs corresponding to the company names.
    """
    es.index(id=company_name, index="last_scraping", document={"last_scraped_at": time})


def get_reviews_not_processed(page_size=100):
    """
    This function retrieves reviews that have not been processed for sentiment analysis from the "companies_reviews" index in Elasticsearch.
    
    Usage: 
    result = get_reviews_not_processed(page_size)

    Args: 
    - page_size (int): The number of reviews to retrieve in one request. Default is 100.

    Returns:
    - result (dict): A dictionary containing the search results.

    Note:
    - This function requires the Elasticsearch library to be imported.
    - The "companies_reviews" index should already exist and contain documents with a "sentiment_score" field.
    """
    query = {
        "query": {
            "bool": {
                "must_not": {
                    "exists": {"field": "sentiment_score"}
                }
            }
        },
        "size": page_size
    }
    result = es.search(index="companies_reviews", body=query)
    return result


def update_review(review, hit):
    """
    This function updates a review document in the "companies_reviews" index in Elasticsearch.
    
    Usage: 
    update_review(review, hit)

    Args: 
    - review (dict): The updated review document.
    - hit (str): The ID of the review document to update.

    Returns:
    None

    Note:
    - This function requires the Elasticsearch library to be imported.
    - The Elasticsearch index should already exist and contain documents with unique IDs.
    """
    es.update(index="companies_reviews", id=hit, body={"doc": review})
