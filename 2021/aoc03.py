from copy import deepcopy

with open("input/input03.txt") as f:
    content = f.read().splitlines()

diagnostic_numbers = []
for line in content:
    diagnostic_number = []
    for bit in line:
        diagnostic_number.append(int(bit))
    diagnostic_numbers.append(diagnostic_number)

num_bits = len(diagnostic_numbers[0])


def count_bins(bin_lists, bin):
    return len([bin_list[i] for bin_list in bin_lists if bin_list[i] == bin])


def bin_to_int(bin_list):
    return int(''.join([str(b) for b in bin_list]), 2)


gamma_rate_bin = []
epsilon_rate_bin = []
for i in range(0, num_bits):
    num_0 = count_bins(diagnostic_numbers, 0)
    num_1 = count_bins(diagnostic_numbers, 1)
    gamma_rate_bin.append(1 if num_1 > num_0 else 0)
    epsilon_rate_bin.append(1 if num_1 < num_0 else 0)

gamma_rate = bin_to_int(gamma_rate_bin)
epsilon_rate = bin_to_int(epsilon_rate_bin)

print("Solution 1: the product of the gamma rate by the epsilon rate is {}".format(gamma_rate * epsilon_rate))

oxygen_generator_rating_bin = None
carbon_dioxide_scrubber_rating_bin = None

reduced_diagnostic_numbers1 = deepcopy(diagnostic_numbers)
reduced_diagnostic_numbers2 = deepcopy(diagnostic_numbers)
for i in range(0, num_bits):
    if not oxygen_generator_rating_bin:
        num_0 = count_bins(reduced_diagnostic_numbers1, 0)
        num_1 = count_bins(reduced_diagnostic_numbers1, 1)
        most_common = 1 if num_1 >= num_0 else 0
        reduced_diagnostic_numbers1 = [diagnostic_number for diagnostic_number in reduced_diagnostic_numbers1
                                       if diagnostic_number[i] == most_common]
        if len(reduced_diagnostic_numbers1) == 1:
            oxygen_generator_rating_bin = reduced_diagnostic_numbers1[0]

    if not carbon_dioxide_scrubber_rating_bin:
        num_0 = count_bins(reduced_diagnostic_numbers2, 0)
        num_1 = count_bins(reduced_diagnostic_numbers2, 1)
        least_common = 1 if num_1 < num_0 else 0
        reduced_diagnostic_numbers2 = [diagnostic_number for diagnostic_number in reduced_diagnostic_numbers2
                                       if diagnostic_number[i] == least_common]
        if len(reduced_diagnostic_numbers2) == 1:
            carbon_dioxide_scrubber_rating_bin = reduced_diagnostic_numbers2[0]

oxygen_generator_rating = bin_to_int(oxygen_generator_rating_bin)
carbon_dioxide_scrubber_rating = bin_to_int(carbon_dioxide_scrubber_rating_bin)

print("Solution 2: the product of the oxygen generator rating by the CO2 scrubber rating is {}"
      .format(oxygen_generator_rating * carbon_dioxide_scrubber_rating))
