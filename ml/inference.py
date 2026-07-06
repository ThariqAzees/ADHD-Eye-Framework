import os
import pickle
import pandas as pd
from typing import Dict, Any, Union
from dataset.schema import SubjectAggregateFeatures

def load_model_package() -> dict:
    """Loads the training package from ml/models_v1.0.pkl."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pkl_path = os.path.join(base_dir, "ml", "models_v1.0.pkl")
    
    if not os.path.exists(pkl_path):
        raise FileNotFoundError(f"Model package not found at {pkl_path}. Please run train_model first.")
        
    with open(pkl_path, 'rb') as f:
        package = pickle.load(f)
        
    return package

def predict_adhd_risk(features: Union[SubjectAggregateFeatures, Dict[str, Any]], model_name: str = 'xgboost') -> float:
    """
    Predicts ADHD risk probability (similarity to ADHD clinical patterns)
    based on the aggregate session features and specified model.
    """
    package = load_model_package()
    
    # Check if model is supported
    if model_name not in package['models']:
        raise ValueError(f"Model '{model_name}' not found. Available models: {list(package['models'].keys())}")
        
    pipeline = package['models'][model_name]
    feature_order = package['feature_order']
    
    # Convert features to dict if it's a dataclass
    if hasattr(features, '__dict__'):
        feats_dict = features.__dict__
    else:
        feats_dict = features
        
    # Build dataframe with a single row, ensuring exact column order
    input_data = {}
    for col in feature_order:
        if col in feats_dict:
            input_data[col] = [feats_dict[col]]
        else:
            input_data[col] = [None] # Will be handled by the pipeline imputer
            
    df_input = pd.DataFrame(input_data)
    
    # Run inference using the pipeline
    # predict_proba returns probability for class 0 and 1. We want class 1 (ADHD).
    prob = pipeline.predict_proba(df_input.values)[0, 1]
    return float(prob)
