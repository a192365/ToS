import pickle
from sklearn.linear_model import LogisticRegression

from src.loader import load_dataset
from src.embedder import Embedder

df = load_dataset()

embedder = Embedder()

X = embedder.encode(df["sentence"].tolist())
y = df["label"].values

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

with open("models/classifier.pkl", "wb") as f:
    pickle.dump(model, f)

print("Classifier trained")