from pathlib import Path
import json
import tomllib
from .filesession import FileSession, FSession


def read_json(path: Path) -> dict | list:
    with open(path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    return data


def read_toml(path: Path) -> dict:
    with open(path, 'r', encoding="utf-8") as f:
        data = tomllib.loads(f.read())
    return data


def write_json(path: Path, data: dict | list | str, fs: FSession = None) -> None:

    def f(fs_: FSession):
        if isinstance(data, list | dict):
            with fs_.open(path, 'w', encoding="utf-8") as f:
                # noinspection PyTypeChecker
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif isinstance(data, str):
            with fs_.open(path, 'w', encoding="utf-8") as f:
                # noinspection PyTypeChecker
                json.dump(json.loads(data), f, indent=4, ensure_ascii=False)
        else:
            raise TypeError(f"Unsupported type {type(data)}")

    if fs is None:
        with FileSession() as fs:
            f(fs)
            fs.commit()
    else:
        f(fs)