#!/usr/bin/env python3
"""
Train salary prediction model using TensorFlow/Keras
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, LabelEncoder
import tensorflow as tf
from tensorflow import keras
import joblib

def load_salary_data(data_path: str) -> pd.DataFrame:
    """Load salary training data"""
    if not os.path.exists(data_path):
        print(f"❌ Data file not found: {data_path}")
        print("\nRun this first:")
        print("  python ml/preprocessing/prepare_training_data.py --salary")
        sys.exit(1)
    
    df = pd.read_csv(data_path)
    
    # Convert skills string to list
    if 'skills' in df.columns:
        df['skills'] = df['skills'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
    
    return df

def prepare_features(df: pd.DataFrame):
    """Prepare feature vectors"""
    print("🔧 Preparing features...")
    
    # Encode skills (multi-hot encoding)
    mlb = MultiLabelBinarizer()
    skills_encoded = mlb.fit_transform(df['skills'])
    print(f"   Skills encoded: {skills_encoded.shape[1]} unique skills")
    
    # Encode locations
    le_location = LabelEncoder()
    location_encoded = le_location.fit_transform(df['location'].fillna('Unknown'))
    location_onehot = pd.get_dummies(location_encoded, prefix='location')
    print(f"   Locations encoded: {location_onehot.shape[1]} unique locations")
    
    # Combine features
    features = np.hstack([
        df[['experience_years']].values,
        skills_encoded,
        location_onehot.values
    ])
    
    labels = df['salary'].values
    
    print(f"   Total features: {features.shape[1]}")
    
    return features, labels, mlb, le_location

def build_model(input_dim: int) -> keras.Model:
    """Build TensorFlow/Keras model"""
    model = keras.Sequential([
        keras.layers.Input(shape=(input_dim,)),
        keras.layers.Dense(256, activation='relu'),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(128, activation='relu'),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(64, activation='relu'),
        keras.layers.Dense(1)  # Salary prediction
    ])
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss='mse',
        metrics=['mae', tf.keras.metrics.RootMeanSquaredError(name='rmse')]
    )
    
    return model

def train_salary_predictor_tf(
    data_path: str = "./data/processed/salary_data.csv",
    output_path: str = "./data/models/salary_predictor_tf",
    epochs: int = 100,
    batch_size: int = 32
):
    """Train TensorFlow salary prediction model"""
    
    print("\n" + "="*70)
    print("🚀 TRAINING SALARY PREDICTOR WITH TENSORFLOW")
    print("="*70)
    
    # Load data
    print("\n1️⃣  Loading data...")
    df = load_salary_data(data_path)
    print(f"   ✅ Loaded {len(df)} samples")
    print(f"   Salary range: ${df['salary'].min():,.0f} - ${df['salary'].max():,.0f}")
    print(f"   Mean salary: ${df['salary'].mean():,.0f}")
    
    # Prepare features
    print("\n2️⃣  Preparing features...")
    X, y, skill_encoder, location_encoder = prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"   Train set: {len(X_train)} samples")
    print(f"   Test set: {len(X_test)} samples")
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Build model
    print("\n3️⃣  Building TensorFlow model...")
    input_dim = X_train.shape[1]
    model = build_model(input_dim)
    
    print("\n📐 Model Architecture:")
    model.summary()
    
    # Callbacks
    early_stopping = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1
    )
    
    # Train
    print("\n4️⃣  Training model...")
    print("="*70)
    
    history = model.fit(
        X_train_scaled, y_train,
        validation_data=(X_test_scaled, y_test),
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[early_stopping, reduce_lr],
        verbose=1
    )
    
    # Evaluate
    print("\n5️⃣  Evaluating model...")
    print("="*70)
    
    y_pred_train = model.predict(X_train_scaled, verbose=0).flatten()
    y_pred_test = model.predict(X_test_scaled, verbose=0).flatten()
    
    # Metrics
    train_rmse = np.sqrt(np.mean((y_train - y_pred_train) ** 2))
    test_rmse = np.sqrt(np.mean((y_test - y_pred_test) ** 2))
    
    train_mae = np.mean(np.abs(y_train - y_pred_train))
    test_mae = np.mean(np.abs(y_test - y_pred_test))
    
    # R² score
    ss_res_test = np.sum((y_test - y_pred_test) ** 2)
    ss_tot_test = np.sum((y_test - np.mean(y_test)) ** 2)
    r2_test = 1 - (ss_res_test / ss_tot_test)
    
    print("\n📊 FINAL RESULTS:")
    print("="*70)
    print(f"Test RMSE:  ${test_rmse:>12,.0f}")
    print(f"Test MAE:   ${test_mae:>12,.0f}")
    print(f"R² Score:   {r2_test:>12.4f}")
    print("="*70)
    
    # Save model
    print("\n6️⃣  Saving model...")
    os.makedirs(output_path, exist_ok=True)
    
    model.save(f"{output_path}/model.h5")
    joblib.dump(scaler, f"{output_path}/scaler.pkl")
    joblib.dump(skill_encoder, f"{output_path}/skill_encoder.pkl")
    joblib.dump(location_encoder, f"{output_path}/location_encoder.pkl")
    
    # Save metadata
    import json
    metadata = {
        'model_type': 'tensorflow_keras',
        'input_dim': int(input_dim),
        'test_rmse': float(test_rmse),
        'test_mae': float(test_mae),
        'r2_score': float(r2_test),
        'epochs_trained': len(history.history['loss']),
        'training_samples': len(X_train),
        'test_samples': len(X_test)
    }
    
    with open(f"{output_path}/metadata.json", 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Model saved to: {output_path}/")
    print("   Files created:")
    print("   • model.h5")
    print("   • scaler.pkl")
    print("   • skill_encoder.pkl")
    print("   • location_encoder.pkl")
    print("   • metadata.json")
    
    # Sample predictions
    print("\n🎯 Sample Predictions (Test Set):")
    print("="*70)
    for i in range(min(10, len(y_test))):
        actual = y_test[i]
        predicted = y_pred_test[i]
        error = abs(actual - predicted)
        error_pct = (error / actual) * 100
        
        print(f"{i+1:2}. Actual: ${actual:>10,.0f} | Predicted: ${predicted:>10,.0f} | Error: ${error:>8,.0f} ({error_pct:>5.1f}%)")
    
    print("="*70)
    print("\n✅ TRAINING COMPLETE!")
    print("\nNext steps:")
    print("  1. Test model: python scripts/test_model.py")
    print("  2. Update API to use trained model")
    print("  3. Create visualizations: python scripts/visualize_trends.py")
    
    return model, history

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Train TensorFlow salary predictor")
    parser.add_argument("--data", default="./data/processed/salary_data.csv")
    parser.add_argument("--output", default="./data/models/salary_predictor_tf")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=32)
    
    args = parser.parse_args()
    
    train_salary_predictor_tf(
        data_path=args.data,
        output_path=args.output,
        epochs=args.epochs,
        batch_size=args.batch_size
    )
