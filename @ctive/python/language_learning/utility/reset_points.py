"""
Script to reset point values in specified files within the 'assets/glossaries' directory.
It searches for patterns like 'score:<number>' and replaces them with 'score:0'.
"""

import re
import os


def reset_points_in_file(file_path: str) -> None:
    """
    Resets point values in the specified file by replacing 'score:<number>' with 'score:0'.

    :param file_path: The path to the file to be processed.
    """
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


def get_files_in(directory: str) -> list[str]:
    """
    Retrieves a list of file paths in the specified directory.

    :param directory: The directory to search for files.
    :return: A list of file paths.
    """
    return [
        file
        for f in os.listdir(directory)
        if os.path.isfile(file := os.path.join(directory, f))
    ]


if __name__ == "__main__":
    # List of files to reset points in
    files_to_reset = get_files_in(os.path.join("assets", "glossaries"))

    for path_to_file in files_to_reset:
        reset_points_in_file(path_to_file)
