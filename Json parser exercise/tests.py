import re
import os
import time
from pathlib import Path
import json_parser as json

def __get_file_string(filepath):
    with open(filepath, 'r') as file:
        return file.read()

def __for_loop_for_recursive_list(table, stack):
    for key in range(0, len(table)):
        value = table[key]
        if isinstance(key, str):
            key = key.replace("\\", "\\\\").replace("\"", "\\\"")
            if not key[0].isalpha() and key[0] != '_':  # enclose empty or advanced strings
                key = f"[{key}]"
        elif not isinstance(key, (int, float)):
            key = f"[\"{str(key)}\"]"
        else:
            key = f"[{str(key)}]"
        
        if isinstance(value, dict) and id(value) not in stack['tracker']:
            stack['file'].write(f"{'	' * stack['depth']}{key} = {{\n")
            stack['tracker'][id(value)] = True
            stack['depth'] += 1
            write_table_recursively_to_file(value, stack)
            stack['depth'] -= 1
            stack['file'].write(f"{'	' * stack['depth']}}},\n")

        else:
            if isinstance(value, str):
                value = value.replace("\\", "\\\\").replace("\"", "\\\"")
                if "\r" in value or "\n" in value:
                    if "]]" in value:
                        value = value.replace("]]", "] ]")
                    value = re.sub(r'([^\r\n]+)', ' ' * (stack['depth'] + 1) + r'\1', value)
                    value = f"[[\n{value}\n{'	' * stack['depth']}]]"
                else:
                    value = f"\"{value}\""
            elif not isinstance(value, (int, float)):
                value = f"\"{str(value)}\""
            stack['file'].write(f"{'	' * stack['depth']}{key} = {value},\n")

def __for_loop_for_recursive_dict(table, stack):
    for key, value in table.items():
        if isinstance(key, str):
            key = key.replace("\\", "\\\\").replace("\"", "\\\"")
            if not key[0].isalpha() and key[0] != '_':  # enclose empty or advanced strings
                key = f"[{key}]"
        elif not isinstance(key, (int, float)):
            key = f"[\"{str(key)}\"]"
        else:
            key = f"[{str(key)}]"
        
        if isinstance(value, dict) and id(value) not in stack['tracker']:
            stack['file'].write(f"{'	' * stack['depth']}{key} = {{\n")
            stack['tracker'][id(value)] = True
            stack['depth'] += 1
            write_table_recursively_to_file(value, stack)
            stack['depth'] -= 1
            stack['file'].write(f"{'	' * stack['depth']}}},\n")

        else:
            if isinstance(value, str):
                value = value.replace("\\", "\\\\").replace("\"", "\\\"")
                if "\r" in value or "\n" in value:
                    if "]]" in value:
                        value = value.replace("]]", "] ]")
                    value = re.sub(r'([^\r\n]+)', ' ' * (stack['depth'] + 1) + r'\1', value)
                    value = f"[[\n{value}\n{'	' * stack['depth']}]]"
                else:
                    value = f"\"{value}\""
            elif not isinstance(value, (int, float)):
                value = f"\"{str(value)}\""
            stack['file'].write(f"{'	' * stack['depth']}{key} = {value},\n")

def write_table_recursively_to_file(table, stack=None):
    file_path = "Json data.txt"
    if stack is None:
        stack = {
            'tracker': {},
            'depth': 0,
            'file': open(file_path, "w+")
        }
    if stack['depth'] == 0:
        stack['file'].write("{\n")
    
    if isinstance(table, list):
        __for_loop_for_recursive_list(table, stack)
    elif isinstance(table, dict):
        __for_loop_for_recursive_dict(table, stack)
    if stack['depth'] == 0:
        stack['file'].write("}\n")
        stack['file'].flush()
        stack['file'].close()
        return __get_file_string(file_path)


def test_json_performance():
    start_time = time.perf_counter()

    file_path = Path("Natives.json")
    json_data = json.decode(file_path)

    print(f"{(time.perf_counter() - start_time) * 1000} ms")
    write_table_recursively_to_file(json_data)

    print("Python data structure printed to \"Json data.txt\".")