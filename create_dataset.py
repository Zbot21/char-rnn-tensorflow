import os
__author__ = 'chris'

dataset_dir = "datasets"
model_dir = "models"
out_dir = "outputs"
tests_dir = "tests"

name = "Research"

os.makedirs(os.path.join(dataset_dir, name, model_dir))
os.makedirs(os.path.join(dataset_dir, name, out_dir))
os.makedirs(os.path.join(dataset_dir, name, tests_dir))
