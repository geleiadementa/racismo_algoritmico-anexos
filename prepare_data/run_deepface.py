import os
import json
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

    new_columns = {}

    for instance in out.keys():
        for category in out[instance].keys():
            if type(out[instance][category]) is dict:
                for subcategory in out[instance][category]:
                    act_key = f'{category}-{subcategory}'
                    add_item(
                        act_key,
                        out[instance][category][subcategory],
                        new_columns
                    )
            else:
                add_item(
                    category,
                    out[instance][category],
                    new_columns
                )

    for col in new_columns.keys():
        df[col] = new_columns[col]

    df.to_csv(resultados, sep='\t', index=False)
