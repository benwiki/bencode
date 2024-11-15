import os
import re

error_regex = re.compile(r"\(Error #\d*\)")


def generate_error_codes(project_path: str) -> None:
    count = 1
    print("Generating error codes", end="")
    for path, _, files in os.walk(project_path):
        for file in files:
            if file.endswith(".py"):
                with open(f"{path}/{file}", "r", encoding="utf-8") as f:
                    file_lines = f.read().split('\n')
                for i, line in enumerate(file_lines):
                    if error_regex.search(line):
                        file_lines[i] = error_regex.sub(f"(Error #{count})", line)
                        count += 1
                with open(f"{path}/{file}", "w", encoding="utf-8") as f:
                    f.write("\n".join(file_lines))
                print(".", end="")
    print(" DONE!")
