from sentence_transformers import SentenceTransformer

class Embedder:

    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2") 
#accept string and list of strings - returning embeddings as numpy array
    def encode(self, texts): 
        return self.model.encode(texts) 
    

## from here, embeddings will be used both for search (FAISS) and classification.