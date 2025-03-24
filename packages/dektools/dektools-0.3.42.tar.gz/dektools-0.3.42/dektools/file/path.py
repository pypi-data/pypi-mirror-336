import os
import uuid
import shutil
from pathlib import Path


def join_path(*args):
    return os.path.normpath(os.path.join(*(args[0], *(x.strip('\\/') for x in args[1:]))))


def normal_path(path, unix=False):
    path = os.path.normpath(os.path.abspath(os.path.expanduser(os.fspath(path))))
    if unix and os.name == 'nt':
        path = path.replace('\\', '/')
    return path


def new_empty_path(*paths):
    while True:
        np = f"{os.path.join(*paths)}.{uuid.uuid4().hex}"
        if not os.path.exists(np):
            return np


def split_ext(path):
    file, ext = os.path.splitext(path)
    if not ext and file.startswith('.'):
        return '', file
    return file, ext


def path_ext(path):
    return split_ext(path)[-1]


def multi_ext(path, limit=None, case=False):
    filename = os.path.basename(path)
    result = []
    while True:
        index = filename.rfind('.')
        if index != -1:
            ext = filename[index:]
            if case is None:
                pass
            elif case:
                ext = ext.upper()
            else:
                ext = ext.lower()
            result.insert(0, ext)
            filename = filename[:index]
            if limit is not None and len(result) >= limit:
                break
        else:
            break
    return filename, result


def list_env_paths():
    return os.environ['PATH'].split(os.pathsep)


def iter_exe_paths(path=None):
    if os.name == 'nt':
        if not path:
            path = os.getcwd()
        yield path
    yield from list_env_paths()


def which(x, path=None):
    return shutil.which(x, path=path)


def which_list(x):
    result = []
    for path in iter_exe_paths():
        p = which(x, path)
        if p:
            result.append(p)
    return result


def where(x, path=None):
    if path:
        paths = [path]
    else:
        paths = iter(iter_exe_paths())
    for p in paths:
        fp = os.path.join(p, x)
        if os.path.exists(fp):
            return fp
    return None


def where_list(x):
    result = []
    for path in iter_exe_paths():
        p = where(x, path)
        if p:
            result.append(p)
    return result


def tree(root=None, depth=None):
    # prefix components:
    space = '    '
    branch = '│   '
    # pointers:
    tee = '├── '
    last = '└── '

    def _tree(dir_path: Path, prefix, dir_depth):
        if depth is not None and dir_depth > depth:
            return
        contents = sorted(dir_path.iterdir(), key=lambda item: 1 if os.path.isfile(dir_path / item) else 0)
        # contents each get pointers that are ├── with a final └── :
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            yield prefix + pointer + path.name
            if path.is_dir():  # extend the prefix and recurse:
                extension = branch if pointer == tee else space
                # i.e. space because last, └── , above so no more |
                yield from _tree(path, prefix + extension, dir_depth + 1)

    for line in _tree(Path(root or os.getcwd()), '', 0):
        print(line, flush=True)
