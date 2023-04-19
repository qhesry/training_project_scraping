import json
import os

with open(f"{os.getcwd()}/config.json") as f:
    config = json.load(f)["elasticsearch"]