import pickle
import pandas as pd

class Predictor:
    def __init__(self):
        self.predictor_model = pickle.load(open("prediction_system/prediction_model/logreg_model.pkl", "rb"))
        self.predictor_tranformer = pickle.load(open("prediction_system/prediction_model/logreg_transform.pkl", "rb"))

    def predict(self, sentiment: str) -> str:
        
        final_input = self.predictor_tranformer.transform(pd.Series(sentiment))
        output = self.predictor_model.predict(final_input)

        return "Rating for the review out of 5 is : " + str(output[0])
    
predictor = Predictor()