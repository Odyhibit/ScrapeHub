import os
import pathlib
import subprocess


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



if __name__ == "__main__":
    archive_ext = [".gz", ".zip", ".rar", ".7z"]
    dangerous_ext = [".exe", ".bat", ".ps1", ".css", ".html", ".htm", ".LNK", ".VBE", ".cmd", ".sh",
                            ".js", ".vb", ".vbs", ".jar", ".doc", ".docm", ".docx", ".eml", ".ini", ".msi",
                            ".ppt", ".xls", ".xlsx", ".xlsm"]
    extract_defang(pathlib.Path("../test/test_downloads"), archive_ext, dangerous_ext)
