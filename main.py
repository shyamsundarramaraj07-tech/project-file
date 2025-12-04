import requests
import numpy as np

def fetch_data():
    response = requests.get('https://api.github.com')
    return response.json()

if __name__ == "__main__":
    data = fetch_data()
    print("GitHub API Status:", data)