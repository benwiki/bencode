"""Find files with the same name but different content in two directories"""

import os

def find_files_with_same_name_different_content(dir1, dir2):
    """Find files with the same name but different content in two directories"""
    files_with_diff_content = []
    for root, _, files in os.walk(dir1):
        for file_name in files:
            file_path1 = os.path.join(root, file_name)
            file_path2 = os.path.join(dir2, file_name)
            if os.path.exists(file_path2):
                file_content1 = open(file_path1, 'r', encoding="utf-8").read()
                file_content2 = open(file_path2, 'r', encoding="utf-8").read()
                if file_content1 != file_content2:
                    files_with_diff_content.append(file_name)
    files_with_diff_content.sort()
    return files_with_diff_content


def main():
    """The main function"""
    dir1 = r"G:\Meine Ablage\Dokumentumok\Tanulás_suli\Továbbtanulás\Uni\Sonstiges\Anfang\Sprachenlernen - DSH\Sprachprogramm"
    dir2 = r"C:\Users\b.hargitai\prog\bencode\archive\0Prog\Python\nyelv"

    files_with_diff_content = find_files_with_same_name_different_content(dir1, dir2)

    if files_with_diff_content:
        print("Files with different content:")
        for file_name in files_with_diff_content:
            print(file_name)
    else:
        print("No files with different content found")


if __name__ == "__main__":
    main()
