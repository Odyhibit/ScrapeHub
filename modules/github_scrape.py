#  Josh Bloom
import requests
from bs4 import BeautifulSoup


def process_folders_files(page_soup: BeautifulSoup, github: str, last_update: str):
    raw_button = page_soup.find("a", {"id": "raw-url"})
    row_list = page_soup.find_all('div', {"role": "row"})

    if raw_button:
        filename = page_soup.find("strong", "final-path").text
        raw_content_url = github + page_soup.find('a', id="raw-url")['href']
        write_file(filename, raw_content_url)
        print("writing", filename, raw_content_url)
        return
    elif len(row_list) > 0:
        for row in row_list:
            url_link = row.find("a", "js-navigation-open Link--primary")
            update_timestamp = row.find("time-ago", "no-wrap")
            if url_link and update_timestamp and update_timestamp['datetime'] > last_update:
                process_folders_files(get_new_soup(github + url_link['href']), github, last_update)
                print(url_link['href'], update_timestamp['datetime'])

    else:
        print("no links found")


def get_new_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def write_file(filename: str, content_url: str):
    with open("github_downloads/" + filename, "wb") as file_out:
        content = requests.get(content_url)
        file_out.write(content.content)



if __name__ == "__main__":
    github_url = "https://github.com/vxunderground/MalwareSourceCode"
    last_update = "2020-08-20"
    process_folders_files(get_new_soup(github_url), "https://github.com", last_update)
