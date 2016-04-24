import csv
import concurrent.futures
from itertools import product

# Create a list of common replacements
common_replacements = {}
with open('data/small_common_replacements.txt', 'r', encoding='utf8') as file:
    reader = csv.reader(file)
    for row in reader:
        common_replacements[row[0]] = row[1:len(row)]


# Can permute passwords
def permute(word, from_char, to_char):
    options = [(c,) if c != from_char else (from_char, to_char) for c in word]
    return (''.join(o) for o in product(*options))


# Generates permutations for a password
def permutePassword(password, depth=1):
    if depth < 0:
        return list()  # base case for recursion
    new_passwords = set()
    new_passwords.add(password)
    for letter in set(password):  # Try to replace each letter
        replacements = common_replacements.get(letter.capitalize(), list())
        # print(", ".join(replacements))
        for r in replacements:  # Using each replacement
            for first_permute in list(permute(password, letter, r)):  # Create a set of permutations
                new_passwords.add(first_permute)
                for recurse_permute in permutePassword(first_permute, depth=depth - 1):  # Create recursive permutations
                    new_passwords.add(recurse_permute)
    return list(new_passwords)


# Generate the passwords
password_list = 'password_lists/10k_most_common.txt'
passwords = set()
with open(password_list, "r", errors='ignore') as f:
    myList = [word.strip() for word in f]
    print("Read File with %d passwords" % len(myList))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results_to_seed = {executor.submit(permutePassword, seed, 2): seed for seed in myList}
        completed = 0
        for future in concurrent.futures.as_completed(results_to_seed):
            result = future.result()
            completed += 1
            print("Added %d passwords from seed %s: %d" % (len(result), results_to_seed[future], completed))
            for res in future.result():
                passwords.add(res)


with open("input.txt", "w") as outfile:
    outfile.write('\n'.join(passwords))
