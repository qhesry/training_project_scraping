## Project Title: TrustPilot Review Scraper for NordVPN and CyberGhost VPN

This project is a web scraping tool that extracts reviews about NordVPN and CyberGhost VPN from Trustpilot.com. The extracted reviews are then stored in Elasticsearch, which serves as the database for the application. Finally, a FastAPI-based API is used to serve the data to a Dash app, where users can visualize the data and gain insights into the opinions and experiences of others who have used these VPN services.

## Prerequisites

Before you can run this project, you will need to install the following dependencies:

- Python 3.8 or higher
- Elasticsearch
- FastAPI
- Dash
- Beautiful Soup 4
- Requests

## Installation

1. Clone this repository to your local machine.
2. You need to install an elasticsearch database and change the connection credentials in `fastapi/main.py` and in `scraping/database_utils.py`
3. Install the required dependencies by running `pip install -r requirements.txt` in your terminal.
4. Run the scraper by executing `python scraping/main.py`.
5. Run the FastAPI server by executing `uvicorn server:app --reload` while in the fast api folder.
6. Run the Dash app by executing `python dash/dash_app.py` while in the dash folder.
7. Open a web browser and navigate to [http://localhost:8050](http://localhost:8050) to view the dashboard.

## Usage

Once the application is running, you can use the Dash app to view some metrics example.

## Credits

This project was created by Quentin Hesry as a demonstration of web scraping, Elasticsearch, FastAPI, and Dash. 
It is intended for training only and should not be used for any commercial purposes.
