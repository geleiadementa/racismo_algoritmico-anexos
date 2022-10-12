import os
import json
import numpy as np
import pandas as pd
from deepface import DeepFace
from typing import Union

samples = os.environ.get('dataset_sample')
raw_images = os.environ.get('raw_images')
resultados = os.environ.get('dataset_resultado')
output = os.environ.get('output_deepface')


def add_item(col: str, item: Union[str, float, int], repo: dict):
    if col in repo.keys():
        repo[col].append(item)
    else:
        repo[col] = [item]


def make_columns(js: dict) -> dict:
    new_columns = {}

    for instance in js.keys():
        for category in js[instance].keys():
            if type(js[instance][category]) is dict:
                add_item(
                    f'var_{category}',
                    np.var(list(js[instance][category].values()), ddof=1),
                    new_columns
                )
                for subcategory in js[instance][category]:
                    act_key = f'{category}-{subcategory}'
                    add_item(
                        act_key,
                        js[instance][category][subcategory],
                        new_columns
                    )
            else:
                add_item(
                    category,
                    js[instance][category],
                    new_columns
                )

    return new_columns


if __name__ == '__main__':

    df = pd.read_csv(samples, delimiter='\t')
    paths = [os.path.join(raw_images, i) for i in df.filepath.to_list()]

    out = DeepFace.analyze(
        img_path=paths,
        detector_backend='mtcnn',
        enforce_detection=False,
        prog_bar=False
    )

    with open(output, 'w') as f:
        print('salvando a saída do deepface:', end=' ')
        f.write(
            json.dumps(out, indent=2)
        )
        print('ok')

    new_columns = make_columns(out)

    for col in new_columns.keys():
        df[col] = new_columns[col]

    df.to_csv(resultados, sep='\t', index=False)
