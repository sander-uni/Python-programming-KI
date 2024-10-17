import my_math_module
import data

# Create the data of size 5000, stored in new file called "Task 1.3 data.txt"
# inside the data folder
# The data is randomized ages from the norwegian population
# It tries to generates age distribution close to reality, within 10%
data.generate(
    5000,
    file_name="Task 1.3 data",
    random_func=data.population_age_randomizer
)

# Parse the newly generated data
population_data = data.parse("Task 1.3 data")

# Create dataset object to perform the data analysis with its various methods
dataset = my_math_module.Dataset(population_data)

# Create sample of size 200
# The sample has no duplicate values
# The sampling is random since there are no other properties in the data
sample = my_math_module.Sample(dataset.data, 200)

# Get dictionary containing lower and upper bound of 95% confidence interval
confidence_interval = sample.get_confidence_interval(0.95)

# The interval
# Intervals aligns with:
# https://www.calculator.net/confidence-interval-calculator.html
print(f"Dataset size: {dataset.size}")
print(f"Sample size: {sample.size}")
print(f"Lower bound: {confidence_interval["lower bound"]}")
print(f"Upper bound: {confidence_interval["upper bound"]}")
print(
    "The lower bound to upper bound range is very likely to contain "
    + "the real mean of the entire dataset.\n"
    + "If we continue to sample more data, "
    + "the real population age mean is more and more apparent."
)
print(f"Real mean for the dataset: {dataset.get_mean()}")
