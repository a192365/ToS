import pickle

class ClauseClassifier:

    def __init__(self, model_path="models/classifier.pkl"): #load trained classifier trained on sentence embeddings
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, vector):

        prediction = self.model.predict([vector])[0] #model also expects input as 2d array
        prob = self.model.predict_proba([vector])[0][1] #of class 1 (unfair) - clausula abusiva

        return {
            "label": int(prediction),
            "probability": float(prob) #here higher probability mean higher likelihood of being unfair
        }
    
    ##classifier outputs both label and probability for interpretability!!