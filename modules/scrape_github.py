import os
import sqlite3
import urllib.parse
import requests


def scrape_github(url: str, connection: sqlite3.Connection, db_cur: sqlite3.Cursor, output_dir: str):
    github = "https://github.com/"
    page_source = requests.get(url).text

    raw_button = get_raw_button(page_source)
    file_list = get_file_list(page_source)

    if raw_button != "":
        filename = raw_button
        if not in_db(filename, db_cur):
            insert_new(filename, db_cur)
            write_file(output_dir, filename, github + filename)
            connection.commit()
            print(filename)
        return
    elif len(file_list) > 0:
        for file in file_list:
            scrape_github("https://github.com" + file, connection, db_cur, output_dir)

    else:
        print("no links found")


def insert_new(filename: str, cursor: sqlite3.Cursor):
    cursor.execute('INSERT INTO filenames(name) VALUES(?)', (filename,))
    return


def in_db(filename: str, cursor: sqlite3.Cursor) -> bool:
    cursor.execute('SELECT count(name) FROM filenames WHERE  name = ? ', (filename,))
    found = cursor.fetchone()
    if found[0] > 0:
        return True
    return False


def get_raw_button(page_source: str) -> str:
    end = page_source.find('" id="raw-url"')
    if not end > 0:
        return ""
    start = page_source.rfind('href="', 0, end) + 6
    return urllib.parse.unquote(page_source[start:end])


def get_file_list(page_source: str) -> [str]:
    file_list = []
    while "js-navigation-open Link--primary" in page_source:
        link_class = page_source.find("js-navigation-open Link--primary")
        start = page_source.find('href="', link_class) + 6
        end = page_source.find('"', start)
        file_list.append(urllib.parse.unquote(page_source[start:end]))
        page_source = page_source[end:]
    return file_list


def get_folder(filename: str) -> str:
    return filename[:filename.rfind("/") + 1]


def write_file(output_dir: str, filename: str, content_url: str):
    filename = urllib.parse.unquote(filename)
    os.makedirs(output_dir + get_folder(filename), exist_ok=True)
    with open(output_dir + filename, "wb") as file_out:
        content = requests.get(content_url)
        file_out.write(content.content)


if __name__ == "__main__":
    con = sqlite3.connect('../github_files.db')
    cur = con.cursor()
    print(in_db("test", cur))
    github_url = "https://github.com/Odyhibit/nested_compressed_folders"
    # test = requests.get(github_url)
    files = get_file_list(github_url)
    for item in files:
        print(item)
    '''
    sqlite_connection = get_connection("../github_files.db")
    github_url = "https://github.com/vxunderground/MalwareSourceCode"
    output_dir = "../github_downloads/"
    last_update = "2020-08-20"
    scrape_github(github_url, sqlite_connection, output_dir)
    '''
