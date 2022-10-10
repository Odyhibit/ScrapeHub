import os
import pathlib
import subprocess
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


def process_archive(this_archive: pathlib.Path, this_directory: pathlib.Path, archive_extensions, dangerous_extensions):
    new_dir = str(this_directory) + "/" + pathlib.Path(this_archive).stem.replace(".", "_")
    os.makedirs(new_dir, exist_ok=True)
    extract = subprocess.run(["7z", "x", "-y", "-pinfected", "-o" + new_dir, this_archive], capture_output=True)
    # print("7z", "  x", " -y", " -o" + new_dir, this_archive)
    print("Extracting", this_archive)
    if extract.returncode == 0:
        print(in_green("Success"))
        if pathlib.Path(this_archive).is_file():
            extract_defang(pathlib.Path(new_dir), archive_extensions, dangerous_extensions)
        os.remove(this_archive)
    else:
        print(in_red("ERROR"), "extracting", this_archive, "return code", extract.returncode)


def make_benign(this_file: pathlib.Path):
    os.rename(this_file, str(this_file) + "_")
    if pathlib.Path(this_file).is_file():
        cwd = os.getcwd()
        os.remove(cwd + "/" + str(this_file))


def extract_defang(this_directory: pathlib.Path, archive_extensions:[str], dangerous_extensions:[str]):
    dir_list = pathlib.Path(this_directory)
    for item in dir_list.iterdir():
        if item.is_dir():
            extract_defang(item, archive_extensions, dangerous_extensions)
        if item.is_file():
            if pathlib.Path(item).suffix in archive_extensions:
                process_archive(item, this_directory, archive_extensions, dangerous_extensions)
            if pathlib.Path(item).suffix in dangerous_extensions:
                make_benign(item)


def in_green(text: str) -> str:
    return "\033[32;1m" + str(text) + "\033[0m"


def in_red(text: str) -> str:
    return "\033[31m" + str(text) + "\033[0m"


github_url = "https://github.com/Odyhibit/nested_compressed_folders"
output_dir = "test_downloads/"
archive_extensions = [".gz", ".zip", ".rar", ".7z"]
dangerous_extensions = [".exe", ".bat", ".ps1", ".css", ".html", ".htm", ".LNK", ".VBE", ".cmd", ".sh",
                        ".js", ".vb", ".vbs", ".jar", ".doc", ".docm", ".docx", ".eml", ".ini", ".msi",
                        ".ppt", ".xls", ".xlsx", ".xlsm"]

print("Connect to db")
connection = sqlite3.connect('../github_files.db')
cur = connection.cursor()

print("Scraping", github_url)
scrape_github(github_url, connection, cur, output_dir)

print("Extracing folder", output_dir)
extract_defang(pathlib.Path(output_dir), archive_extensions, dangerous_extensions)

