from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schemas.validation import Input
from Models.prediction import predict
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

app.add_middleware(CORSMiddleware,
                     allow_origins=["*"],
                     allow_credentials=True,
                    allow_methods=["*"],   
                    allow_headers=["*"])

@app.get('/')
def about():
    return {"message":"This is an API for IPL win probability prediction"}

@app.get('/health')
def health_check():
    return {
        "Status":"OK"
    }

@app.post('/predict')
def userInput(user:Input):
    user_dict=user.model_dump(include=['batting_team','bowling_team','city','runs_left','ball_left','wicket_left','target','crr','rrr'])
    try:
        probab=predict(user_dict)
        return JSONResponse(status_code=200,content=probab)
    except Exception as e:
        return JSONResponse(status_code=500,content={"message":str(e)})
    
