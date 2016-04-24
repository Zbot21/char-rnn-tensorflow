import os
import automated_testing
from automated_testing import TrainingParameters

b_size = 300

datasets = ("Rock_You_75",)
target_file = os.path.join("datasets", "target_data", "crackstation-human-only.txt")

save_every = 10000

# Different various training options
train_options = (
    TrainingParameters(layers=3, rnn_size=500, batch_size=b_size, save_every=500),
)

automated_testing.run_automated_testing(train_options, datasets, target_file)

