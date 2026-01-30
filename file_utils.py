import glob
import os
import json
import re
import shutil
from typing import List
from loguru import logger
from pathlib import Path


def write_json_file(data, file_path):
    """Write data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def write_jsonl_file(data, file_path, mode='w'):
    """
    Write data to a JSON lines file. Each line in the file contains one JSON object.
    :param data: List of dictionaries or objects that can be serialized to JSON
    :param file_path: String denoting the path to the output file
    """
    with open(file_path, mode=mode, encoding="utf-8") as f:
        for item in data:
            json_str = json.dumps(item, ensure_ascii=False) if type(item) is not str else item
            f.write(json_str + "\n")


def read_json_file_union(file_path: str):
    if file_path.endswith(".json") is True:
        return read_json_file(file_path)
    elif file_path.endswith(".jsonl") is True:
        return read_jsonl_file(file_path)
    else:
        raise ValueError(f"后缀错误: {file_path}")


def read_json_file(file_path: str):
    """
    Read a JSON file and return the content as a JSON object (dictionary or list).
    :param file_path: String denoting the path to the JSON file
    :return: JSON object (typically a dictionary or a list)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_jsonl_file(file_path: str):
    """
    Read a JSONL file and return a list of Python dictionaries.
    :param file_path: String denoting the path to the JSONL file
    :return: List of dictionaries parsed from JSON lines in the file
    """
    # Prepare an empty list to hold the JSON objects
    data = []
    if os.path.exists(file_path) is False:
        return data
    # Open the file and read line by line
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Each line is a complete JSON object
            json_obj = json.loads(line.strip())
            # Add the parsed JSON object to the list
            data.append(json_obj)
    # Return the list of JSON objects
    return data


def read_fuzzy_jsonl_file(file_pattern: str):
    """
    Read all JSONL files that match the given file pattern and return a combined list of Python dictionaries.
    :param file_pattern: String denoting the pattern to match JSONL files
    :return: List of dictionaries parsed from JSON lines in matched files
    """
    # Prepare an empty list to hold all JSON objects from multiple files
    all_data = []
    # Use glob to find all files matching the pattern
    matched_files = glob.glob(file_pattern)
    # Iterate over each matched file
    for file_path in matched_files:
        # For each file, read the JSONL contents
        data = read_jsonl_file(file_path)
        # Extend the all_data list with the data from this file
        all_data.extend(data)
    # Return the combined list of JSON objects
    return all_data


def read_jsonl_file_to_dict(file_path, dict_key):
    """
    Read a JSONL file and return a dictionary of Python dictionaries.
    :param file_path: String denoting the path to the JSONL file
    :param dict_key: The key in each dictionary (from each JSON line) to use as the key in the resulting dictionary.
    :return: Dictionary of dictionaries parsed from JSON lines in the file, keyed by dict_key
    """
    # Prepare an empty dictionary to hold the JSON objects
    data = {}
    if not os.path.exists(file_path):
        return data
    # Open the file and read line by line
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            # Each line is a complete JSON object
            json_obj = json.loads(line.strip())
            # Check if dict_key exists in the current json_obj
            if dict_key in json_obj:
                # Use the value of dict_key as the key in 'data' dictionary
                key_value = json_obj[dict_key]
                # Add the parsed JSON object to the dictionary
                data[key_value] = json_obj
            else:
                continue
    # Return the dictionary of JSON objects
    return data


def read_text_file(file_path) -> List[str]:
    result_list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip("\n\r")
            if line != "":
                result_list.append(line)
    return result_list


def read_text_split_file(file_path, sep="\t"):
    result_list = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip("\n\r")
            if line != "":
                result_list.append(line.split(sep))
    return result_list


def scan_dir(directory=".", suffix=None):
    """
    Scan a directory and return a list of file paths with the given suffix.
    :param directory: String denoting the directory to scan
    :param suffix: List of strings denoting the file suffixes to match
    :return: List of file paths with the given suffix
    """
    # Ensure suffix is a list
    if suffix is None:
        suffix = []
    elif isinstance(suffix, str):
        suffix = [suffix]
    # Prepare an empty list to hold the file paths
    file_list = []
    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if len(suffix) > 0:
                # Check if the file ends with any of the provided suffixes
                if any(file.endswith(s) for s in suffix):
                    # Construct the full file path and add it to the list
                    file_list.append(os.path.join(root, file))
            else:
                # Construct the full file path and add it to the list
                file_list.append(os.path.join(root, file))
    # Return the list of file paths
    return file_list


