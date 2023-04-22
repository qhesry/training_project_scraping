from bs4 import BeautifulSoup
from datetime import datetime

import time
import requests

from utils.utils import convert_date, create_unique_id
from database_utils.database_utils import insert_review, insert_company_infos, get_last_scraping_time, set_last_scraped_at
from processing.preprocessing import preprocessing_review
from processing.sentiment_analysis import calculate_sentiment

def get_html(url):
    """
    This function retrieves the HTML content of a web page from a specified URL.
    
    Usage: 
    html_content = get_html(url)

    Args: 
    - url (str): The URL of the web page to retrieve.

    Returns:
    - html_content (str): The HTML content of the web page.

    Raises:
    - ConnectionError: If a connection to the specified URL cannot be established.
    - HTTPError: If an HTTP error occurs while retrieving the HTML content.

    Note:
    - This function requires the requests library to be imported.
    """

    try:
        # Send a GET request to the specified URL and retrieve the HTML content
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.ConnectionError:
        # Raise a ConnectionError if a connection to the specified URL cannot be established
        raise ConnectionError(f"Could not connect to {url}")
    except requests.exceptions.HTTPError as e:
        # Raise an HTTPError if an HTTP error occurs while retrieving the HTML content
        raise requests.exceptions.HTTPError(f"Error retrieving HTML content: {e}")


def get_reviews(company_name, last_time_scraped, soup):
    """
    This function extracts and returns review information from a parsed HTML page.

    Usage:
    stop_fetching, companies_reviews = get_reviews(company_name, last_time_scraped, soup)

    Args:
    - company_name (str): The name of the company being scraped.
    - last_time_scraped (str or None): The timestamp of the last web scraping for the company.
    - soup (bs4.BeautifulSoup): A BeautifulSoup object representing the parsed HTML page.

    Returns:
    - stop_fetching (bool): A boolean value indicating whether the function should stop fetching more reviews.
    - companies_reviews (list): A list of dictionaries, where each dictionary contains review information.

    Raises:
    - IndexError: If an error occurs while extracting review information from the HTML page.

    Note:
    - This function requires the following helper functions to be defined: `calculate_sentiment`, `create_unique_id`, `convert_date`.
    """
    companies_reviews = []
    stop_fetching = False

    reviews = soup.find_all('article', attrs={'class': 'paper_paper__1PY90 paper_outline__lwsUX card_card__lQWDv styles_reviewCard__hcAvl'})

    for review in reviews:
        try:

            date_of_review = review.find('time').get('datetime')
            date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
            datetime_of_review = datetime.strptime(date_of_review, date_format)

            if last_time_scraped and datetime_of_review <= last_time_scraped:
                stop_fetching = True
                break

            title = review.find('h2').get_text(strip=True)
            username = review.find('span', attrs={'class': 'typography_heading-xxs__QKBS8 typography_appearance-default__AAY17'}).get_text(strip=True)
            rating = review.find('div', attrs={'class': 'styles_reviewHeader__iU9Px'}).get('data-service-review-rating')
            content_p = review.find("p", { "class": "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn"})
            if content_p:
                content = content_p.get_text(strip=True)
            else:
                content = ""

            date_of_experience = review.find('p', attrs={'class': 'typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn'}).get_text(strip=True).replace("Date of experience:", "")
            answer = review.find("div", {"class": "paper_paper__1PY90 paper_outline__lwsUX paper_subtle__lwJpX card_card__lQWDv card_noPadding__D8PcU styles_wrapper__ib2L5"})
            if answer:
                author_answer = answer.find("p", {"class": "typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_weight-heavy__E1LTj styles_replyCompany__ro_yX"}).get_text(strip=True).replace("Reply from ", "")
                date_answer = answer.find("time").get('datetime')
                answer_content = review.find("p", {"class": "typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_message__shHhX"}).get_text(strip=True)
            else:
                author_answer = None
                date_answer = None
                answer_content = None

            label, accuracy = calculate_sentiment(content)
            review_scraped = {
                "company_name" : company_name,
                "title" : title,
                "username": username,
                "rating": rating,
                "content": content,
                "date_of_review": convert_date(date_of_review),
                "date_of_experience": convert_date(date_of_experience),
                "author_answer": author_answer,
                "date_answer": convert_date(date_answer),
                "answer_content": answer_content,
                "sentiment_score" : label,
                "accuracy_score" : accuracy
            }

            review_scraped['unique_hash'] = create_unique_id(review_scraped)

            companies_reviews.append(review_scraped)
        except AttributeError:
            raise IndexError("Error extracting review information from page")

    return stop_fetching, companies_reviews

