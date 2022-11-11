import polars as pl
from os import getenv

dataset_base_path = getenv("dataset_base")
n_samples = int(getenv("n_amostras"))
n_imgs = int(getenv("n_imgs"))
seed = int(getenv("seed"))
dataset_sample = getenv("dataset_sample")

df = pl.read_csv(dataset_base_path, sep="\t")

ids = (
    df.groupby(["ethnicity", "gender"])
    .agg([pl.col("id").unique().shuffle(seed=seed).head(n=n_samples)])
    .explode(pl.col("id"))["id"]
)

mask = pl.all().exclude("id")

(
    df.filter(pl.col("id").is_in(ids))
    .groupby(pl.col("id"))
    .agg(mask.shuffle(seed=seed).head(n=n_imgs))
    .explode(mask)
    .write_csv(dataset_sample, sep="\t")
)
