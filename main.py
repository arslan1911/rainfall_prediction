from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import pandas as pd
import os
import uvicorn
import pickle
import sys
# Get the root directory and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

load_dotenv()
app = FastAPI()

class ModelInputData(BaseModel):
    TempHighF: float
    TempAvgF : float
    TempLowF : float
    DewPointHighF : float
    DewPointAvgF : float
    DewPointLowF : float
    HumidityHighPercent : float
    HumidityAvgPercent : float
    HumidityLowPercent : float
    SeaLevelPressureAvgInches : float
    VisibilityHighMiles : float
    VisibilityAvgMiles : float
    VisibilityLowMiles : float
    WindHighMPH : float
    WindAvgMPH : float
    WindGustMPH : float

# Load the saved model
# Get the absolute path of the current script's directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the 'model.pkl' file
model_path = os.path.join(current_directory, 'saved_models', 'model.pkl')

print(model_path)
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Define test fastapi

@app.get("/test")
def test():
    return {"message": "This is a test endpoint."}

# Define the data endpoint    

# # Define the prediction endpoint
@app.post("/predict_rainfall")
def predict_rainfall(input_data: ModelInputData):
    try:
        input_df = pd.DataFrame([input_data.dict().values()], columns=input_data.dict().keys())
        prediction = model.predict(input_df)
        return {"prediction": prediction.tolist()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
