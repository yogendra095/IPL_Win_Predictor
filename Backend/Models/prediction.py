import numpy as np
import pandas as pd
import pickle


with open("Models/model.pkl",'rb') as f:
    model=pickle.load(f)

categories=['Bowling_win',"Batting_win"]

def predict(user:dict):

    df=pd.DataFrame([user])
    df.rename(columns={'target':'total_runs_x'},inplace=True)
    probabilities=model.predict_proba(df)[0]
    combined=dict(zip(categories,map(lambda p: np.round(p,2),probabilities)))
    return combined
