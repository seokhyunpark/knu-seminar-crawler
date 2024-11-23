import requests
from bs4 import BeautifulSoup


def fetch_body_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        body = soup.find('body')
        if body:
            return body.get_text(strip=True).split("목록")[0]
        else:
            print("[ERROR] CANNOT FIND BODY TAG")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] HTTP REQUEST ERROR: {e}")
