import os
import pandas as pd

def load_dataset(base_path="data/ToS"):
    sentences_path = os.path.join(base_path, "Sentences")
    labels_path = os.path.join(base_path, "Labels")

    data = []
    #each files corresponds to a dataset company - we have 50 companies - 
    for file in os.listdir(sentences_path):
        company = file.replace(".txt", "")
    #load sentences (one clause per line)
        with open(os.path.join(sentences_path, file)) as f: 
            sentences = f.read().splitlines()
    #load lables (1 and -1) aligned with sentences by index
        with open(os.path.join(labels_path, file)) as f:
            labels = [int(x) for x in f.read().splitlines()]
    #
        for i, sentence in enumerate(sentences): 
            data.append({
                "company": company,
                "sentence": sentence,
                "label": labels[i]
            })

    return pd.DataFrame(data) #TODO: sanity check!

#dataset will be used downstream for embedding generation next step!