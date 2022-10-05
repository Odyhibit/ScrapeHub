import os
import pathlib
import subprocess


def process_archive(this_archive: pathlib.Path, this_directory: pathlib.Path):
    new_dir = str(this_directory) + "/" + pathlib.Path(this_archive).stem.replace(".", "_")
    os.makedirs(new_dir, exist_ok=True)
    destination = pathlib.Path(new_dir)
    print(this_archive, "->", pathlib.Path(this_archive.parent, destination))
    extract = subprocess.run(["7z", "x", "-pinfected", "-o" + new_dir, this_archive])
    print("7z", "x", "-o" + new_dir, this_archive)
    if extract.check_returncode() == 0:
        os.remove(this_archive)
        extract_defang(pathlib.Path(new_dir))
    else:
        print("ERROR extracting", this_archive)


def make_benign(this_file: pathlib.Path):
    os.rename(this_file, str(this_file) + "_")


def extract_defang(this_directory: pathlib.Path):
    dir_list = pathlib.Path(this_directory)
    for item in dir_list.iterdir():
        if item.is_dir():
            extract_defang(item)
        if item.is_file():
            if pathlib.Path(item).suffix in archive_extensions:
                process_archive(item, this_directory)
            if pathlib.Path(item).suffix in dangerous_extensions:
                make_benign(item)


if __name__ == "__main__":
    archive_extensions = [".gz", ".zip", ".rar", ".7z"]
    dangerous_extensions = [".exe", ".bat", ".ps1", ".css", ".html", ".htm", ".LNK", ".VBE", ".cmd", ".sh",
                            ".js", ".vb", ".vbs", ".jar", ".doc", ".docm", ".docx", ".eml", ".ini", ".msi",
                            ".ppt", ".xls", ".xlsx", ".xlsm"]
    extract_defang(pathlib.Path("../github_downloads"))
