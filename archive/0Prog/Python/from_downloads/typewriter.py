"""
A tiny help tool for saving snippets.
"""

import os
import tkinter as tk
import customtkinter as ctk

root = ctk.CTk()


def copy_to_clipboard(entry: tk.Entry):
    root.lower()
    root.clipboard_clear()
    root.clipboard_append(entry.get())


def save_content(i, j, type):
    def save_inner(content) -> bool:
        with open(STOREFILE, 'r') as f:
            tw_store: dict = eval(f.read())
            tw_store[(i, j)] = tw_store.get((i, j), {})
            tw_store[(i, j)][type] = content
        with open(STOREFILE, 'w') as f:
            f.write(str(tw_store))
        return True
    return save_inner


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
STOREFILE = f'{CURRENT_PATH}/typewriter_store.txt'

if not os.path.exists(STOREFILE):
    with open(STOREFILE, 'w') as f:
        f.write(r'{}')
with open(STOREFILE, 'r') as f:
    store: dict[tuple[int, int], dict[str, str]] = eval(f.read())

row, col = 12, 8
entry_str: list[list[tk.StringVar]] = []
content_entries: list[list[tk.Entry]] = []
name_entries: list[list[tk.Entry]] = []
buttons: list[list[ctk.CTkButton]] = []

for i in range(row):
    entry_str.append([])
    content_entries.append([])
    name_entries.append([])
    buttons.append([])
    for j in range(col):
        entry_str[i].append(tk.StringVar())

        content_entries[i].append(tk.Entry(
            root, width=30, validate='key',
            validatecommand=(root.register(
                save_content(i, j, 'content')), '%P'),
            fg='white', bg='black'))
        content_entries[i][j].grid(row=i*3, column=j)

        if ((record := store.get((i, j), '')) and
           (content := record.get('content', ''))):  # type: ignore
            content_entries[i][j].insert(0, content)

        name_entries[i].append(tk.Entry(
            root, width=30, validate='key',
            validatecommand=(root.register(
                save_content(i, j, 'name')), '%P'),
            textvariable=entry_str[i][j],
            fg='white', bg='black'))
        name_entries[i][j].grid(row=i*3+1, column=j)

        if ((record := store.get((i, j), '')) and
           (name := record.get('name', ''))):  # type: ignore
            name_entries[i][j].insert(0, name)

        buttons[i].append(ctk.CTkButton(
            root, width=30, height=3,
            textvariable=entry_str[i][j],
            corner_radius=50, hover_color="red",
            command=lambda entry=content_entries[i][j]:
                copy_to_clipboard(entry)))
        buttons[i][j].grid(row=i*3+2, column=j)

root.mainloop()
