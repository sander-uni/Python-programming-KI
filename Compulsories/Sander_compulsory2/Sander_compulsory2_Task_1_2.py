import data
import tests
import time

# File located in < same folder as this python file >/Data
data.generate(
    50_000,
    random_func=data.population_age_randomizer,
    file_name="Population age"
)
data = data.parse("Population age")

# Shows it's stored in a numpy.ndarray
print(data)

print("Population age data")

print("")
print("Running tests. This may take up to 30 seconds...")
print("")

print("Test 1: number with 2 dots in it.")
try:
    tests.test_malformed_number_in_data_1()
except Exception as error:
    print(f"Test failed with error: {error}")
else:
    print("Test ran as expected!")


print("")
time.sleep(4)
print("Test 2: number with minus in the wrong place.")
try:
    tests.test_malformed_number_in_data_2()
except Exception as error:
    print(f"Test failed with error: {error}")
else:
    print("Test ran as expected!")


print("")
time.sleep(4)
print("Test 3: Illegal char in data.")
try:
    tests.test_illegal_char_in_data()
except Exception as error:
    print(f"Test failed with error: {error}")
else:
    print("Test ran as expected!")


print("")
time.sleep(4)
print("Performance test: 1mb file of random data")
tests.test_parse_performance()
