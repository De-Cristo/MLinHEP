from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import os

def plot_confusion_matrix(model, X_test, y_test, output_dir):
    """
    Plot and save the confusion matrix.
    
    Parameters:
    - model: Trained LightGBM model.
    - X_test: Test feature set.
    - y_test: True labels for the test set.
    - output_dir: Directory to save the confusion matrix plot.
    Plot and save the confusion matrix in PRL style.
    """
    y_pred = model.predict(X_test)  # Get class predictions
    cm = confusion_matrix(y_test, y_pred)

    fig, ax = plt.subplots(figsize=(3.5, 2.5))  # PRL-style size
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Background", "Signal"])
    disp.plot(cmap='Blues', values_format='d', ax=ax, colorbar=False)
    ax.set_title("")  # Remove default title
    ax.set_xlabel("Predicted", fontsize=10)
    ax.set_ylabel("True", fontsize=10)
    ax.tick_params(labelsize=8)
    plt.tight_layout()

    # Save in PRL format
    confusion_matrix_path = os.path.join(output_dir, "confusion_matrix.eps")
    plt.savefig(confusion_matrix_path, format='eps')

    # Save in PNG format
    confusion_matrix_png_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(confusion_matrix_png_path, format='png', dpi=300)  # High resolution for PNG

    plt.close()
    print(f"Confusion matrix saved to {confusion_matrix_path}")

from scipy.stats import ks_2samp
import pandas as pd


def ks_test_train_vs_validation(train_signal_scores, 
                                train_background_scores, 
                                val_signal_scores, 
                                val_background_scores, output_dir):
    """
    Perform KS test comparing training and validation datasets for both signal and background.
    """
    # Perform KS test for signal
    ks_stat_signal, p_value_signal = ks_2samp(train_signal_scores, val_signal_scores)
    print(f"Signal KS Statistic: {ks_stat_signal}, p-value: {p_value_signal}")

    # Perform KS test for background
    ks_stat_background, p_value_background = ks_2samp(train_background_scores, val_background_scores)
    print(f"Background KS Statistic: {ks_stat_background}, p-value: {p_value_background}")

    # Plot cumulative distributions for signal
    plt.figure(figsize=(3.5, 2.5))
    plt.hist(train_signal_scores, bins=50, density=True, histtype='step', cumulative=True, label='Train Signal', color='blue')
    plt.hist(val_signal_scores, bins=50, density=True, histtype='step', cumulative=True, label='Validation Signal', color='red')
    plt.xlabel('BDT Score', fontsize=10)
    plt.ylabel('Cumulative Probability', fontsize=10)
    plt.title(f"Signal KS Test\nKS={ks_stat_signal:.3f}, p={p_value_signal:.3e}", fontsize=9)
    plt.legend(fontsize=8, loc='best')
    plt.tight_layout()
    signal_plot_path = os.path.join(output_dir, "ks_test_signal_train_vs_val.eps")
    plt.savefig(signal_plot_path, format='eps')
    signal_plot_png_path = os.path.join(output_dir, "ks_test_signal_train_vs_val.png")
    plt.savefig(signal_plot_png_path, format='png', dpi=300)
    plt.close()
    print(f"Signal KS test plots saved to {signal_plot_path} and {signal_plot_png_path}")

    # Plot cumulative distributions for background
    plt.figure(figsize=(3.5, 2.5))
    plt.hist(train_background_scores, bins=50, density=True, histtype='step', cumulative=True, label='Train Background', color='blue')
    plt.hist(val_background_scores, bins=50, density=True, histtype='step', cumulative=True, label='Validation Background', color='red')
    plt.xlabel('BDT Score', fontsize=10)
    plt.ylabel('Cumulative Probability', fontsize=10)
    plt.title(f"Background KS Test\nKS={ks_stat_background:.3f}, p={p_value_background:.3e}", fontsize=9)
    plt.legend(fontsize=8, loc='best')
    plt.tight_layout()
    background_plot_path = os.path.join(output_dir, "ks_test_background_train_vs_val.eps")
    plt.savefig(background_plot_path, format='eps')
    background_plot_png_path = os.path.join(output_dir, "ks_test_background_train_vs_val.png")
    plt.savefig(background_plot_png_path, format='png', dpi=300)
    plt.close()
    print(f"Background KS test plots saved to {background_plot_path} and {background_plot_png_path}")

def plot_feature_importance(model, features, output_dir):
    """
    Generate and save the feature importance plot in PRL style with cleaned feature names.
    
    Parameters:
    - model: Trained LightGBM model.
    - features: List of feature names.
    - output_dir: Directory to save the plot.
    """
    # Remove the "events_" prefix from feature names
    cleaned_features = [feature.replace("events_", "") for feature in features]

    # Extract feature importance and sort
    importance = model.feature_importances_
    importance_df = pd.DataFrame({'Feature': cleaned_features, 'Importance': importance}).sort_values(by='Importance', ascending=False)

    # Create PRL-style plot
    plt.figure(figsize=(3.5, 2.5))  # Compact PRL-style size
    plt.barh(importance_df['Feature'], importance_df['Importance'], color='blue', height=0.6)
    plt.gca().invert_yaxis()  # Highest importance at the top
    plt.xlabel('Importance', fontsize=10)
    plt.ylabel('Feature', fontsize=10)
    plt.tick_params(axis='x', labelsize=8)
    plt.tick_params(axis='y', labelsize=7)
    plt.tight_layout()

    # Save in EPS format
    feature_importance_eps_path = os.path.join(output_dir, "feature_importance.eps")
    plt.savefig(feature_importance_eps_path, format='eps')
    print(f"Feature importance plot saved to {feature_importance_eps_path}")

    # Save in PNG format
    feature_importance_png_path = os.path.join(output_dir, "feature_importance.png")
    plt.savefig(feature_importance_png_path, format='png', dpi=300)
    print(f"Feature importance plot saved to {feature_importance_png_path}")

    plt.close()

