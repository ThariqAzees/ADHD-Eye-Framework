import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pickle
import datetime
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

def train_and_evaluate_pipelines() -> dict:
    """
    Orchestrates training using Nested Cross-Validation, prints results,
    and saves the final pipelines to ml/models_v1.0.pkl.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "processed", "dataset_features_REAL_v1.0.csv")
    models_dir = os.path.join(base_dir, "ml")
    os.makedirs(models_dir, exist_ok=True)
    models_pkl_path = os.path.join(models_dir, "models_v1.0.pkl")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Processed dataset features not found at {csv_path}. Please run build_dataset first.")
        
    df = pd.read_csv(csv_path)
    
    # Use corrected features for training the live production model
    from ml.features import CORRECTED_FEATURE_NAMES
    X = df[CORRECTED_FEATURE_NAMES]
    feature_names = list(X.columns)
    
    # Map target: ADHD -> 1, Control -> 0
    y = df['group'].map({'ADHD': 1, 'Control': 0}).values
    X_vals = X.values
    
    # Sanity check: verify load effect in features
    # load effect: accuracy_by_load_diff = accuracy(1-dot) - accuracy(2-dot) > 0
    mean_load_diff = df['accuracy_by_load_diff'].mean()
    print(f"Sanity Check: Mean accuracy load difference = {mean_load_diff:.4f}")
    if mean_load_diff <= 0.0:
        print("[WARNING] Working memory load effect sanity check failed: accuracy(1-dot) <= accuracy(2-dot)!")
    else:
        print("[SUCCESS] Working memory load effect sanity check passed.")
        
    # Setup outer CV (5 folds)
    outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    
    # Define models and grids
    models_grid = {
        'logistic_regression': {
            'estimator': LogisticRegression(random_state=42, solver='liblinear'),
            'param_grid': {
                'classifier__C': [0.01, 0.1, 1.0, 10.0],
                'classifier__penalty': ['l2']
            }
        },
        'random_forest': {
            'estimator': RandomForestClassifier(random_state=42),
            'param_grid': {
                'classifier__n_estimators': [50, 100],
                'classifier__max_depth': [3, 5, None],
                'classifier__min_samples_split': [2, 5]
            }
        },
        'xgboost': {
            'estimator': XGBClassifier(random_state=42, eval_metric='logloss'),
            'param_grid': {
                'classifier__n_estimators': [50, 100],
                'classifier__max_depth': [3, 5],
                'classifier__learning_rate': [0.05, 0.1, 0.2]
            }
        }
    }
    
    cv_results = {model_name: [] for model_name in models_grid}
    
    # Nested CV loop
    print("Running Nested Cross-Validation...")
    for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X_vals, y)):
        print(f"\n--- Outer Fold {fold_idx + 1} ---")
        X_train, X_test = X_vals[train_idx], X_vals[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]
        
        for model_name, config in models_grid.items():
            # Pipeline definition
            pipeline = Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
                ('classifier', config['estimator'])
            ])
            
            # GridSearchCV (Inner Loop)
            grid_search = GridSearchCV(
                estimator=pipeline,
                param_grid=config['param_grid'],
                cv=inner_cv,
                scoring='f1',
                n_jobs=-1
            )
            
            grid_search.fit(X_train, y_train)
            best_model = grid_search.best_estimator_
            
            # Evaluate on Outer Test Set
            y_pred = best_model.predict(X_test)
            # Try to get probabilities
            if hasattr(best_model, "predict_proba"):
                y_prob = best_model.predict_proba(X_test)[:, 1]
            else:
                y_prob = y_pred
                
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            try:
                auc = roc_auc_score(y_test, y_prob)
            except:
                auc = 0.5
                
            cv_results[model_name].append({
                'accuracy': acc,
                'precision': prec,
                'recall': rec,
                'f1': f1,
                'auc': auc
            })
            
            print(f"[{model_name}] best params: {grid_search.best_params_} -> test F1 = {f1:.4f}")
            
    # Calculate and display aggregate outer performance
    summary_metrics = {}
    print("\n================ NESTED CV SUMMARY PERFORMANCE ================")
    for model_name, metrics in cv_results.items():
        metrics_df = pd.DataFrame(metrics)
        summary_metrics[model_name] = {}
        print(f"\nModel: {model_name.upper()}")
        for col in metrics_df.columns:
            mean_val = metrics_df[col].mean()
            std_val = metrics_df[col].std()
            summary_metrics[model_name][col] = {'mean': mean_val, 'std': std_val}
            print(f"  {col.capitalize()}: {mean_val:.4f} ± {std_val:.4f}")
            
    # Fit Final Models on ALL data
    print("\nFitting final models on the entire dataset...")
    final_pipelines = {}
    
    # Fit imputer and scaler on full data for reference
    final_imputer = SimpleImputer(strategy='median')
    final_scaler = StandardScaler()
    X_imputed = final_imputer.fit_transform(X_vals)
    X_scaled = final_scaler.fit_transform(X_imputed)
    
    for model_name, config in models_grid.items():
        # Complete pipeline
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('classifier', config['estimator'])
        ])
        
        # GridSearch on full data
        grid_search = GridSearchCV(
            estimator=pipeline,
            param_grid=config['param_grid'],
            cv=inner_cv,
            scoring='f1',
            n_jobs=-1
        )
        grid_search.fit(X_vals, y)
        final_pipelines[model_name] = grid_search.best_estimator_
        print(f"[{model_name}] Final fit complete. Best params: {grid_search.best_params_}")
        
    # Bundle the models, preprocessing steps, feature order, and metadata
    package = {
        "models": final_pipelines,
        "feature_order": feature_names,
        "scaler": final_scaler,
        "imputer": final_imputer,
        "metadata": {
            "framework_version": "1.0.0",
            "feature_extractor_version": "1.0.0",
            "model_version": "1.0.0",
            "dataset_version": "Rojas-Libano-2019-v3",
            "timestamp": datetime.datetime.now().isoformat(),
            "nested_cv_results": summary_metrics
        }
    }
    
    with open(models_pkl_path, 'wb') as f:
        pickle.dump(package, f)
        
    model_pkl_path = os.path.join(models_dir, "model.pkl")
    with open(model_pkl_path, 'wb') as f:
        pickle.dump(package, f)
        
    model_real_pkl_path = os.path.join(models_dir, "model_REAL_v1.0.pkl")
    with open(model_real_pkl_path, 'wb') as f:
        pickle.dump(package, f)
        
    print(f"\nBundled model package saved successfully to {models_pkl_path}, {model_pkl_path}, and {model_real_pkl_path}!")
    return summary_metrics

if __name__ == "__main__":
    train_and_evaluate_pipelines()
