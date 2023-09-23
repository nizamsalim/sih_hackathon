from requests import get
from bs4 import BeautifulSoup
from ordered_set import OrderedSet
from time import sleep
import json
# from translation import translateData



def scrape_index_page():
    url = "https://pib.gov.in/indexd.aspx"
    response = get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    release_links = soup.select(".release_list a")

    links = []
    for link in release_links:
        href = link.get("href")
        if href and "ReleseDetail" in href:
            release_page_link = f"https://pib.gov.in{href.replace('ReleseDetail', 'ReleasePage')}"
            links.append(release_page_link)

    return links


def filter_unwanted_links(image_links, unwanted):
    filtered_links = []
    for link in image_links:
        if not any(keyword in link for keyword in unwanted):
            filtered_links.append(link)
    return filtered_links


def scrape_text_and_images(url):
    response = get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Remove unwanted content
    unwanted_tags = soup.select(
        "img[src*='facebook'], img[src*='whatsapp'], img[src*='email'], img[src*='linkedin']")
    for tag in unwanted_tags:
        tag.extract()

    # Extract text
    text_elements = soup.select("span")
    text_elements = set([element.get_text(strip=True)
                         for element in text_elements])
    sorted(text_elements)
    # text_set = OrderedSet([element.get_text(strip=True)
    #                       for element in text_elements])
    text = " ".join(text_elements)

    # Extract image links
    image_tags = soup.find_all("img", src=True)
    image_links = [tag["src"] for tag in image_tags]

    return text, image_links


# Define unwanted image links
unwanted_image_keywords = ["ph2023818240601.jpg",
                           "ph202183101", "ph20221121131401"]

url_list = scrape_index_page()

text_list = list()


def scrapeData():
    # file = open("./texts.txt", "w", encoding="utf-8")
    i = 0
    for url in url_list:
        text, image_links = scrape_text_and_images(url)
        filtered_image_links = filter_unwanted_links(
            image_links, unwanted_image_keywords)
        n = len(url_list)
        # file.write(text)
        # print(text, end="\n----------------------------------------------------\n")
        text_list.append(text)

    # json_obj = json.dumps(text_list[2:n])
    # with open("./texts.json", "w") as o_file:
    #     o_file.write(json_obj)


    # file.writelines(text_list)
    # file.close()

    # file = open("./texts.txt", "r", encoding="utf-8")
    # # print(file.readlines())
    # for i in file.readlines():
    #     print(i)
    #     print("\n----------------------------------------------------------------\n")
    #     # sleep(5)


scrapeData()
