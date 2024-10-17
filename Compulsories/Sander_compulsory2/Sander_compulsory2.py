# There's a file for each task
# Execute this current file to access user interface
# to run every task
# They prove my functions and programs work

# Below are pointers to the source for each task
# Task 1.1 in "my_math_module.py"
# Task 1.2 in "data.py"
# Task 1.3 in "Sander_compulsory2_Task_1_3.py"

# Task 2.0 in "bernoulli_trial.py"
# Task 2.1 in "bernoulli_trial.py"
# Task 2.2 in "bernoulli_trial.py"
# Task 2.3 in "Sander_compulsory2_Task_2_3.py"

# Very overkill, but I learned a lot and enjoyed the process
# I've provided a requirements file
# Only external requirement is numpy
# I used Python 3.12 64 bit
# Written in vs2022

import subprocess


TASK_DESCRIPTIONS = [
    "Write Python functions to calculate the theoretical values for mean\n"
    "(expectation), variance, and standard deviation for a sample. that\n"
    "means s and not σ.",

    "Write a Python function that reads a text file containing numerical\n"
    "data (which we will later analyze) and stores the data in a list.\n"
    "The file format should be as follows:\n"
    "1. The first line contains the total number of numbers (a\n"
    "positive integer).\n"
    "2. The subsequent lines contain the numbers, separated by spaces\n"
    "or newlines.\n"
    "For example, a file with 5 numbers could look like:\n"
    "Handle any potential errors gracefully, such as if the first line is\n"
    "not a valid integer or if the number of values does not match the\n"
    "number stated.",

    "Write a program that reads sample data from a file and computes a\n"
    "95% confidence interval for the population mean μ.\n"
    "Note: Ensure that the sample size is sufficiently large or that the\n"
    "data is normally distributed to satisfy the assumptions for the\n"
    "confidence interval. Your program should output the lower and upper\n"
    "bounds of the confidence interval and explain what the interval\n"
    "means in the context of the sample.",

    "Write a Python function that simulates a Bernoulli trial using\n"
    "Python's random number generator.",

    "Use the random number generator function in Python to implement a\n"
    "function which generates the individual outcomes according to the\n"
    "problem stated.",

    "Implement a function that, given n (the number of trials) and p =\n"
    "P(S) (the probability of success for each trial), returns the total\n"
    "number of successes in n trials. You can use the function from 2.1\n"
    "to generate individual outcomes for each trial.",

    "Write a program that:\n"
    "1. Prompts the user to input the probability p = P(S) and the\n"
    "number of trials n.\n"
    "2. output the theoretical values for expectation and standard\n"
    "deviation,\n"
    "3. simulate repeated Bernoulli trials for different values n\n"
    "(number of trials, for example 30 and 100).\n"
    "\n"
    "In the Python file, include the following as comments:\n"
    "• Describe the context of your Bernoulli trial (e.g., what does\n"
    "success (S) and failure (F) represent in your scenario?).\n"
    "• State the problem clearly, specifying what the trial is\n"
    "simulating. What do success and failure represent in your\n"
    "problem? What is the probability of success p=P(S)?"
]


def get_task_num_input(input_display: str):
    while True:
        user_input = input(input_display)
        try:
            user_input = int(user_input)
        except ValueError:
            print("Invalid value, try again.")
            continue

        if user_input < 1 or user_input > 8:
            print("The integer must be between 1 and 8 inclusive.")
        else:
            return user_input


if __name__ == "__main__":
    input_str = []
    task_file_names = []
    for i1 in range(1, 3):
        for i2 in range(0, 4):
            input_str.append(f"\"{(i1 - 1) * 4 + i2}\" to run task {i1}.{i2}")
            task_file_names.append(f"Sander_compulsory2_Task_{i1}_{i2}.py")

    del input_str[0]  # There is no task 1.0
    del task_file_names[0]  # There is no task 1.0

    input_str.append("\"8\" exit.")
    input_str.append(": ")
    input_str = "\n".join(input_str)

    is_running = True
    while is_running:
        user_input = get_task_num_input(input_str)
        for i in range(1, 9):
            if user_input == 8:
                print("Goodbye")
                is_running = False
                break
            else:
                print(task_file_names[user_input - 1])
                print(TASK_DESCRIPTIONS[user_input - 1])
                print("="*30)
                subprocess.run(
                    ["python", task_file_names[user_input - 1]],
                    check=True
                )
                print("="*30)
                print("")
                break
