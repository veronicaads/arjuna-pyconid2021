import argparse
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import asyncio
from pyppeteer import launch


async def scraper(user_email, password, depth):
    # new browser
    browser = await launch()
    login_page = await browser.newPage()
    await login_page.goto("https://account.kompas.id/login")

    input_element = await login_page.querySelectorAll('input.bg-white')
    await input_element[0].type(user_email)
    await input_element[1].type(password)

    login_button_element = await login_page.querySelector('button.btn-submit')
    await login_button_element.click()

    print("Success to login")

    # scroll down as the depth param
    await login_page.goto("https://www.kompas.id/kategori/sastra/")

    for i in tqdm(range(int(depth))):
        element = await login_page.querySelector('span.text-xl')
        if element is None:
            break
        await element.click()
        time.sleep(10)

    print("Success scrolled down")

    # get link as list
    page_html = await login_page.content()
    soup = BeautifulSoup(page_html, 'html.parser')
    sastra_link_list = []
    for a in soup.find_all('a', href=True):
        if '/baca/' in a['href']:
            sastra_link_list.append(a['href'])

    print("Start to scrape link from the list")

    sastra_dataset = []
    article_number = 0
    for link in tqdm(list(set(sastra_link_list))):
        article_number += 1
        go_to_link = 'https://www.kompas.id' + link
        try:
            await login_page.goto(go_to_link)
            sub_page_html = await login_page.content()
            inner_soup = BeautifulSoup(sub_page_html, 'html.parser')
            article = inner_soup.findAll('p', class_=False, id=False)
            sentence_nummber = 0
            for element in article[:-2]:
                sentence_nummber += 1
                sastra_dataset.append(
                    {"link" : go_to_link,
                    "sentence_number": f"kalimat_{sentence_nummber}",
                    "article_number": article_number,
                    "text" : element.text})
        except:
            # get navigation timeout error
            time.sleep(5)
        time.sleep(5)

    return pd.DataFrame(sastra_dataset)


def get_title(x):
    element = x.split("/")
    return element[-1].replace('-',' ')


async def main(**kwargs):
    user_email = kwargs["user_email"]
    password = kwargs["password"]
    depth = kwargs["depth"]

    print("Start scraping process")
    dataset = await scraper(user_email, password, depth)
    
    # cleaning
    dataset = dataset[dataset['text'] != '']
    dataset['title'] = dataset.apply(lambda x: get_title(x['link']), axis=1)

    # the dataset will be saved in the same path as the python script
    dataset.to_csv('dataset.csv', index=False)

    print(f"Scraper process is done and get {dataset.article_number.nunique()} unique article")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kompas Sastra Web Scraper")

    parser.add_argument(
        "--user_email",
        dest="user_email",
        required=True,
        help="Kompas.id user email that you registered",
    )
    parser.add_argument(
        "--password",
        dest="password",
        required=True,
        help="Kompas.id user password that you registered",
    )

    parser.add_argument(
        "--depth",
        dest="depth",
        required=True,
        help="Scroll depth for get list of sastra link (e.g 100)",
    )

    args = parser.parse_args()
    asyncio.run(main(**vars(args)))
