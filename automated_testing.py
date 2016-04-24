import os
import string
import train
import sample
import find_in_file
import time
import tensorflow as tf
import random as r


class TrainingParameters:
    def __init__(self,
                 rnn_size=128,
                 layers=2,
                 model='lstm',
                 batch_size=50,
                 seq_length=50,
                 epochs=50,
                 save_every=100,
                 grad_clip=5.,
                 learning_rate=0.002,
                 decay_rate=.97):
        self.rnn_size = rnn_size
        self.num_layers = layers
        self.model = model
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.num_epochs = epochs
        self.save_every = save_every
        self.grad_clip = grad_clip
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate

    def get_training_arguments(self, data_dir, save_dir):
        return TrainArguments(data_dir, save_dir,
                              self.rnn_size,
                              self.num_layers,
                              self.model,
                              self.batch_size,
                              self.seq_length,
                              self.num_epochs,
                              self.save_every,
                              self.grad_clip,
                              self.learning_rate,
                              self.decay_rate)


# Model for training data, holds parameters
class TrainArguments(TrainingParameters):
    def __init__(self, data_dir, save_dir,
                 rnn_size=128,
                 layers=2,
                 model='lstm',
                 batch_size=50,
                 seq_length=50,
                 epochs=50,
                 save_every=100,
                 grad_clip=5.,
                 learning_rate=0.002,
                 decay_rate=0.97):
        TrainingParameters.__init__(self, rnn_size, layers, model, batch_size, seq_length, epochs, save_every,
                                    grad_clip,
                                    learning_rate, decay_rate)
        self.data_dir = data_dir
        self.save_dir = save_dir

    def get_sample_model(self, n=500, prime='a'):
        return SampleArguments(self.save_dir, n, prime)


# Model for test data
class SampleArguments:
    def __init__(self, save_dir, n=500, prime='a'):
        self.save_dir = save_dir
        self.n = n
        self.prime = prime


models_dir = "models"
output_dir = "outputs"
test_dir = "tests"
dataset_dir = "datasets"
time_format = "D%Y-%m-%dT%H-%M-%S"
sample_size = 5000


def get_target_passwords(target_file):
    return find_in_file.load_set(target_file)


def run_automated_testing(train_options, datasets, target_file):
    # Some presets
    print("Loading target passwords.")
    target_passwords = get_target_passwords(target_file)
    print("Loaded %d target passwords." % len(target_passwords))

    with open("run_log.log", 'a') as log_file:
        for dataset in datasets:
            for train_params in train_options:
                model_name = train_dataset(dataset, train_params)
                ls = set(string.letters.lower())
                for prime in ''.join(r.sample(ls, len(ls)))[0:3]:
                    run_test_preloaded(dataset, model_name, prime, target_passwords)


def train_dataset(dataset, train_params):
    temp_dataset_dir = dataset_dir
    data_dir = os.path.join(temp_dataset_dir, dataset)
    print("Data Directory: %s" % data_dir)
    # Model name (layers_size_model_time)
    model_name = "%d_%d_%s" % (train_params.num_layers,
                               train_params.rnn_size,
                               train_params.model)
    model_dir = os.path.join(data_dir, models_dir, model_name)
    print("Model Dir: %s" % model_dir)
    train_args = train_params.get_training_arguments(data_dir, model_dir)
    tf.reset_default_graph()
    train.train(train_args)

    return model_name


def run_test(dataset, model_name, prime, target_file, size=5000):
    target_passwords = find_in_file.load_set(target_file)
    print("Loaded %d target passwords." % len(target_passwords))
    run_test_preloaded(dataset, model_name, prime, target_passwords, size)


def run_test_preloaded(dataset, model_name, prime, target_passwords, size=5000):
    output_file = create_sample(dataset, model_name, prime, size)
    passes, percent, shared_passes = find_in_file.find_common_preload(output_file, target_passwords)
    passes_from_orig, percent_orig, shared_passes_to_orig = find_in_file.find_common(output_file,
                                                                                     "%s/input.txt" % os.path.join(
                                                                                         dataset_dir, dataset))
    test_output = os.path.join(dataset_dir, dataset, test_dir, "%s_%s_%d_test.txt" % (model_name, prime, size))
    with open(test_output, "w") as out:
        output = "Passes from Original List %d - Shared Passwords: %d - Percentage of Generated: %f\n" % (
                passes_from_orig, passes, percent)
        out.write(output)
        print("[%s] %s" % (model_name, output))
        out.write("Passwords:\n")
        out.write('\n'.join(shared_passes) + "\n")


def create_sample(dataset, model_name, prime, size=5000):
    output_name = "%s_%s_%d.txt" % (model_name, prime, size)
    output_file = os.path.join(dataset_dir, dataset, output_dir, output_name)
    model_file = os.path.join(dataset_dir, dataset, models_dir, model_name)
    sample_args = SampleArguments(model_file, size, prime)
    with open(output_file, "w") as out:
        tf.reset_default_graph()
        out.write(sample.sample(sample_args))
    return output_file
