"""
This library is used for the fractalMap project,
connecting the mindmap features with
markdown features
"""

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
    with open(filename, encoding="utf-8") as file:
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
