import pandas as pd
import numpy as np
import numerapi
from dotenv import load_dotenv
from langlands_transformer.spectral_drift_monitor import SpectralDriftMonitor
from langlands_transformer.embedding import spectral_embedding
from langlands_transformer.symmetry import enforce_symmetry
from langlands_transformer.propagation import spectral_attention

import os

# Load .env file
load_dotenv()

PUBLIC_ID = os.getenv("NUMERAI_PUBLIC_ID")
SECRET_KEY = os.getenv("NUMERAI_SECRET_KEY")
MODEL_ID = os.getenv("NUMERAI_MODEL_ID")

if not PUBLIC_ID or not SECRET_KEY or not MODEL_ID:
    raise ValueError("Missing Numerai credentials. Make sure .env is correctly set.")


# Initialize Numerai API
napi = numerapi.NumerAPI(public_id=PUBLIC_ID, secret_key=SECRET_KEY)

def download_numerai_data():
    print("Fetching dataset list from Numerai...")

    datasets = napi.list_datasets()

    print("Available datasets:")
    for file in datasets:
        print(file)

    # Updated filters to match v5.0 file names
    train_file = next(file for file in datasets if "train.parquet" in file and "v5" in file)
    live_file = next(file for file in datasets if "live.parquet" in file and "v5" in file)

    print(f"Downloading: {train_file}")
    print(f"Downloading: {live_file}")

    napi.download_dataset(train_file, "train.parquet")
    napi.download_dataset(live_file, "live.parquet")

    print("Download complete.")

def load_features_and_live_data():
    df_train = pd.read_parquet("train.parquet")
    df_live = pd.read_parquet("live.parquet")

    features = [col for col in df_train.columns if col.startswith("feature_")]
    return df_train, df_live, features

def train_mock_model(df_train, features):
    # Placeholder for real model training — for now, simple average of features
    df_train["target"] = df_train[features].mean(axis=1)
    return df_train

def make_spectral_predictions(df_live, features):
    # Compute spectral embeddings + attention-based predictions for live data
    sigma_list = []
    predictions = []

    drift_monitor = SpectralDriftMonitor(drift_threshold=0.05)

    for idx, row in df_live.iterrows():
        feature_values = row[features].values
        mock_prediction = np.mean(feature_values)  # Replace with actual model prediction if desired

        sigma = spectral_embedding(np.mean(feature_values), mock_prediction)
        symmetrized_sigmas = enforce_symmetry(sigma)

        sigma_list.extend(symmetrized_sigmas)
        predictions.append(mock_prediction)

    # Spectral attention across all examples (could be per-feature too)
    attention = spectral_attention(sigma_list)

    # Final blending (could be refined to weight predictions by spectral consistency)
    blended_predictions = np.dot(attention.mean(axis=1), predictions)

    # Optional: Check spectral drift and warn if market conditions have shifted
    drift_monitor.check_drift(sigma_list)

    return df_live["id"], blended_predictions

def save_predictions(ids, predictions, filename="predictions.csv"):
    df = pd.DataFrame({"id": ids, "prediction": predictions})
    df.to_csv(filename, index=False)
    print(f"Predictions saved to {filename}")

def upload_predictions():
    print("Uploading predictions to Numerai...")
    napi.upload_predictions("predictions.csv", model_id=MODEL_ID)
    print("Upload complete!")

def main():
    download_numerai_data()
    df_train, df_live, features = load_features_and_live_data()
    train_mock_model(df_train, features)  # Replace with your own training logic

    ids, predictions = make_spectral_predictions(df_live, features)
    save_predictions(ids, predictions)
    upload_predictions()

if __name__ == "__main__":
    main()
