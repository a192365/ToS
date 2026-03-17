import os
import pickle
import faiss
import numpy as np

from src.loader import load_dataset
from src.embedder import Embedder

df = load_dataset()

embedder = Embedder()

embeddings = embedder.encode(df["sentence"].tolist())

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))

os.makedirs("models", exist_ok=True)

faiss.write_index(index, "models/faiss.index")

metadata = df.to_dict("records")

with open("models/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("Index built successfully")