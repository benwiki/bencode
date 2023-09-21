import os
import sys
from map import MindMap, Node, ProgressStyle
from map import DARK_THEME, LIGHT_THEME
import tkinter as tk
from tkinter.filedialog import askdirectory


def get_tree_from_path(
        path: str, root='', parent=None, layer=0, 
        ) -> Node:
    full_path = f'{root + path}\\'
    if parent is None:
        path = get_last_from_path(path)

    node = Node(path, 0, parent, [], {
        'path': full_path, 'isdir': True, 'layer': layer})
    try:
        folder = next(os.walk(full_path))
    except StopIteration:
        return node

    for subfolder in folder[1]:
        node.children.append(
            get_tree_from_path(subfolder, full_path, node, layer + 1))
    for file in folder[2]:
        node.children.append(
            Node(file, 0, node, [], {
                'path': full_path + file,
                'isfile': True
            }))
    return node


def get_last_from_path(path: str) -> str:
    return path.split('/')[-1].split('\\')[-1]


def handle_key(key: tk.Event, node: Node, selected: int):
    path: str
    match key.keysym:
        case 'O' | 'Return' if key.state == 1:
            path = node['path']
        case 'o' | 'Return' if len(node.children) > 0:
            path = node.children[selected]['path']
        case _:
            return
    
    if os.path.isdir(path):
        os.system(f'explorer "{path}"')
    elif os.path.isfile(path):
        path = path.replace("\\", "/")
        print(path)
        os.system(f'"{path}"')


def get_starting_directory() -> str:
    if len(sys.argv) == 1:
        tk.Tk().withdraw()
        return askdirectory().replace('/', '\\')
    else:
        return sys.argv[1]


if __name__ == '__main__':
    start_path = get_starting_directory()


    theme = DARK_THEME

    map = MindMap(
        get_tree_from_path(start_path),
        theme=theme,
        pr_style=ProgressStyle(theme, "sector"))
    map.set_key_command(handle_key)
    map.win.focus_force()
    map.start()