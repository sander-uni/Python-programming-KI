import time
import data


# Catch number with 2 dots in it
# Expectation: return empty list and give helpful feedback to fix it
def test_malformed_number_in_data_1():
    data.parse("Malformed number test data 1")


# Catch number with a minus in wrong place
# Also tests that it can work with file extension in the name, it should.
# Expectation: return empty list and give helpful feedback to fix it
def test_malformed_number_in_data_2():
    data.parse("Malformed number test data 2.txt")


# Catch illegal character
# Expectation: return empty list and give helpful feedback to fix it
def test_illegal_char_in_data():
    data.parse("Malformed number test data 3")


# 100,000 datapoints
# 1 run took 9300 ms
def test_parse_performance():
    start_time = time.perf_counter()
    data.parse("Performance test")
    print(f"Time to parse: {(time.perf_counter() - start_time) * 1000} ms")
