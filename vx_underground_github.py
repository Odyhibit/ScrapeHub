from modules.scrape_github import *
from modules.extract_defang import *

github_url = "https://github.com/vxunderground/MalwareSourceCode"
output_dir = "github_downloads/"
archive_extensions = [".gz", ".zip", ".rar", ".7z"]
dangerous_extensions = [".exe", ".bat", ".ps1", ".css", ".html", ".htm", ".LNK", ".VBE", ".cmd", ".sh",
                        ".js", ".vb", ".vbs", ".jar", ".doc", ".docm", ".docx", ".eml", ".ini", ".msi",
                        ".ppt", ".xls", ".xlsx", ".xlsm"]
last_update = get_last_update("vx_underground_github_date")
scrape_github(get_new_soup(github_url), last_update, output_dir)
extract_defang(pathlib.Path("github_downloads"))
set_last_update("vx_underground_github_date")
