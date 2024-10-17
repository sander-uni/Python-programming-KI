import random
import math
import my_math_module


# Task 2.0
# Pretend the random numbers are scores from 2 groups of people
# This is a diving competition
# We want group 1 to win, so them winning is success
# If in a trial, they have the same score, they flip a coin
# Team 1 is a better team than team 2
# Total outcomes = 9*10=90
# 9 outcomes guaranteed win for team 1 (pairs with 1)
# 9 outcomes are same pairs, 50% dice roll
# Leaves 72 outcomes with success half the time
# 36 + 9*0.5 (dice roll) + 9 (2-10 pairs with 1) = 49.5 successes on average
# 49.5/90=55%
# Simulating 1,000,000 trials supports this math
def bernoulli_simulation(n: int = 10):
    group_1_scores = []
    group_2_scores = []
    for _ in range(0, n):
        group_1_scores.append(random.randint(2, 10))  # 2 - 10 score
        group_2_scores.append(random.randint(1, 10))  # 1 - 10 score

    success = 0
    failure = 0
    # P = 0.55
    # Q = 0.45
    for i in range(0, n):
        if group_1_scores[i] > group_2_scores[i]:
            success += 1
        elif group_1_scores[i] == group_2_scores[i]:
            if random.randint(0, 1) == 1:
                success += 1
            else:
                failure += 1
        else:
            failure += 1

    print(f"Successes: {success}, failures: {failure}")
    print(f"Success rate: {(success / n) * 100}%")


# Calculates the the expected value of a discrete random variable
def E(outcomes: list, p: float):
    return my_math_module.sigma(
            len(outcomes),
            lambda i: outcomes[i] * p
    )


# Calculate probability of x when it's uniformily distributed
def P(outcomes: list):
    return 1 / len(outcomes)


def get_standard_deviation(p: float, n: int):
    return math.sqrt(n * p * (1 - p))


def get_variance(p: float, n: int):
    return get_standard_deviation(p, n)**2


# Task 2.1
# 6-sided dice
# Mcnulty rolls the dice
# Success: roll 4-6 inclusive
# Failure: roll 1-3 inclusive
# Very explicit conditions for clarity
def dice_trial():
    roll = random.randint(1, 6)
    if roll >= 4 and roll <= 6:
        return 1  # Success
    elif roll >= 1 and roll <= 3:
        return 0  # Failure


# Task 2.2
# Generic bernoulli trial function
def bernoulli_trial(n: int, p: float):
    print("Theoretical values:")
    print(f"Expectation: {E([0, 1], p)}")
    print(f"Variance: {get_variance(p, n)}")
    print(f"Standard deviation: {get_standard_deviation(p, n)}")
    print("")

    success = 0
    p = int(p * 1_000_000_000)
    for _ in range(0, n):
        if random.randint(1, 1_000_000_000) <= p:
            success += 1

    print(f"Successes: {success}, failures: {n - success}")
    print(f"Success rate: {(success / n) * 100}%")
    return success


def get_probability_input():
    while True:
        user_input = input(
            "Input probability of success.\n"
            "The number must be between 0.0 & 1.0\n"
            ": "
        )
        try:
            user_input = float(user_input)
        except ValueError:
            print("Invalid value, try again.")
            continue

        if user_input < 0 or user_input > 1:
            print("The number must be between 0.0 and 1.0 inclusive.")
        else:
            return user_input


def get_trials_input():
    while True:
        user_input = input(
            "Input number of trials.\n"
            "The number must be an integer between 1 & 1,000,000\n"
            ": "
        )
        try:
            user_input = int(user_input)
        except ValueError:
            print("Invalid value, try again.")
            continue

        if user_input < 1 or user_input > 1_000_000:
            print("The integer must be between 1 and 1,000,000 inclusive.")
        else:
            return user_input
