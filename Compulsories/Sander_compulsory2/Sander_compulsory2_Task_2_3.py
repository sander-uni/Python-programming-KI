import bernoulli_trial


print(
    "Bernoulli trial 1: Coin flip\n"
    "Probability of success is 50%\n"
    "Success: Heads\n"
    "Failure: Tails\n"
    "30 trials\n"
)
bernoulli_trial.bernoulli_trial(30, 0.5)
print("")
print("")

print(
    "Bernoulli trial 2: Lottery\n"
    "Probability of success is 1 in 100 million\n"
    "Success: Win $100 million usd\n"
    "Failure: Win nothing, lose money paying for ticket\n"
    "10 million trials\n"
)
bernoulli_trial.bernoulli_trial(10_000_000, 0.000_000_01)
print("")
print("")

# Lets user simulate as many bernoulli trials they want
# User can choose how many trials and probability
# User can do as many simulations they want until they decide to exit
print("")
print("Now you can simulate any bernoulli trial you wish.")
print("")
while True:
    n = bernoulli_trial.get_trials_input()  # Get number of trials
    p = bernoulli_trial.get_probability_input()  # Get probability as a float
    print("")
    print("")
    bernoulli_trial.bernoulli_trial(n, p)
    print("")
    print("")
    user_input = input("Type \"y\" to continue or anything else to stop: ")
    if user_input != "Y" and user_input != "y":
        break
