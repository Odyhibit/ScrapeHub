import os
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup


def scrape_website(page_soup: BeautifulSoup, last_update: str, output_dir: str):
    table_rows = page_soup.find_all('tr')
    for i, row in enumerate(table_rows):
        if i > 1:
            link = row.find('a')['href']
            date = row.find('td', class_='date').text
            if link[-1] == "/":
                scrape_website(get_new_soup(link), last_update, output_dir)
            elif date > last_update:
                filename = get_filename_from_url(link)
                print(filename, date)
                write_file(output_dir, filename, link)


def get_filename_from_url(url: str) -> str:
    index = url.find("/", 4)
    return url[index + 1:]


def get_folder(filename: str) -> str:
    return filename[:filename.rfind("/")+1]


def get_new_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def write_file(output_dir: str, filename: str, content_url: str):
    os.makedirs(output_dir + get_folder(filename), exist_ok=True)
    with open(output_dir + filename, "wb") as file_out:
        content = requests.get(content_url)
        file_out.write(content.content)


def get_last_update(filename: str) -> str:
    with open(filename, "r") as update:
        return update.readline().strip()


def set_last_update(filename: str):
    with open(filename, "w") as output:
        website_dt = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        output.write(website_dt)


if __name__ == "__main__":
    github_url = "https://samples.vx-underground.org/samples/"
    output_dir = "../website_downloads"
    last_update = get_last_update("../last_update/vx_underground_website_date")
    scrape_website(get_new_soup(github_url), last_update, output_dir)
