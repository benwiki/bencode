import os


def getSubFolders(folder: str) -> list[str]:
    return next(os.walk(folder))[1]


def startsWithAny(text: str, startsWith: str | list[str]):
    for startSeq in startsWith:
        if text.startswith(startSeq):
            return True
    return False


def explorePath(path: str, folder: str = '.') -> dict:
    res: dict[str, dict] = {}
    for folder in getSubFolders(path):
        if startsWithAny(folder, ['.', '_']) or folder in ['code']:
            continue
        elif startsWithAny(folder, ['android', 'build', 'source', 'admob',
                                    'ios', 'linux', 'windows', 'macos',
                                    'EmilyDragon1', 'EmilyDragon2', 'EmilyDragon3', 'Offline']):
            res[folder] = {}
            continue
        res[folder] = explorePath(f'{path}/{folder}', folder)
    return res


def treeify(graph: dict[str, dict], last: list[bool] | None = None) -> str:
    if last is None:
        last = []
    dirLen = len(graph)
    res = ''
    for i, dir in enumerate(graph):
        res += ''.join('    ' if L else '|   ' for L in last)
        res += '└───' if i == dirLen - 1 else '├───'
        res += f'{dir}\n'
        res += treeify(graph[dir], last + [i == dirLen - 1])
    return res


open('folder_tree.txt', 'w', encoding='utf-8').write(treeify(explorePath('.')))
