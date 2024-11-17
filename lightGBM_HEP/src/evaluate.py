from .eval_utils import *

def evaluate_model(model, X_train, X_test, y_train, y_test, features, output_dir):
    """
    Evaluate the model and generate:
    - ROC curve
    - Feature importance plot
    - Distribution of predicted scores
    - Distributions of all input features for signal and background
    """
    import os
    from sklearn.metrics import roc_curve, auc
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    os.makedirs(output_dir, exist_ok=True)

    #1 Generate ROC Curve
    print("Generating ROC curve...")
    plot_roc_curve(model, X_test, y_test, output_dir)

    #2 Plot Confusion Matrix
    print("Generating confusion matrix...")
    plot_confusion_matrix(model, X_test, y_test, output_dir)

    #3 Generate Feature Importance Plot
    print("Generating feature importance plot...")
    plot_feature_importance(model, features, output_dir)

    #4 Generate Prediction Score Distribution
    print("Generating prediction score distribution...")
    train_signal_scores, train_background_scores, \
    val_signal_scores, val_background_scores = plot_prediction_score_distribution(model, X_train, y_train, X_test, y_test, output_dir)

    #5 Perform KS test for Train vs Validation
    print("Performing KS test for train vs validation datasets...")
    ks_test_train_vs_validation(train_signal_scores, 
                                train_background_scores, 
                                val_signal_scores, 
                                val_background_scores, output_dir)
    
    #6 Input Feature Distributions
    print("Generating input feature distributions...")
    signal_mask = y_test == 1
    background_mask = y_test == 0

    for i, feature in enumerate(features):
        plt.figure()
        plt.hist(X_test[signal_mask, i], bins=50, alpha=0.5, label='Signal', color='blue', density=True)
        plt.hist(X_test[background_mask, i], bins=50, alpha=0.5, label='Background', color='red', density=True)
        plt.xlabel(feature)
        plt.ylabel('Density')
        plt.title(f'Distribution of {feature} (Signal vs Background)')
        plt.legend()
        feature_dist_path = os.path.join(output_dir, f"{feature}_distribution.png")
        plt.savefig(feature_dist_path)
        plt.close()
        print(f"Feature distribution for {feature} saved to {feature_dist_path}")