def scan_files(directory, file_format, naming_pattern):
    """
    扫描指定文件夹内符合特定命名规则和文件格式的文件。

    :param directory: 要扫描的文件夹路径
    :param file_format: 文件的格式，如 'jsonl'
    :param naming_pattern: 文件命名规则，如 'abc_*' 或 '*'
    :return: 符合条件的文件列表
    """
    # 构建文件名匹配模式
    if naming_pattern == '*':
        # 匹配所有以指定格式结尾的文件
        full_pattern = f".*\.{file_format}$"
    else:
        # 替换命名规则中的 '*' 以构建正则表达式
        pattern = naming_pattern.replace('*', '.*')
        full_pattern = f"{pattern}\.{file_format}$"

    # 遍历目录中的所有文件
    matched_files = []
    for filename in os.listdir(directory):
        if re.match(full_pattern, filename):
            matched_files.append(filename)

    return matched_files


def find_files_with_pattern(directory, pattern):
    """
    Scan a specified directory for files that match the given regular expression pattern.
    Returns a list of matching file names.

    Args:
    directory (str): The directory to scan.
    pattern (str): The regular expression pattern to match the file names.

    Returns:
    list[str]: A list of file names that match the pattern.
    """
    matched_files = []
    # Ensure the directory exists before attempting to list its contents
    if not os.path.exists(directory):
        logger.warning("The specified directory does not exist.")
        return matched_files

    # List and match files in the specified directory
    for file in os.listdir(directory):
        if re.match(pattern, file):
            matched_files.append(file)
    return matched_files


def trans_json_to_jsonl(json_file_path, jsonl_file_path):
    """
    Transform a JSON file into a JSON lines file.
    :param json_file_path: String denoting the path to the input JSON file
    :param jsonl_file_path: String denoting the path to the output JSON lines file
    """
    # Read the JSON file
    data = read_json_file(json_file_path)
    # Write the JSON lines file
    write_jsonl_file(data, jsonl_file_path)


def check_dir(directory_path):
    """确保文件路径中的最后一级目录存在，如果不存在，则递归创建这个目录。"""
    # 如果目录路径不是空的，并且这个目录不存在，那么创建它
    if directory_path and not os.path.exists(directory_path):
        try:
            os.makedirs(directory_path)
            logger.info(f"Directory created: {directory_path}")
        except OSError as e:
            logger.error(f"Failed to create directory {directory_path}: {e}")


def is_directory_empty(directory):
    """检查给定的目录是否为空"""
    # 使用os.listdir获取目录中所有文件和子目录的列表
    if os.path.exists(directory) and os.path.isdir(directory):
        return not os.listdir(directory)
    else:
        return False  # 目录不存在，或路径不是一个目录


def init_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    touch_file(file_path)


def touch_file(file_path):
    """创建一个空文件"""
    file_path_obj = Path(file_path)
    file_path_obj.touch()


def delete_files(target_dir, target_file_name):
    for dirpath, dirnames, filenames in os.walk(target_dir):
        for file in filenames:
            if file == target_file_name:
                full_path = os.path.join(dirpath, file)
                os.remove(full_path)


def check_output_path(output_path):
    # 检查并创建目录
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # 检查文件是否存在， 如果存在则删除文件
    if os.path.exists(output_path) is True:
        os.remove(output_path)
    # 创建一个新的空文件
    with open(output_path, "x") as file:
        pass


def split_dataframe_by_rows(df, rows_per_file, output_prefix):
    """  
    将 DataFrame 按行数分割成多个 CSV 文件  
    参数:  
    df: pandas DataFrame 对象  
    rows_per_file: 每个文件的行数  
    output_prefix: 输出文件名前缀  
    """
    total_rows = len(df)
    num_files = (total_rows // rows_per_file) + (1 if total_rows % rows_per_file > 0 else 0)
    for i in range(num_files):
        start_row = i * rows_per_file
        end_row = min((i + 1) * rows_per_file, total_rows)
        # 创建文件名，例如 output_prefix_001.csv
        file_name = f"{output_prefix}_{i+1:03d}.tsv"
        # 保存切片的 DataFrame
        df.iloc[start_row:end_row].to_csv(file_name, index=False, sep="\t")
        print(f"已保存 {file_name}, 行 {start_row+1}-{end_row}")
