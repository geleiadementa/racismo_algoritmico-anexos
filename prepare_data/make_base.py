import csv
import re
import xmltodict
from os import getenv
from tqdm import tqdm
from glob import glob

labels_file = getenv("labels")
identity_meta = getenv("identity_meta")
raw_images_path = getenv("raw_images")
dataset_output = getenv("dataset_base")

regex = re.compile(r"(n\d{6})")

# according to VMER_dataset/README.txt
labels_names = {
    '1': 'African American',
    '2': 'East Asian',
    '3': 'Caucasian Latin',
    '4': 'Asian Indian'
}


def make_index_dict(content: iter, id_col: str, target: str) -> dict:
    _t = {}
    for i in content:
        _t[i[id_col]] = i[target]

    return _t


if __name__ == "__main__":

    pbar = tqdm(total=3, unit='step', desc='read data...')
    with open(labels_file) as f0:
        labels = xmltodict.parse(f0.read())["xml"]["subject"]
        id2ethnicity = make_index_dict(labels, "id", "ethnicity")
        pbar.update(1)

    with open(identity_meta, newline="") as f1:
        identity_dict = list(csv.DictReader(f1, skipinitialspace=True))
        id2identity = make_index_dict(identity_dict, "Class_ID", "Gender")
        id2identity['n001710'] = "m"
        pbar.update(1)
        id2name = make_index_dict(identity_dict, "Class_ID", "Name")
        pbar.update(1)
        del identity_dict

    files = glob(raw_images_path + "/*/*.jpg")

    with open(dataset_output, "w", newline="") as f:
        dataset_writer = csv.writer(f, delimiter="\t")
        # write header
        dataset_writer.writerow([
            "id", "name", "filepath", "ethnicity", "ethnicity_name", "gender"
        ])

        for filepath in tqdm(
            files, ncols=80, unit="files", mininterval=0.5,
            desc='make base dataset'
        ):
            match = regex.search(filepath)
            _id = match.group()
            ethnicity = id2ethnicity[_id]
            ethnicity_name = labels_names[ethnicity]
            gender = id2identity[_id]
            name = id2name[_id]

            dataset_writer.writerow([
                _id, name, filepath, ethnicity, ethnicity_name, gender
            ])
