import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re


def preprocessing_review(reviews):
    """
    Preprocesses the reviews by performing the following steps:
    - Splitting the title into keywords and removing non-alphabetic characters.
    - Removing HTML tags and special characters from the review content.
    - Converting text to lowercase.
    - Tokenizing text and removing stop words.
    - Lemmatizing words.

    Args:
    reviews (list): A list of reviews to be preprocessed.

    Returns:
    list: A list of preprocessed reviews.
    """
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    for review in reviews:

        # Split the title into keywords and remove non-alphabetic characters
        title_lower = review['title'].lower()

        words_title = [word for word in nltk.word_tokenize(title_lower) if word not in stop_words]
        
        # Add the keywords to the document
        review["title_keywords"] = words_title

        # Remove HTML tags and special characters
        text = re.sub('<[^<]+?>', '', review["content"])
        text = re.sub('[^a-zA-Z0-9\s]', '', text)

        # Convert text to lowercase
        text = text.lower()

        # Tokenize text and remove stop words
        words = [word for word in nltk.word_tokenize(text) if word not in stop_words]

        # Lemmatize words
        words = [lemmatizer.lemmatize(word) for word in words]

        processed_text = ' '.join(words)

        # Add the processed text to the review
        review["processed_text"] = processed_text

    return reviews