import os
import shutil

import pandas as pd


def select_option(obj: [list, tuple, dict, pd.DataFrame], item_name='item', key=False, extra_options: dict = None):
    if not extra_options:
        extra_options = {}

    if isinstance(obj, pd.DataFrame):
        if obj.shape[0] == 1:
            return obj.index[0] if key else obj.iloc[0]
        if obj.shape[0] == 0:
            return False
        key = True
        df = obj.reset_index()
        df.index += 1
        print(df)

        n = obj.shape[0]
        items = {n_: df_ for n_, (_, df_) in enumerate(obj.iterrows())}
    else:
        if isinstance(obj, dict) and len(obj) == 1:
            return list(obj.keys())[0] if key else obj[list(obj.keys())[0]]
        elif len(obj) + len(extra_options) == 1:
            return obj[0]
        elif len(obj) == 0:
            return False

        items = {}
        for n, item in enumerate(obj):
            print(f"{n + 1}: {item}")
            items[n + 1] = item

    for option, result in extra_options.items():
        n += 1
        print(f"{n + 1}: {option}")
        items[n + 1] = result

    selection = 0
    while selection not in items:
        selection = int(input(f"Enter {item_name} number: "))

    if key or isinstance(obj, (list, tuple)):
        return items[selection]

    return obj[items[selection]]


def select_options(objs: [list, tuple, dict, pd.DataFrame], item_name='item', key=False, extra_options: dict = None):
    if not extra_options:
        extra_options = {}

    extra_options.update(Stop=False)

    if isinstance(objs, tuple):
        objs = list(objs)

    options = []

    while True:
        if objs:
            obj = select_option(objs, item_name, key=key, extra_options=extra_options)
            if not obj:
                break

            if isinstance(objs, dict):
                options.append(obj)
                objs.pop(obj)
            elif isinstance(objs, pd.DataFrame):
                options.append(obj)
                objs.drop(columns=obj, inplace=True)
            else:
                options.append(objs.pop(objs.index(obj)))

        else:
            break

    return options


def empty_directory(directory_path, excluded_entries: list = None, excluded_filetype: str = None):
    if not excluded_entries:
        excluded_entries = []
    # Check if the directory exists
    if not os.path.exists(directory_path):
        return False

    # List all files and subdirectories in the directory
    for entry in os.listdir(directory_path):
        entry_path = os.path.join(directory_path, entry)
        if any(list(filter(lambda file: os.path.splitext(file)[1] == excluded_filetype, filenames))
               for _, _, filenames in os.walk(entry_path, topdown=False)):
            continue

        excluded = filter(lambda excluded_entry: excluded_entry in entry, excluded_entries)
        if any(excluded) or (excluded_filetype and entry.endswith(excluded_filetype)):
            continue

        # Check if it's a file and remove it
        if os.path.isfile(entry_path):
            assert not entry_path.endswith(".py"), f"Trying to delete python (.py) files! ({entry_path})"
            os.remove(entry_path)

        # Check if it's a directory and remove it recursively
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)


def get_data_path(data_current_dir: str = None, file: str = None, exclude_list: list = None, file_format: str = ".csv",
                  known_entries: list = None):
    if not data_current_dir:
        data_current_dir = os.getcwd()
    elif not os.path.exists(data_current_dir):
        print(f"Warning: {data_current_dir} does not exist, using current working directory.")
        data_current_dir = os.getcwd()

    if not exclude_list:
        exclude_list = []

    if not known_entries:
        known_entries = []

    data_path = data_current_dir
    for dirpath, dirnames, filenames in os.walk(data_current_dir):
        # Interactively select which directory for the current household
        if dirpath == data_path:
            if dirnames:
                if options := [element for element in known_entries if element in dirnames]:
                    pass
                else:
                    options = list(filter(lambda dir_: dir_ not in exclude_list, dirnames))

                sub_dir = select_option(options, "directory")
                data_path = os.path.join(data_path, sub_dir)

            elif file:
                assert file in filenames, f"{file} is not in {dirpath}."
                return data_path, file
            else:
                files = sorted(filter(lambda file_: os.path.splitext(file_)[1] == file_format, filenames))
                file = select_option(files)
                return data_path, file

# def get_file_path(current_dir: str = None, file_exts: list = None, extra_options: dict = None,
#                   exclude_list: list = None, dir_only: bool = False):
#     if not current_dir:
#         current_dir = os.getcwd()
#
#     if not exclude_list:
#         exclude_list = []
#
#     if not file_exts:
#         file_exts = [".csv"]
#
#     while True:
#         options = [option for option in os.listdir(current_dir) if (os.path.splitext(option)[1] in file_exts
#                    and option not in exclude_list) or os.path.isdir(os.path.join(current_dir, option))]
#         sub_dir = select_option(options, extra_options=extra_options)
#         if not sub_dir or os.path.isfile(os.path.join(current_dir, sub_dir)):
#             if dir_only:
#                 return current_dir
#
#             return current_dir, sub_dir
#
#         current_dir = os.path.join(current_dir, sub_dir)
