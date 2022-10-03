import os
import pathlib
import subprocess


def process_archive(this_archive: pathlib.Path,this_directory: pathlib.Path):
    new_dir = str(this_directory) + "/" + pathlib.Path(this_archive).stem.replace(".", "_")
    os.makedirs(new_dir, exist_ok=True)
    destination = pathlib.Path(new_dir)
    print(this_archive, "->", pathlib.Path(this_archive.parent, destination))
    extract = subprocess.run(["7z", "x", "-pinfected", "-o" + new_dir, this_archive])
    print("7z", "x", "-o" + new_dir, this_archive)
    if not extract.stderr:
        os.remove(this_archive)


def make_benign(this_file: pathlib.Path):
    os.rename(this_file, str(this_file) + "_")


def process_dir(this_directory: pathlib.Path):
    this_path = pathlib.Path(this_directory)
    for item in this_path.iterdir():
        if item.is_dir():
            process_dir(item)
        if item.is_file():
            if pathlib.Path(item).suffix in archive_extensions:
                process_archive(item,this_directory)
            if pathlib.Path(item).suffix in dangerous_extensions:
                make_benign(item)


if __name__ == "__main__":
    archive_extensions = [".gz", ".zip", ".rar", ".7z"]
    dangerous_extensions = [".exe", ".bat", ".ps1", ".css", ".html", ".htm", ".LNK", ".VBE", ".cmd", ".sh",
                            ".js", ".vb", ".vbs", ".jar", ".doc", ".docm", ".docx", ".eml", ".ini", ".msi",
                            ".ppt", ".xls", ".xlsx", ".xlsm"]

    process_dir(pathlib.Path("../github_downloads"))
