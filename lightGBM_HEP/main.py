import yaml,os
from src.preprocess import preprocess_data
from src.train import train_model
from src.evaluate import evaluate_model

def load_config(config_path):
    """
    Load YAML configuration file.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config
    
if __name__ == "__main__":
    # Define paths and features
    
    config_path = "./params/config.yaml"
    config = load_config(config_path)
    train_dir = config["paths"]["train_dir"]
    output_dir = config["paths"]["output_dir"]
    model_path = config["paths"]["model_path"]
    features = config["features"]
    label_column = config["label_column"]
    hyperparameters = config["hyperparameters"]
    
    # Preprocess data
    X_train, X_test, y_train, y_test = preprocess_data(train_dir, features, label_column)
    
    # Train model with Optuna
    model, study = train_model(X_train, y_train, model_path, features)
    # model, study = train_model(X_train, y_train, model_path, hyperparameters)
    
    # Evaluate model
    evaluate_model(model, X_train, X_test, y_train, y_test, features, output_dir)
    