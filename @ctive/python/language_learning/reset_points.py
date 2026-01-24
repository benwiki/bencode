import re
import os


def reset_points_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Regex pattern to find 'score:<number>' and replace it with 'score:0'
    pattern = r"score:-?\d+"
    updated_content = re.sub(pattern, "score:0", content)

    if updated_content == content:
        print(f"No changes made to file: {file_path}")
        return

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)
    print(f"Reset points in file: {file_path}")


def get_files_in(directory: str):
    return [
        file
        for f in os.listdir(directory)
        if os.path.isfile(file := os.path.join(directory, f))
    ]


if __name__ == "__main__":
    # List of files to reset points in
    files_to_reset = get_files_in("glossary")

    for file_path in files_to_reset:
        reset_points_in_file(file_path)
