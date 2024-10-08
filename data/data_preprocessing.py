import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing file '{file_path}'.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def preprocess_data(data):
    # check for data to dataframe format
    if not isinstance(data, pd.DataFrame):
        print("Input should be a pandas DataFrame.")
        return None
    # Remove duplicates
    try:
        data = data.drop_duplicates()
    except Exception as e:
        print(f"An error occurred while preprocessing data: {str(e)}")
    
    # Remove rows with missing values
    data = data.dropna()
    
    # drop or delete the unnecessary columns in the data. 
    data = data.drop(['Events', 'Date', 'SeaLevelPressureHighInches', 
                  'SeaLevelPressureLowInches'], axis=1)
    # some values have 'T' which denotes trace rainfall 
    # we need to replace all occurrences of T with 0 
    # so that we can use the data in our model 
    data = data.replace('T', 0.0) 
  
    # the data also contains '-' which indicates no 
    # or NIL. This means that data is not available 
    # we need to replace these values as well. 
    data = data.replace('-', 0.0) 
    
    # convert data types to float for numerical columns
    data = data.apply(pd.to_numeric, errors='coerce')
    data.fillna(0, inplace=True)
    
    # normalize the data
    #Sdata = (data - data.mean()) / data.std()
    
    return data

# function to split the data into training and testing sets
def split_data(data, test_size=0.2):
    X = data.drop('PrecipitationSumInches', axis=1)
    y = data['PrecipitationSumInches']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":

    from dotenv import load_dotenv
    import os
    load_dotenv()
    

    file_path = os.getenv("DATA_PATH")
    data = load_data(file_path)
    
    if data is not None:
        preprocessed_data = preprocess_data(data)
        if preprocessed_data is not None:
            X_train, X_test, y_train, y_test = split_data(preprocessed_data)
            print(f"Training data shape: {X_train.shape}, {y_train.shape}")
            print(f"Testing data shape: {X_test.shape}, {y_test.shape}")
    print(X_test.columns)