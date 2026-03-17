import faiss
import pickle
import numpy as np

class SearchEngine:

    def __init__(self, index_path="models/faiss.index", metadata_path="models/metadata.pkl"): ## load pre-built FAISS index (built during indexing step)
        self.index = faiss.read_index(index_path)

        with open(metadata_path, "rb") as f:
            self.metadata = pickle.load(f)

    def search(self, vector, top_k=5):

        vector = np.array([vector]).astype("float32") #faiss expect inputs as 2d - float32 array

        distances, indices = self.index.search(vector, top_k) #returns distances and indices of nearest vectors, for similarity search

        results = []

        for score, idx in zip(distances[0], indices[0]):
            meta = self.metadata[idx]

            results.append({
                "sentence": meta["sentence"],
                "company": meta["company"],
                "label": meta["label"], 
                "score": float(score) #more_similar (L2 distance) - lower distances indicates higher similarity!
            })

        return results #top_k most similar clauses to the qeuyry
    
    ## metadata keeps original sentence + company + label
    ## index search is done in vector space using sentence embeddingss