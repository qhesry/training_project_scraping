## TrustPilot Review Scraper for NordVPN and CyberGhost VPN

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
2. Launch the docker-compose file using `docker-compose up -d`
3. Open a web browser and navigate to [http://localhost:8050](http://localhost:8050) to view the dashboard.

## Usage

Once the application is running, you can use the Dash app to view some metrics example.

## Credits

This project was created by Quentin Hesry as a demonstration of web scraping, Elasticsearch, FastAPI, and Dash. 
It is intended for training only and should not be used for any commercial purposes.
