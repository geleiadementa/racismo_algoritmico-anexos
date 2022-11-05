import pandas as pd
from os import getenv

dataset_base_path = getenv('dataset_base')
n_samples = int(getenv('n_amostras'))
seed = int(getenv('seed'))
dataset_sample = getenv('dataset_sample')

(
    pd.read_csv(dataset_base_path, delimiter="\t")
    .groupby(['ethnicity', 'gender'])
    .sample(n_samples, random_state=seed)
    .to_csv(dataset_sample, sep="\t", index=False)
)
