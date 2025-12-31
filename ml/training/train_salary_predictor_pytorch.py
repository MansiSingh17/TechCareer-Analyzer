#!/usr/bin/env python3
"""
Train salary prediction model using PyTorch
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer, LabelEncoder
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
import joblib
from tqdm import tqdm

class SalaryPredictorModel(nn.Module):
    def __init__(self, input_dim: int):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, x):
        return self.network(x)

def load_salary_data(data_path: str) -> pd.DataFrame:
    """Load prepared salary data"""
    if not os.path.exists(data_path):
        print(f"❌ Data file not found: {data_path}")
        print("\nPrepare data first:")
        print("  python ml/preprocessing/prepare_training_data.py --salary")
        sys.exit(1)
    
    df = pd.read_csv(data_path)
    df['skills'] = df['skills'].apply(lambda x: x.split(',') if isinstance(x, str) else [])
    return df

def prepare_features(df: pd.DataFrame):
    """Prepare features for PyTorch"""
    mlb = MultiLabelBinarizer()
    skills_encoded = mlb.fit_transform(df['skills'])
    
    le_location = LabelEncoder()
    location_encoded = le_location.fit_transform(df['location'].fillna('Unknown'))
    location_onehot = pd.get_dummies(location_encoded, prefix='location')
    
    features = np.hstack([
        df[['experience_years']].values,
        skills_encoded,
        location_onehot.values
    ])
    
    labels = df['salary'].values
    
    return features, labels, mlb, le_location

def train_pytorch_model(
    data_path: str = "./data/processed/salary_data.csv",
    output_path: str = "./data/models/salary_predictor_pytorch",
    epochs: int = 100,
    batch_size: int = 32,
    learning_rate: float = 0.001
):
    """Train PyTorch model"""
    
    print("\n" + "="*70)
    print("🚀 TRAINING SALARY PREDICTOR WITH PYTORCH")
    print("="*70)
    
    # Load data
    print("\n1️⃣  Loading data...")
    df = load_salary_data(data_path)
    print(f"   ✅ {len(df)} samples loaded")
    
    # Prepare features
    print("\n2️⃣  Preparing features...")
    X, y, skill_encoder, location_encoder = prepare_features(df)
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert to tensors
    X_train_tensor = torch.FloatTensor(X_train_scaled)
    y_train_tensor = torch.FloatTensor(y_train).reshape(-1, 1)
    X_test_tensor = torch.FloatTensor(X_test_scaled)
    y_test_tensor = torch.FloatTensor(y_test).reshape(-1, 1)
    
    # Data loaders
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    
    # Build model
    print("\n3️⃣  Building PyTorch model...")
    input_dim = X_train.shape[1]
    model = SalaryPredictorModel(input_dim)
    
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    print(f"   Model: {sum(p.numel() for p in model.parameters())} parameters")
    
    # Training loop
    print("\n4️⃣  Training...")
    print("="*70)
    
    best_test_loss = float('inf')
    
    for epoch in range(epochs):
        model.train()
        train_loss = 0
        
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            predictions = model(batch_X)
            loss = criterion(predictions, batch_y)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        
        avg_train_loss = train_loss / len(train_loader)
        
        # Validation
        model.eval()
        with torch.no_grad():
            test_predictions = model(X_test_tensor)
            test_loss = criterion(test_predictions, y_test_tensor)
            
            # R²
            ss_res = torch.sum((y_test_tensor - test_predictions) ** 2)
            ss_tot = torch.sum((y_test_tensor - torch.mean(y_test_tensor)) ** 2)
            r2_score = 1 - (ss_res / ss_tot)
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1:3}/{epochs} | Train RMSE: ${np.sqrt(avg_train_loss):>8,.0f} | Test RMSE: ${np.sqrt(test_loss.item()):>8,.0f} | R²: {r2_score.item():.4f}")
        
        # Save best
        if test_loss < best_test_loss:
            best_test_loss = test_loss
            
            os.makedirs(output_path, exist_ok=True)
            torch.save({
                'model_state_dict': model.state_dict(),
                'input_dim': input_dim,
                'r2_score': r2_score.item()
            }, f"{output_path}/model.pth")
            
            joblib.dump(scaler, f"{output_path}/scaler.pkl")
            joblib.dump(skill_encoder, f"{output_path}/skill_encoder.pkl")
            joblib.dump(location_encoder, f"{output_path}/location_encoder.pkl")
    
    print("="*70)
    print(f"\n✅ Best Test RMSE: ${np.sqrt(best_test_loss):,.0f}")
    print(f"✅ Final R² Score: {r2_score.item():.4f}")
    
    # Sample predictions
    print("\n🎯 Sample Predictions:")
    print("="*70)
    model.eval()
    with torch.no_grad():
        predictions = model(X_test_tensor).numpy().flatten()
        actual = y_test
        
        for i in range(min(10, len(predictions))):
            print(f"{i+1:2}. Actual: ${actual[i]:>10,.0f} | Predicted: ${predictions[i]:>10,.0f}")
    
    print("="*70)
    print("\n✅ TRAINING COMPLETE!")

if __name__ == "__main__":
    train_pytorch_model()
