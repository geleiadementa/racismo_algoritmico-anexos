import csv
import re
import xmltodict
from os import getenv
from tqdm import tqdm
from glob import glob

labels_file = getenv('labels')
raw_images_path = getenv('raw_images')
dataset_output = getenv('dataset_base')

regex = re.compile(r"(n\d{6})")

if __name__ == '__main__':

    with open(labels_file) as f:
        labels = xmltodict.parse(f.read())['xml']['subject']

    _id2ethnicity = {}

    for i in labels:
        _id2ethnicity[i['id']] = i['ethnicity']

    files = glob(raw_images_path + "/*/*.jpg")

    with open(dataset_output, 'w', newline='') as f:
        dataset_writer = csv.writer(
            f, delimiter='\t'
        )
        # write header
        dataset_writer.writerow(['id', 'filepath', 'ethnicity'])

        for filepath in tqdm(files, ncols=80, unit='files', mininterval=0.5):
            match = regex.search(filepath)
            _id = match.group()
            ethnicity = _id2ethnicity[_id]

            dataset_writer.writerow([_id, filepath, ethnicity])
