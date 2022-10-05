from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup


def scrape_github(page_soup: BeautifulSoup,  last_update: str, output_dir: str):
    raw_button = page_soup.find("a", {"id": "raw-url"})
    row_list = page_soup.find_all('div', {"role": "row"})
    github = "https://github.com/"
    if raw_button:
        filename = page_soup.find("strong", "final-path").text
        raw_content_url = github + page_soup.find('a', id="raw-url")['href']
        write_file(output_dir, filename, raw_content_url)
        print("writing", filename, raw_content_url)
        return
    elif len(row_list) > 0:
        for row in row_list:
            url_link = row.find("a", "js-navigation-open Link--primary")
            update_timestamp = row.find("time-ago", "no-wrap")
            if url_link and update_timestamp and update_timestamp['datetime'] > last_update:
                scrape_github(get_new_soup(github + url_link['href']), last_update, output_dir)
                print(url_link['href'], update_timestamp['datetime'])
    else:
        print("no links found")


def get_new_soup(url: str) -> BeautifulSoup:
    r = requests.get(url)
    return BeautifulSoup(r.text, 'html.parser')


def write_file(output_dir: str, filename: str, content_url: str):
    with open(output_dir + filename, "wb") as file_out:
        content = requests.get(content_url)
        file_out.write(content.content)


def get_last_update(filename: str) -> str:
    with open(filename, "r") as update:
        return update.readline().strip()


def set_last_update(filename: str):
    with open(filename, "w") as output:
        github_dt = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        output.write(github_dt)


if __name__ == "__main__":
    github_url = "https://github.com/vxunderground/MalwareSourceCode"
    output_dir = "../github_downloads/"
    last_update = "2020-08-20"
    scrape_github(get_new_soup(github_url), last_update, output_dir)
