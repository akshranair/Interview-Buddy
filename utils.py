import requests
from bs4 import BeautifulSoup
def get_response(url, variables, query, headers):
    response = requests.post(
        url,
        json = {"variables":variables, "query":query},
        headers=headers,
        timeout=10)
    
    return response

def clean_text(html_text):
    text = BeautifulSoup(html_text, "html.parser").get_text()
    clean_text = text.replace('\n', ' ')
    clean_text = clean_text.replace('\xa0', ' ')