from sklearn.metrics import roc_curve, auc

def plot_roc_curve(model, X_test, y_test, output_dir):
    """
    Generate and save the ROC curve in PRL style.
    
    Parameters:
    - model: Trained LightGBM model.
    - X_test: Test feature set.
    - y_test: True labels for the test set.
    - output_dir: Directory to save the plot.
    """
    # Get prediction scores
    y_scores = model.predict_proba(X_test)[:, 1]
    
    # Calculate ROC curve and AUC
    fpr, tpr, _ = roc_curve(y_test, y_scores)
    roc_auc = auc(fpr, tpr)

    # Create PRL-style ROC plot
    plt.figure(figsize=(3.5, 2.5))  # Compact PRL-style size
    plt.plot(fpr, tpr, label=f'AUC = {roc_auc:.2f}', color='blue', lw=1.5)
    plt.plot([0, 1], [0, 1], 'k--', lw=1)  # Diagonal line
    plt.xlabel('False Positive Rate', fontsize=10)
    plt.ylabel('True Positive Rate', fontsize=10)
    plt.tick_params(labelsize=8)
    plt.legend(fontsize=8, loc='lower right')
    plt.tight_layout()

    # Save in EPS format
    roc_curve_eps_path = os.path.join(output_dir, "roc_curve.eps")
    plt.savefig(roc_curve_eps_path, format='eps')
    print(f"ROC curve saved to {roc_curve_eps_path}")

    # Save in PNG format
    roc_curve_png_path = os.path.join(output_dir, "roc_curve.png")
    plt.savefig(roc_curve_png_path, format='png', dpi=300)  # High resolution for PNG
    print(f"ROC curve saved to {roc_curve_png_path}")

    plt.close()

import numpy as np

def plot_prediction_score_distribution(model, X_train, y_train, X_val, y_val, output_dir):
    """
    Generate and save the normalized prediction score distribution plot in PRL style.

    Parameters:
    - model: Trained LightGBM model.
    - X_train: Training feature set.
    - y_train: Training labels.
    - X_val: Validation feature set.
    - y_val: Validation labels.
    - output_dir: Directory to save the plot.
    """
    # Get prediction scores
    train_scores = model.predict_proba(X_train)[:, 1]
    val_scores = model.predict_proba(X_val)[:, 1]

    # Separate training and validation scores for signal and background
    train_signal_scores = train_scores[y_train == 1]
    train_background_scores = train_scores[y_train == 0]
    val_signal_scores = val_scores[y_val == 1]
    val_background_scores = val_scores[y_val == 0]

    # Normalize histograms to ensure both training and validation are comparable
    train_signal_density, train_signal_bins = np.histogram(train_signal_scores, bins=50, density=True)
    train_background_density, train_background_bins = np.histogram(train_background_scores, bins=50, density=True)
    train_signal_bin_centers = (train_signal_bins[:-1] + train_signal_bins[1:]) / 2
    train_background_bin_centers = (train_background_bins[:-1] + train_background_bins[1:]) / 2

    # Create PRL-style plot
    plt.figure(figsize=(3.5, 2.5))

    # Plot normalized histograms for training data (filled)
    plt.hist(train_signal_scores, bins=50, alpha=0.6, label='Train Signal', density=True, color='blue')
    plt.hist(train_background_scores, bins=50, alpha=0.6, label='Train Background', density=True, color='red')

    # Calculate validation histograms as ROOT-style points
    for scores, label, color in [
        (val_signal_scores, 'Validation Signal', 'blue'),
        (val_background_scores, 'Validation Background', 'red')
    ]:
        # Compute histogram for validation data
        counts, bin_edges = np.histogram(scores, bins=50, density=True)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_width = bin_edges[1] - bin_edges[0]

        # Calculate errors
        total_counts, _ = np.histogram(scores, bins=50)  # Non-normalized counts
        errors = np.sqrt(total_counts) / (len(scores) * bin_width)  # Normalize errors

        # Plot data points with error bars
        plt.errorbar(bin_centers, counts, yerr=errors, fmt='o', label=label, color=color, markersize=3, capsize=1, linestyle='none')

    # PRL-style labels and legend
    plt.xlabel('Prediction Score', fontsize=10)
    plt.ylabel('Density', fontsize=10)
    plt.tick_params(labelsize=8)
    plt.legend(fontsize=8, loc='best')
    plt.tight_layout()

    # Save in EPS format
    score_distribution_eps_path = os.path.join(output_dir, "prediction_score_distribution.eps")
    plt.savefig(score_distribution_eps_path, format='eps')
    print(f"Prediction score distribution saved to {score_distribution_eps_path}")

    # Save in PNG format
    score_distribution_png_path = os.path.join(output_dir, "prediction_score_distribution.png")
    plt.savefig(score_distribution_png_path, format='png', dpi=300)
    print(f"Prediction score distribution saved to {score_distribution_png_path}")

    plt.close()

    return train_signal_scores, train_background_scores, val_signal_scores, val_background_scores

