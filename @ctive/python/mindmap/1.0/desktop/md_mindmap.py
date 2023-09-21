"""
This allows for displaying a single mindmap written in a markdown file
"""

# from mindmaps import mindmap_draw
from map import md_helper as mindmap_draw
import sys


def extract_mindmap(filename: str):
    """
    This extracts the fenced mindmap code-block from the passed markdown file
    args:
        filename: the filename/path of the markdown file
    returns:
        a multiline str of the mindmap code
    """
    code_fence_begin = "```mindmap"
    code_fence_end = "```"
    output_string: str = ""

    # read the file
    is_in_codeblock = False
    with open(filename) as file:
        candidates = file.readlines()
    for candidate in candidates:
        # check if codeblock ends
        if code_fence_end in candidate:
            is_in_codeblock = False
        # append to output
        if is_in_codeblock:
            output_string += candidate
        # check if codeblock beginns
        if code_fence_begin in candidate:
            is_in_codeblock = True

    return output_string.strip()


def main():
    # This could be vastly improved by using a proper cmd library like click or argparse
    md_file = sys.argv[1]

    mindmap_text = extract_mindmap(md_file)
    mindmap_draw(mindmap_text)


if __name__ == "__main__":
    main()
