import imageio
import numpy as np
import pandas as pd
from os import environ
from tqdm import tqdm
from pathlib import Path
from matplotlib import pyplot as plt

csv = environ.get('dataset_resultado')
output_dir = environ.get('output_dir')


def make_figure() -> (plt.Figure, dict):
    axes = {}

    fig = plt.figure(figsize=(8, 12))
    gs = fig.add_gridspec(nrows=5, ncols=2)

    axes['image'] = fig.add_subplot(gs[:2, :])
    axes['table'] = fig.add_subplot(gs[2, :])
    axes['race'] = fig.add_subplot(gs[3:, 0], projection='polar')
    axes['emotion'] = fig.add_subplot(gs[3:, 1], projection='polar')

    return fig, axes


def plot_polar(ax: plt.Axes, row: pd.Series, name: str):

    row_item = row.filter(like=name + '-').astype(np.float64)
    ax.stem(
        row_item.index.map(
            lambda x: x.replace(name + '-', '').replace(' ', '\n')
        ),
        row_item.values
    )


if __name__ == '__main__':

    table_labels = ['age', 'gender', 'dominant_race', 'dominant_emotion']
    df = pd.read_csv(csv, sep='\t')
    n = len(df)

    for i in tqdm(range(n)):
        row = df.iloc[i]
        fig, ax = make_figure()

        img = imageio.v3.imread(row['filepath'])

        ax['image'].imshow(img)

        table_row = row[table_labels]
        ax['table'].axis('off')
        ax['table'].set_title('Deepface results:', y=0.8)
        ax['table'].table(
            cellText=table_row.values.reshape(-1, 1),
            rowLabels=table_row.index,
            cellLoc='center',
            loc='center',
            cellColours=[['#1f1f1f']] * len(table_labels),
            rowColours=['#1f1f1f'] * len(table_labels),
            bbox=[0.52, 0.2, 0.2, 0.6],
            edges='B'
        )

        ax['race'].set_title('\"race\" prediction:', y=1.2)
        plot_polar(
            ax['race'], row, 'race'
        )
        ax['race'].set_ylim((0, 100))

        ax['emotion'].set_title('emotion prediction:', y=1.2)
        plot_polar(
            ax['emotion'], row, 'emotion'
        )
        ax['emotion'].set_ylim((0, 100))

        _id = row.id
        stem = Path(row.filepath).stem

        fig.suptitle(f'{_id} - {stem}')
        fig.savefig(Path(output_dir).joinpath('images', f'{_id}-{stem}.png'))
        plt.close(fig)
