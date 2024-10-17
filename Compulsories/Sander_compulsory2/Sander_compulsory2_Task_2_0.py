import bernoulli_trial

# Simulates 1000 trials of a bernoulli trial
print(
    "Pretend the random numbers are scores from 2 groups of people\n"
    "This is a diving competition\n"
    "We want group 1 to win, so them winning is success\n"
    "If in a trial, they have the same score, they flip a coin\n"
    "Team 1 is a better team than team 2\n"
    "Total outcomes = 9*10=90\n"
    "\n"
    "9 outcomes guaranteed win for team 1 (pairs with 1)\n"
    "9 outcomes are same pairs, 50% dice roll\n"
    "Leaves 72 outcomes with success half the time\n"
    "36 + 9*0.5(dice roll) + 9(2-10 pairs with 1) = 49.5 successes / 90\n"
    "49.5/90=55%\n"
    "Simulating 1,000,000 trials supports this math"
)

print("10,000 trials")
bernoulli_trial.bernoulli_simulation(n=10_000)
