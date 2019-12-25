from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # first run: sudo apt-get install firefox-geckodriver


def scroll_down(driver):
    """A method for scrolling the page.
    reference: https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-indynamically-loading-webpage
    """

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(1)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height


def scrape_user_data_from_username(username=None, inc_watching=True):
    """
    Function to scrape user data to ensure that we aren't giving recommendations from the
    animes they've already seen or are watching

    :param username: (str) the username of the individual
    :param inc_watching: (Bool) Flag to say if we want to scrape from their watching list
    :return: (pd.Dataframe) user information dataframe
    """
    # reference: http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
    df = pd.DataFrame(columns=['animeID', 'scored', 'status'])
    pos = 0
    if username:
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.get('https://myanimelist.net/animelist/' + username)
        scroll_down(driver)
        html_page = driver.page_source
        driver.quit()

        vals = []
        soup = BeautifulSoup(html_page, "html.parser")
        for anime_row in soup.find_all('tbody', class_='list-item'):

            if anime_row.find('td', class_='data status watching') and inc_watching:
                anime_id = anime_row.find('a', class_='link sort')['href'].split('/')[-2]

                bad_chars = str.maketrans(dict.fromkeys("\n[]', "))
                anime_scored = anime_row.find('td', class_='data score').text
                anime_scored = anime_scored.translate(bad_chars)
                if anime_scored == '-':
                    anime_scored = 0

                vals.append(int(anime_id))
                vals.append(int(anime_scored))
                vals.append('watching')

                # anime_id and anime_scored
                df.loc[pos] = vals
                vals = []
                pos += 1

            elif anime_row.find('td', class_='data status completed'):
                anime_id = anime_row.find('a', class_='link sort')['href'].split('/')[-2]

                bad_chars = str.maketrans(dict.fromkeys("\n[]', "))
                anime_scored = anime_row.find('td', class_='data score').text
                anime_scored = anime_scored.translate(bad_chars)
                if anime_scored == '-':
                    anime_scored = 0

                vals.append(int(anime_id))
                vals.append(int(anime_scored))
                vals.append('completed')

                # anime_id and anime_scored
                df.loc[pos] = vals
                vals = []
                pos += 1
        print(pos)

    return df


def scrape_image_url(anime_id):
    """
    Scrapes anime url from myanimelist.net using the anime_id

    :param (str) anime id to scrape image from
    :return: (str) the url to the image of the anime
    """
    source = requests.get('https://myanimelist.net/anime/' + str(anime_id))
    if source.status_code == 200:
        soup = BeautifulSoup(source.text, "html.parser")
        anime_img_url = soup.find('img', class_='ac')['src']
    else:
        anime_img_url = str(source.status_code)

    return anime_img_url

