import os
import optuna
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

def objective(trial, X_train, y_train):
    """
    Objective function for Optuna to optimize LightGBM hyperparameters.
    """
    param = {
        'objective': 'binary',
        'metric': 'auc',
        'verbose': 1,
        'boosting_type': 'gbdt',
        # 'learning_rate': trial.suggest_float('learning_rate', 0.05, 0.1),
        # 'num_leaves': trial.suggest_int('num_leaves', 7, 31),
        # 'max_depth': trial.suggest_int('max_depth', 3, 5),
        # 'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        # 'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        # 'reg_alpha': trial.suggest_float('reg_alpha', 0.0, 10.0),
        # 'reg_lambda': trial.suggest_float('reg_lambda', 0.0, 10.0),
        'learning_rate': 0.03,
        'num_leaves': 31,
        'max_depth': 5,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'reg_alpha': 5.0,
        'reg_lambda': 5.0,
        'n_estimators': 100,  # Fixed for fast tuning; increase later.
        'early_stopping_rounds': 20
    }
    
    # Split train data for internal validation
    X_train_split, X_valid_split, y_train_split, y_valid_split = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    
    # Train model
    model = LGBMClassifier(**param)
    model.fit(X_train_split, y_train_split, eval_set=[(X_valid_split, y_valid_split)])
    
    # Predict and compute AUC
    y_pred = model.predict_proba(X_valid_split)[:, 1]
    auc = roc_auc_score(y_valid_split, y_pred)
    return auc

def train_model(X_train, y_train, model_path, features):
    """
    Optimize LightGBM hyperparameters using Optuna and train the final model.
    """
    print("Optimizing hyperparameters with Optuna...")
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X_train, y_train), n_trials=1)
    
    print("Best parameters:", study.best_params)
    
    # Train the final model with the best parameters
    print("Training final model with best parameters...")
    best_params = study.best_params
    final_model = LGBMClassifier(**best_params, n_estimators=1200)
    final_model.fit(X_train, y_train, feature_name=features)
    # final_model.fit(X_train, y_train)
    
    # Save the model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    final_model.booster_.save_model(model_path)
    print(f"Model saved to {model_path}")
    
    return final_model, study
