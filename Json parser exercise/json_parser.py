#  Based on previous json parsers i've written in other languages
#  Magnitudes slower than Python's json module (~24x slower)
#  Written as a learning and optimization exercise
#  Traverses file by by byte
#  8000 ms to decode 2.6mb file
#  Lua version I made of this some months ago, decodes the same file in 150ms

import re
from pathlib import Path
from unicodedata import east_asian_width


def process_non_str_value(value, current_node, key_and_value, str_pos):
    key = None
    if isinstance(current_node, list):
        current_node.append(None)
        key = len(current_node) - 1
    else:
        key = key_and_value[0]
        del key_and_value[0]

    assert key not in current_node, (
        f"Duplicate keys are not allowed. char pos {str_pos}, key: \"{key}\""
    )
    if value == b"true":
        current_node[key] = True
        return
    elif value == b"false":
        current_node[key] = False
        return
    elif value == b"null":
        current_node[key] = "null"
        return

    try:
        num = float(value)
        if num:
            current_node[key] = num
    except ValueError:
        raise ValueError(f"Invalid non-str value: {value}")

escape_sequences = {
    "\\b": "\b",
    "\\f": "\f",
    "\\n": "\n",
    "\\r": "\r",
    "\\t": "\t",
    "\\\"": "\"",
    "\\\\": "\\"
}

def process_escapes(match):
    return escape_sequences[match.group()]

def decode(file_path: Path):
    assert isinstance(file_path, Path), (
        "The \"file_path\" parameter takes only arguments of type \"Path\"."    
    )
    assert file_path.exists(), (
        "Tried to parse a file that doesn't exist."    
    )
    assert file_path.suffix == ".json", (
        "Tried to parse a non-json file."    
    )


    json_bytes = None
    json_bytes_len = None

    try:
        with file_path.open("rb") as file:
            json_bytes = file.read()
            json_bytes_len = len(json_bytes)
            file.close()
    except FileNotFoundError:
        print("Failed to open file for unknown reason.")
        return
    except PermissionError:
        print("Insufficient permissions to open this file.")
        return

    is_in_string = False
    is_escaped = False
    there_was_an_escape = False
    start_of_string = 0
    str_pos = 0
    byte_skips = 0
    key_and_value = [] #  Index 0 is the key, index 1 is the value
    current_node = []
    tree = [current_node]

    for str_pos in range(0, json_bytes_len):
        if byte_skips > 0:
            byte_skips -= 1
            continue

        byte = json_bytes[str_pos]
        if byte == 34 and not is_escaped: #  If byte is ", handle string
            if is_in_string:
                key_and_value.append(json_bytes[start_of_string + 1:str_pos].decode("utf-8"))
                if isinstance(current_node, list):
                    value = key_and_value[0]
                    if there_was_an_escape:
                        value = re.sub(
	                        r"\\[bfnrt\"\\]",
                            process_escapes,
	                        value
                        )

                    del key_and_value[0]
                    current_node.append(value)
                elif len(key_and_value) == 2:
                    key = key_and_value[0]
                    assert key not in current_node, (
                        f"Duplicate keys are not allowed. char pos {str_pos}, key: \"{key}\""    
                    )
                    current_node[key] = key_and_value[1]
                    if there_was_an_escape:      
                        current_node[key] = re.sub(
	                        r"\\[bfnrt\"\\]",
                            process_escapes,
	                        current_node[key]
                        )

                    del key_and_value[1]
                    del key_and_value[0]

                is_in_string = False
                there_was_an_escape = False
            else:
                is_in_string = True
                start_of_string = str_pos

        elif is_in_string: #  Continue to iterate through the string
            if byte == 92 and not is_escaped: #  If byte is \, handle escape sequences
                is_escaped = True
                there_was_an_escape = True
                continue #  is_escaped is set to False at the end, so continue

        elif byte == 123: #  If byte is {, Start new object node
            if isinstance(current_node, list):
                current_node.append({})
                current_node = current_node[len(current_node) - 1]
            else:
                key = key_and_value[0]
                del key_and_value[0]
                assert key not in current_node, (
                    f"Duplicate keys are not allowed. char pos {str_pos}, key: \"{key}\""    
                )
                current_node[key] = {}
                current_node = current_node[key]
            tree.append(current_node)

        elif byte == 125: #  If byte is }, End object node
            del tree[len(tree) - 1]
            current_node = tree[len(tree) - 1]

        elif byte == 91: #  If byte is [, Start new array node
            if isinstance(current_node, list):
                current_node.append([])
                current_node = current_node[len(current_node) - 1]
            else:
                key = key_and_value[0]
                del key_and_value[0]
                assert key not in current_node, (
                    f"Duplicate keys are not allowed. char pos {str_pos}, key: \"{key}\""    
                )
                current_node[key] = []
                current_node = current_node[key]
            tree.append(current_node)

        elif byte == 93: #  If byte = ], End array node
            del tree[len(tree) - 1]
            current_node = tree[len(tree) - 1]

        elif byte > 44 and byte != 58:
        #  If byte is not a comma, not a colon or whitespace
		#  Process null / num / bool value

            pattern = re.compile(b"(true|false|null|[-.\d]+)")
            #  intentionally not strict on numbers so process function can raise error

            match = pattern.match(json_bytes, pos=str_pos, endpos=json_bytes_len - 1)
            assert match is not None, (
                "Invalid value ("
                + f"{json_bytes[str_pos:min(json_bytes_len, str_pos + 10)]})"
                + f"at pos {str_pos}"    
            )

            process_non_str_value(match.group(), current_node, key_and_value, str_pos)
            byte_skips = match.end() - str_pos

        is_escaped = False

    return current_node
