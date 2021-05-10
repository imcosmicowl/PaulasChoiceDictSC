import os

import requests
from bs4 import BeautifulSoup
from googlesearch import search


def color_string(code):
    """"https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python"""
    if code == 'Best':  # BEST
        return '\x1b[6;30;44m'
    elif code == 'Good':  # GOOD
        return '\x1b[6;30;42m'
    elif code == 'Average':  # AVERAGE
        return '\x1b[6;30;43m'
    elif code == 'Poor':  # POOR
        return '\x1b[6;30;41m'
    else:
        return '\x1b[6;30;47m'


def get_page_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"}
    page = requests.get(url, headers=headers)
    return page.content


def search_request(skincare_ingredient):
    paulas_url = search(query=skincare_ingredient + " paula's choice", num=1)
    try:
        content = get_page_html(next(paulas_url))
    except:
        return "NONE", None
    soup = BeautifulSoup(content, 'html.parser')
    ratting = soup.find('span', {"class": "rating-best"})
    if ratting is None:
        ratting = soup.find('span', {"class": "rating-good"})
        if ratting is None:
            ratting = soup.find('span', {"class": "rating-average"})
            if ratting is None:
                ratting = soup.find('span', {"class": "rating-poor"})
                if ratting is None:
                    ratting = "NONE"
                    return ratting, None
    text = soup.get_text()
    star_indx = text.find("Categories:") + 11
    end_indx = text.find("References for this information:")
    if end_indx == -1:
        end_indx = text.find("Back to Ingredient Dictionary")
    return ratting.text, text[star_indx:end_indx]


if __name__ == '__main__':

    while True:
        ingredient = input("Enter an ingredient:")

        if ingredient == 'exit' or ingredient == 'e':
            break
        ratting, text = search_request(ingredient)
        print("\033[4mRatting:\033[0m", color_string(ratting) + ratting + '\x1b[0m')
        if text is None:
            print(color_string(ratting) + "INGREDIENT NOT FOUND" + '\x1b[0m')
        else:
            print("\033[4mCategories:\033[0m", text)

        os.remove("./.google-cookie")
