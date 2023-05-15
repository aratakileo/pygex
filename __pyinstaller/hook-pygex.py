import os
import pathlib


# Get data folder
pygex_folder = os.path.dirname(pathlib.Path(__file__).parent.absolute())

# datas is the variable that pyinstaller looks for while processing hooks
datas = []


def _append_to_pygex(file_path):
    res_path = os.path.join(pygex_folder, file_path)
    if os.path.exists(res_path):
        datas.append((res_path, "pygex"))


_append_to_pygex('broker.pyi')