def get_company_infos(soup):
    """
    This function extracts and returns company information from a parsed HTML page.

    Usage:
    company_info = get_company_infos(soup)

    Args:
    - soup (bs4.BeautifulSoup): A BeautifulSoup object representing the parsed HTML page.

    Returns:
    - company_info (dict): A dictionary containing the company information.

    Raises:
    - IndexError: If an error occurs while extracting company information from the HTML page.

    Note:
    - This function requires the helper function `create_unique_id` to be defined.
    """

    # Extract company information from the HTML elements
    company_name = soup.find('span', attrs={'class': 'typography_display-s__qOjh6 typography_appearance-default__AAY17 title_displayName__TtDDM'}).get_text(strip=True)
    company_rating = soup.find('p', attrs={'class': 'typography_body-l__KUYFJ typography_appearance-subtle__8_H2l'}).get_text(strip=True)
    ratings = soup.find_all('p', attrs={'class': 'typography_body-m__xgxZ_ typography_appearance-default__AAY17 styles_cell__qnPHy styles_percentageCell__cHAnb'})

    try:
        # Construct a dictionary containing the company information
        company = {
            "name" : company_name,
            "rating" : company_rating,
            "stars" : {
                "5" : ratings[0].get_text(strip=True),
                "4" : ratings[1].get_text(strip=True),
                "3" : ratings[2].get_text(strip=True),
                "2" : ratings[3].get_text(strip=True),
                "1" : ratings[4].get_text(strip=True),
            }
        }

        # Generate a unique ID for the company and insert the company information into Elasticsearch
        company['unique_hash'] = create_unique_id(company)
        insert_company_infos(company=company)

    except IndexError:
        # Raise an IndexError if an error occurs while extracting star ratings from the HTML page
        raise IndexError("Error extracting star ratings from page")

    return company



def fetch_page(base_url, current_page = 1, max_page = 1, company_name = "", last_time_scraped = None):
    """
    This function fetches a single page of reviews from a specified URL, parses the reviews, preprocesses them,
    and inserts them into Elasticsearch.

    Usage:
    stop_fetching, time_stopped, number_scraped = fetch_page(base_url, current_page, max_page, company_name, last_time_scraped)

    Args:
    - base_url (str): The base URL for the review pages to scrape.
    - current_page (int): The current page number to scrape (default 1).
    - max_page (int): The maximum number of pages to scrape (default 1).
    - company_name (str): The name of the company being scraped (default "").
    - last_time_scraped (datetime.datetime): The timestamp of the last review scraped (default None).

    Returns:
    - stop_fetching (bool): A boolean indicating whether to stop fetching reviews.
    - time_stopped (datetime.datetime): The timestamp of the last review scraped.
    - number_scraped (int): The number of reviews scraped from the page.

    Note:
    - This function requires the helper functions `get_html`, `get_reviews`, `preprocessing_review`, and `insert_review`
      to be defined.
    """
    print(f"Scraping page ({company_name}): {current_page}/{max_page}")

    # Fetching html for current page, parsing reviews and preprocess them
    html = get_html(f"{base_url}?page={current_page}")
    number_scraped = 0
    if html:
        soup = BeautifulSoup(html, "html.parser")
        stop_fetching, company_reviews = get_reviews(company_name, last_time_scraped, soup)
        company_reviews = preprocessing_review(reviews=company_reviews)

        insert_review(company_reviews)

        reviews_sorted = sorted(company_reviews, key=lambda k: k['date_of_review'], reverse=True)
        number_scraped = len(reviews_sorted)
        if len(reviews_sorted) > 0:
            time_stopped = reviews_sorted[0]["date_of_review"]
        else:
            time_stopped = last_time_scraped
    else:
        print("Impossible to get website html page")

    print(f"Review parsed for page : {current_page}")
    return stop_fetching, time_stopped, number_scraped

def scrap_url(url, testing = True):
    """
    Scrapes the reviews of a company from a given url using BeautifulSoup library and stores them in Elasticsearch index.

    Args:
    url (str): The url of the company page containing the reviews.

    Returns:
    int: The number of reviews scraped and stored in Elasticsearch index.
    """
    # First page content
    get_home_page_html = get_html(url)
    if not get_home_page_html:
        return

    soup = BeautifulSoup(get_home_page_html, "html.parser")
    # Finding page number
    if testing:
        last_page = 2
    else:
        last_page = soup.find('a', {"name":"pagination-button-last"}).find('span', {"class": "typography_heading-xxs__QKBS8 typography_appearance-inherit__D7XqR typography_disableResponsiveSizing__OuNP7"}).get_text()

    # Getting company infos
    company = get_company_infos(soup)
    
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
    last_scraping_time = get_last_scraping_time(company["name"])
    current_last_time_scraped = None
    if last_scraping_time:
        current_last_time_scraped = datetime.strptime(last_scraping_time, date_format)

    number_of_reviews_scraped = 0
    if not current_last_time_scraped:
        page = int(last_page)
        stop = False
        while (stop is False and page != 0):
            stop, time_stopped, number_scraped = fetch_page(url, page, last_page, company['name'])
            page -= 1
            set_last_scraped_at(company["name"], time_stopped)
            time.sleep(5)
            number_of_reviews_scraped += number_scraped
    else:
        page = 1
        stop = False
        scraped_time = None
        while (stop is False and page != last_page):
            stop, time_stopped, number_scraped = fetch_page(url, page, last_page, company['name'], current_last_time_scraped)
            if page == 1:
                scraped_time = time_stopped
            page += 1
            time.sleep(1)
            number_of_reviews_scraped += number_scraped

        set_last_scraped_at(company["name"], scraped_time)
    
    return number_of_reviews_scraped