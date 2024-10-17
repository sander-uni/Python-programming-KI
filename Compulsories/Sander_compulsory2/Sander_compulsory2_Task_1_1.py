import my_math_module
import data

data.generate(
    50_000,
    random_func=data.population_age_randomizer,
    file_name="Population age"
)
population_age_data = data.parse("Population age")

dataset = my_math_module.Dataset(population_age_data)

sample = my_math_module.Sample(population_age_data, 200)

print(f"Sample size: {sample.size}")
print(f"Size of dataset: {dataset.size}")
print(f"Variance: {sample.get_variance()}")
print(f"Standard deviation: {sample.get_standard_deviation()}")
print(f"Mean: {sample.get_mean()}")
