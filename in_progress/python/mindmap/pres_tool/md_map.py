"""
This allows for displaying a single mindmap written in a markdown file
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-
# import tkinter

from mdMapTools import extract_mindmap
from map import run_map as draw_map
import sys

def main():
    # This could be vastly improved by using a proper cmd library like click or argparse
    md_file = sys.argv[1]

    mindmap_text = extract_mindmap(md_file)
    draw_map(mindmap_text)


if __name__ == "__main__":
    main()
