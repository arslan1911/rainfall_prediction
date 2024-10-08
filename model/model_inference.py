import pickle
import os
from dotenv import load_dotenv
import sys



# Load environment variables from.env file
load_dotenv()
 
# load the model
def load_model(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    return model

# function to predict rainfall

def predict_rainfall(model, X):
    return model.predict(X)

if __name__ == "__main__":
 
    # Load model
    model_path = os.getenv("TRAINED_MODEL")
    model = load_model(model_path)
    
    # Required columns
    required_columns = ['TempHighF', 'TempAvgF', 'TempLowF', 'DewPointHighF', 'DewPointAvgF',
       'DewPointLowF', 'HumidityHighPercent', 'HumidityAvgPercent',
       'HumidityLowPercent', 'SeaLevelPressureAvgInches',
       'VisibilityHighMiles', 'VisibilityAvgMiles', 'VisibilityLowMiles',
       'WindHighMPH', 'WindAvgMPH', 'WindGustMPH']
    # Predict rainfall
    
    # rainfall_prediction = predict_rainfall(model, X)
    # print(f"Predicted rainfall: {rainfall_prediction[0]} inches")

    # Get the root directory and add it to sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    #  Get the first row of the test data from the dataprocessing file 
    from data.data_preprocessing import split_data, load_data, preprocess_data
    import sys
    from dotenv import load_dotenv
    import os
    load_dotenv()
    

    file_path = os.getenv("DATA_PATH")
    data = load_data(file_path)
    data = preprocess_data(data)
    X_test, _, _, y_test = split_data(data)
    # print(X_test.iloc[1])
    print(f"Predicted: {model.predict([X_test.iloc[3]])}, Actual: {y_test.iloc[3]}")
