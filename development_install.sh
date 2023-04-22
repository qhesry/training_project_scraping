# Create a new virtual environment
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install dependencies for dash app
pip install -r ./dash/requirements.txt

# Install dependencies for fast API app
pip install -r ./fastapi/requirements.txt

# Install dependencies for scraping app
pip install -r ./scraping/requirements.txt