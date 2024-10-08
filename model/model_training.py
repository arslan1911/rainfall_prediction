from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error,r2_score
from dotenv import load_dotenv
import pickle
import os
import numpy as np
import sys
# Get the root directory and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data.data_preprocessing import load_data, split_data, preprocess_data

load_dotenv()

def get_model():
    # Create LinearModel
    model = LinearRegression(fit_intercept=True)
    return model
   

# function to train the model
def train_model(pipeline, X_train, y_train):
    pipeline.fit(X_train, y_train)
    return pipeline

# function to evaluate the model

def evaluate_model(model, X_test, y_test):
    """
    Evaluates a model's performance on test data.
    
    Parameters:
    - model: Trained model to evaluate.
    - X_test: Test features.
    - y_test: True labels for the test data.
    
    Returns:
    - A dictionary of evaluation metrics.
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Initialize results dictionary
    results = {}
    
    # Calculate evaluation metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results['mse'] = mse
    results['rmse'] = rmse
    results['r2_score'] = r2
    return results


# function to save the model
def save_model(model, model_path, model_name):
    with open(str(model_path) + "/" + model_name +".pkl", 'wb') as file:
        pickle.dump(model, file)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    # Load data
    data_path = os.getenv("DATA_PATH")
    data = load_data(data_path)
    
    # Preprocess data
    preprocessed_data = preprocess_data(data)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(preprocessed_data)
    
    
    # Train model
    model = train_model(get_model(), X_train, y_train)
    
    # Evaluate model
    accuracy = evaluate_model(model, X_test, y_test)
    print(f"Model accuracy: {accuracy}")
    
    # Save model
    model_path = os.getenv("MODEL_PATH")
    model_name = "model"
    save_model(model, model_path, model_name)
   