import requests
from bs4 import BeautifulSoup


def scrape_website_storage_requirements(page_soup: BeautifulSoup, last_update: str):
    global total_size
    global file_count
    table_rows = page_soup.find_all('tr')
    for i, row in enumerate(table_rows):
        if i > 1:
            link = row.find('a')['href']
            date = row.find('td', class_='date').text
            size = row.find('td', class_='size').text
            if link[-1] == "/":
                scrape_website_storage_requirements(get_new_soup(link), last_update)
            elif date > last_update:
                filename = get_filename_from_url(link)
                print(filename, size, date)
                total_size += int(size)
                file_count += 1


def get_filename_from_url(url: str) -> str:
    index = url.find("/", 4)
    return url[index + 1:]


def get_folder(filename: str) -> str:
    return filename[:filename.rfind("/") + 1]


def get_new_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


if __name__ == "__main__":
    github_url = "https://samples.vx-underground.org/samples/"
    update = "2022-10-08 06:58:30"
    total_size = 0
    file_count = 0
    scrape_website_storage_requirements(get_new_soup(github_url), update)
    print("Total Download size is", total_size, "and there are", file_count, "files")
