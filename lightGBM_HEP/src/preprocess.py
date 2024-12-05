import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_and_label_parquet_files(input_dir, signal_prefix="ZH"):
    """
    Load all Parquet files from a directory and assign labels based on file names.
    
    Parameters:
    - input_dir (str): Path to the directory containing Parquet files.
    - signal_prefix (str): Prefix to identify signal files.
    
    Returns:
    - pd.DataFrame: Combined DataFrame with a 'label' column.
    """
    parquet_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.parquet')]
    if not parquet_files:
        raise FileNotFoundError(f"No Parquet files found in {input_dir}")
    
    dataframes = []
    for file in parquet_files:
        label = 1 if os.path.basename(file).startswith(signal_prefix) else 0
        print(f"Loading {file} with label {label}")
        df = pd.read_parquet(file)
        df['label'] = label
        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)

def preprocess_data(input_dir, features, label_column="label", test_size=0.2):
    """
    Load data, filter rows, normalize features, and split into train-test sets.
    """
    print(f"Loading and labeling data from {input_dir}...")
    dataset = load_and_label_parquet_files(input_dir)

    # Filter rows with invalid values (e.g., zeros in specific features)
    dataset = dataset[(dataset[features] > 0).all(axis=1)]

    # Split features and labels
    X = dataset[features]
    y = dataset[label_column]

    # Normalize features
    # scaler = StandardScaler()
    # X_scaled = scaler.fit_transform(X)

    X_scaled = X

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=test_size, random_state=42)
    print(f"Data preprocessing complete. Train samples: {len(X_train)}, Test samples: {len(X_test)}")
    
    return X_train, X_test, y_train, y_test
