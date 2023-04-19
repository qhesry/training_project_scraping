import nltk
from database_utils.database_utils import create_index
from processing.scrapping import scrap_url
import os

if __name__ == "__main__":
    # Urls to scrap
    urls = ["https://www.trustpilot.com/review/cyberghostvpn.com", "https://www.trustpilot.com/review/nordvpn.com"]

    # Download stopwords and WordNetLemmatizer if not downloaded already
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')

    create_index()
    number_of_reviews_scraped = 0
    # Scraping every Urls
    for url in urls:
        number = scrap_url(url)
        number_of_reviews_scraped += number

    print(f"Scraped : {number_of_reviews_scraped} reviews")