from modules.scrape_website import *
from modules.extract_defang import *

website_url = "https://samples.vx-underground.org/samples/"
output_dir = "website_downloads/"
date_file = "last_update/vx_underground_website_date"
archive_extensions = [".gz", ".zip", ".rar", ".7z"]
dangerous_extensions = [".exe", ".bat", ".ps1", ".css", ".html", ".htm", ".LNK", ".VBE", ".cmd", ".sh",
                        ".js", ".vb", ".vbs", ".jar", ".doc", ".docm", ".docx", ".eml", ".ini", ".msi",
                        ".ppt", ".xls", ".xlsx", ".xlsm"]

last_update = get_last_update(date_file)
scrape_website(get_new_soup(website_url), last_update, output_dir)
set_last_update(date_file)
extract_defang(pathlib.Path(output_dir))

