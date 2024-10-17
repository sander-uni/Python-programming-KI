# The parse function satisfied the conditions of task 1.2.
# It's a somewhat strict parser, that accepts nothing but
# whitespace and numbers.
# It does not care about how many or what whitespace
# characters between the numbers.
# Additionally, the generator function writes
# Randomized data in human readable format,
# That the parser function can read.
# Check tests.py for functionality tests

import random
import os
import re
import numpy as np
from enum import Enum


class BYTES(Enum):
    ZERO = 48
    NINE = 57
    MINUS = 45
    DOT = 46
    NEWLINE = 10


__whitespace_bytes = (9, 10, 32, 13, 12, 11)


def __isspace(byte):
    return byte in __whitespace_bytes


def __make_data_folder():
    if not os.path.exists("Data"):
        current_folder = os.getcwd()
        try:
            os.mkdir("Data")
        except PermissionError:
            print(f"Missing permissions to create folder at {current_folder}.")
            return False
        except FileNotFoundError:
            print(f"Failed to create folder at {current_folder}.")
            return False

    return True


# Based on norway age demographics
# Distributes age data roughly in line with real demographics
# The average age is typically within 10% of the real demographics
def population_age_randomizer():
    if random.randint(0, 9) == 9:
        # 10% chance of being 70 and older
        # Old people range is 70-130

        end_range = 60  # Oldest recorded human was 122 years old
        current_probability = 65 * 10**6  # 65000000 / 1000000 == 65%
        for age_offset in range(0, end_range + 5, 5):
            if (  # The older the age group is, the more likely to choose it
                random.randint(1, 10**8) <= current_probability
                or age_offset == end_range
            ):
                current_probability += (
                    (10**8 - current_probability)
                    * (0.15 + 0.02 * age_offset)
                ) // 1

                if age_offset == end_range:
                    range_start = 70
                    range_end = range_start + (age_offset - 5) // 2
                    return random.randint(range_start, range_end)
                else:
                    range_start = 70 + age_offset
                    range_end = range_start + 5
                    return random.randint(range_start, range_end)

    else:
        # The remaining age groups were mostly evenly distributed
        # So they're indiscriminately distributed for simplicity's sake
        return random.randint(0, 69)


# Writes a dataset following the assignment's restrictions
# In human readable format
# Takes a randomizer function as argument
def generate(
    datapoint_count: int,
    data_per_line: int = 5,
    random_func=lambda: random.randint(-100, 100),
    file_name: str = "My data"
):
    if datapoint_count > 10**5:
        print("Cancelled data generation.")
        print("You can't generate more than 100,000 numbers.")
        return

    if not __make_data_folder():
        print("Cancelled data generation.")
        print("Failed to make data folder.")
        return

    file_name = re.sub(r"\.\w+$", "", file_name)
    # Remove file extension
    # Allows with and without it

    try:
        with open(f"Data/{file_name}.txt", "w+", encoding="utf-8") as file:
            file.write(f"dataset size: {datapoint_count}\n")
            for i in range(1, datapoint_count + 1):
                datapoint = random_func()

                string = f"{datapoint}"
                string = string + (" " * (10 - len(string)))
                file.write(string)
                if i % data_per_line == 0:
                    file.write("\n")

            file.flush()
            file.close()
    except FileNotFoundError:
        print("Failed to create the data file.")
        print("No data was generated.")
        return


def __print_parse_failed(file_name: str, msg: str, print_msg: bool = True):
    print(f"Cancelled parsing the file \"{file_name}.txt\".")
    if print_msg:
        print(msg)


def __print_parse_error_traceback(
    file_name: str,
    msg: str,
    str_pos: int,
    line: int
):
    __print_parse_failed(file_name, None, print_msg=False)
    print(f"{msg} at file pos {str_pos}, line {line}.")


def parse(file_name: str):
    assert isinstance(file_name, str), (
        "Tried to pass a non-string value as file name."
    )
    file_name = re.sub(r"\.\w+$", "", file_name)
    # Remove file extension
    # Allows with and without it

    if not __make_data_folder():
        __print_parse_failed(
            file_name,
            "Failed to make data folder."
        )
        return np.empty(0, dtype=float)
    if not os.path.exists(f"Data/{file_name}.txt"):
        __print_parse_failed(
            file_name,
            f"The file \"{file_name}.txt\" doesn't exist."
        )
        return np.empty(0, dtype=float)

    dataset_size = None

    try:
        with open(f"Data/{file_name}.txt", "rb") as file:
            file_bytes = file.read()
            line = 1
            start_of_number = 0
            is_in_number = False
            is_fraction = False

            match = re.match(rb"\s*dataset size:\s*(\d+)", file_bytes)
            try:
                dataset_size = int(match.group(1))
            except ValueError:
                __print_parse_failed(
                    file_name,
                    "Missing dataset size property."
                )
                return np.empty(0, dtype=float)

            data = np.empty(dataset_size, dtype=float)
            data_i = 0

            for str_pos in range(match.end(), len(file_bytes)):
                byte = file_bytes[str_pos]
                if byte >= BYTES.ZERO.value and byte <= BYTES.NINE.value:
                    if not is_in_number:
                        is_in_number = True
                        start_of_number = str_pos
                elif byte == BYTES.DOT.value:  # is a "." character
                    if is_fraction or not is_in_number:
                        __print_parse_error_traceback(
                            file_name,
                            "Invalid dot character",
                            str_pos,
                            line
                        )
                        return np.empty(0, dtype=float)

                    is_fraction = True
                elif byte == BYTES.MINUS.value:  # is a "-" character
                    if is_in_number:
                        __print_parse_error_traceback(
                            file_name,
                            "Invalid minus character",
                            str_pos,
                            line
                        )
                        return np.empty(0, dtype=float)

                    is_in_number = True
                    start_of_number = str_pos
                elif __isspace(byte):  # is whitespace
                    if byte == BYTES.NEWLINE.value:
                        line += 1
                    if is_in_number:
                        datapoint = file_bytes[start_of_number:str_pos + 1]
                        try:
                            datapoint = float(datapoint)
                        except ValueError:
                            __print_parse_error_traceback(
                                file_name,
                                f"Invalid number ({datapoint})",
                                str_pos,
                                line
                            )
                            return np.empty(0, dtype=float)
                        data[data_i] = datapoint
                        data_i += 1
                        is_in_number = False
                        is_fraction = False
                else:  # is anything else
                    __print_parse_error_traceback(
                        file_name,
                        f"Illegal char (byte: '{byte}', char: '{chr(byte)}')",
                        str_pos,
                        line
                    )
                    return np.empty(0, dtype=float)
    except FileNotFoundError:
        __print_parse_failed(
            file_name,
            "Failed to open the data file."
        )
        return np.empty(0, dtype=float)

    if dataset_size != len(data):
        __print_parse_failed(
            file_name,
            "Dataset size property doesn't match size of the set.\n"
            + f"Expected {dataset_size}, got {len(data)}."
        )
        return np.empty(0, dtype=float)

    return data
