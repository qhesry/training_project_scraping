from transformers import pipeline
from database_utils.database_utils import get_reviews_not_processed, update_review

sentiment_pipeline = pipeline(model="nlptown/bert-base-multilingual-uncased-sentiment")

def calculate_sentiment(review):
    """
    Calculates the sentiment score and accuracy of a given review.

    Args:
    review (str): The review to be analyzed.

    Returns:
    tuple: A tuple containing the sentiment score and accuracy.
    """
    tronc_review = review[:512]
    result = sentiment_pipeline(tronc_review)
    label = result[0]['label'].split(' ')[0]
    accuracy = result[0]['score']
    return label, accuracy

# Just in case
def process_reviews_not_processed_during_scraping():
    """
    Processes reviews that were not sentiment analyzed during the scraping process.
    Retrieves reviews that do not have a sentiment score, calculates the sentiment score and accuracy,
    and updates the review in the Elasticsearch index.

    Returns:
    None
    """
    company_reviews = get_reviews_not_processed()
    page = 1
    while company_reviews['hits']['hits']:
        print(f"Processing page : {page}")
        for hit in company_reviews['hits']['hits']:
            review = hit['_source']['content']

            sentiment_label, accuracy = calculate_sentiment(review[:512])

            review = {
                "sentiment_score" : sentiment_label.split(' ')[0],
                "accuracy"        : accuracy,
            }

            update_review(review, hit['_id'])

            page += 1
            company_reviews = get_reviews_not_processed()

