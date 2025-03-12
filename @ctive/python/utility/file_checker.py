import difflib
import filecmp
import json
import os

# original = "/Users/robertsonwang/Desktop/CS 229/Project/CS229_Project/data/processed_data/processed_data.csv"


def compare_directories(original, new):
    def get_all_files(directory):
        all_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                all_files.append(os.path.relpath(os.path.join(root, file), directory))
        return set(all_files)

    original_files = get_all_files(original)
    new_files = get_all_files(new)

    added = list(new_files - original_files)
    removed = list(original_files - new_files)
    changed = {}

    common_files = original_files & new_files
    for file in common_files:
        original_file_path = os.path.join(original, file)
        new_file_path = os.path.join(new, file)
        if not filecmp.cmp(original_file_path, new_file_path, shallow=False):
            with open(original_file_path, "r") as orig_file, open(
                new_file_path, "r"
            ) as new_file:
                orig_content = orig_file.readlines()
                new_content = new_file.readlines()
                difference = [line for line in orig_content if line not in new_content]
                difference2 = [line for line in new_content if line not in orig_content]
                changed[file] = (difference, difference2)
                # diff = difflib.unified_diff(
                #     orig_content.splitlines(), new_content.splitlines()
                # )
                # changed[file] = "\n".join(diff)

    return {"added": added, "removed": removed, "changed": changed}


# Example usage:
result = compare_directories(
    "/Users/benke/Downloads/sziamuhely_wp",
    "/Users/benke/Downloads/sziamuhely_wp_ERROR",
)
with open("result.json", "w") as f:
    f.write(json.dumps(result, indent=4))
