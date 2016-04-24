__author__ = 'chris'
import os
import automated_testing
import random as r
import string
import tensorflow as tf

dataset = "Rock_You_75"
model = "3_400_lstm"
num_primes = 5
target_file = os.path.join("datasets", "target_data", "crackstation-human-only.txt")
print("Preloading Passwords")
target_passwords = automated_testing.get_target_passwords(target_file)
print("Done Preloading Passwords")
size = 100000

ls = set(string.letters.lower())
for prime in ''.join(r.sample(ls, len(ls)))[0:num_primes]:
    print("Running test with prime %s" % prime)
    automated_testing.run_test_preloaded(dataset, model, prime, target_passwords, size)
    print("Done running test with prime %s" % prime)

