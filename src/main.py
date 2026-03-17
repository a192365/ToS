from fastapi import FastAPI
from src.schemas import SearchRequest, ClassifyRequest
from src.embedder import Embedder
from src.search_engine import SearchEngine
from src.classifier import ClauseClassifier

app = FastAPI()

embedder = Embedder() #initialize components, this also avoid reloading models on every request
search_engine = SearchEngine()
classifier = ClauseClassifier()

@app.get("/health") #is the API running? 
def health():
    return {"status": "ok"}

@app.post("/search")
def search(req: SearchRequest):

    vector = embedder.encode([req.query])[0] #user query is converted into embedding vector
    results = search_engine.search(vector, req.top_k) #most similar clauses are retrieved from index

    return {"results": results}

@app.post("/classify")
def classify(req: ClassifyRequest):

    vector = embedder.encode([req.text])[0] #encode input clause into embedding space
    result = classifier.predict(vector) #predict fair/nott fair (1 or -1) using the trained classifierr

    return result


## Flow: 
# query → embedding → search
# text → embedding → classifier
# and API layer connects embedding, retrieval and classification components!