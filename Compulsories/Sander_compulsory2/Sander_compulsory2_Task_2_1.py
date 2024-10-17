import bernoulli_trial

outcomes = {
    0: "Failure",
    1: "Success"
}

print("Success: dice rolls 4-6 inclusive")
print("Failure: dice rolls 1-3 inclusive")
for i in range(0, 10):
    print(f"Outcome: {outcomes[bernoulli_trial.dice_trial()]}")
