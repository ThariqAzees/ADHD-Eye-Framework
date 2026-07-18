import os
import sys
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score, confusion_matrix
)

# Insert project root to module search path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.features import CORRECTED_FEATURE_NAMES, LEGACY_FEATURE_NAMES

RANDOM_SEED = 42

# Define models and grids to match train_model.py exactly
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

models_config = {
    'Logistic_Regression': {
        'estimator': LogisticRegression(random_state=RANDOM_SEED, solver='liblinear'),
        'param_grid': {
            'clf__C': [0.01, 0.1, 1.0, 10.0],
            'clf__penalty': ['l2']
        }
    },
    'Random_Forest': {
        'estimator': RandomForestClassifier(random_state=RANDOM_SEED),
        'param_grid': {
            'clf__n_estimators': [50, 100],
            'clf__max_depth': [3, 5, None],
            'clf__min_samples_split': [2, 5]
        }
    },
    'XGBoost': {
        'estimator': XGBClassifier(random_state=RANDOM_SEED, eval_metric='logloss'),
        'param_grid': {
            'clf__n_estimators': [50, 100],
            'clf__max_depth': [3, 5],
            'clf__learning_rate': [0.05, 0.1, 0.2]
        }
    }
}

def calculate_cohens_d(x1, x2):
    n1, n2 = len(x1), len(x2)
    if n1 <= 1 or n2 <= 1:
        return 0.0
    s1, s2 = np.var(x1, ddof=1), np.var(x2, ddof=1)
    pooled_se = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    if pooled_se == 0:
        return 0.0
    return (np.mean(x1) - np.mean(x2)) / pooled_se

def benjamini_hochberg(p_values):
    n = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    q_values = np.zeros(n)
    min_q = 1.0
    for i in range(n - 1, -1, -1):
        q = sorted_p[i] * n / (i + 1)
        min_q = min(min_q, q)
        q_values[i] = min_q
    original_q = np.zeros(n)
    original_q[sorted_indices] = q_values
    return original_q

def evaluate_nested_cv_detailed(X, y, subject_ids, model_name, classifier, param_grid):
    outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_SEED)
    
    detailed_folds = []
    oof_predictions = []
    
    for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X, y)):
        X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        test_subjects = subject_ids.iloc[test_idx]
        
        # Build pipeline
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('clf', classifier)
        ])
        
        # Grid Search on training fold
        grid_search = GridSearchCV(
            pipeline,
            param_grid=param_grid,
            cv=inner_cv,
            scoring='f1',
            n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        
        # Predict on outer test fold
        y_pred = best_model.predict(X_test)
        y_prob = best_model.predict_proba(X_test)[:, 1] if hasattr(best_model, 'predict_proba') else y_pred
        
        # Compute fold metrics
        acc = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        
        # Specificity and Balanced Accuracy
        cm = confusion_matrix(y_test, y_pred)
        if cm.shape == (2, 2):
            tn, fp, fn, tp = cm.ravel()
            spec = tn / (tn + fp) if (tn + fp) > 0 else 0.0
            bal_acc = (recall + spec) / 2.0
        else:
            spec = 0.0
            bal_acc = acc
            
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        try:
            auc = roc_auc_score(y_test, y_prob)
        except:
            auc = 0.5
            
        try:
            pr_auc = average_precision_score(y_test, y_prob)
        except:
            pr_auc = 0.0
            
        detailed_folds.append({
            'Model': model_name,
            'Fold': fold_idx + 1,
            'Accuracy': acc,
            'Balanced_Accuracy': bal_acc,
            'Precision': precision,
            'Recall': recall,
            'Specificity': spec,
            'F1_Score': f1,
            'ROC_AUC': auc,
            'PR_AUC': pr_auc
        })
        
        # Record Out-of-Fold Predictions
        for sub_id, t_cls, p_cls, p_prob in zip(test_subjects, y_test, y_pred, y_prob):
            oof_predictions.append({
                'subject_id': sub_id,
                'true_class': t_cls,
                'predicted_class': p_cls,
                'predicted_probability': p_prob,
                'outer_fold': fold_idx + 1,
                'model': model_name
            })
            
    return detailed_folds, oof_predictions

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "data", "processed", "dataset_features_REAL_v1.0.csv")
    output_dir = os.path.join(base_dir, "experimental_audit", "publication_evidence")
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_csv(csv_path)
    y = df['group'].map({'ADHD': 1, 'Control': 0})
    subject_ids = df['subject_id']
    
    # ----------------------------------------------------
    # 1. DESCRIPTIVE STATISTICS
    # ----------------------------------------------------
    print("[DESCRIPTIVE STATS]")
    desc_rows = []
    # Include all features (union of legacy and corrected)
    all_features = sorted(list(set(LEGACY_FEATURE_NAMES + CORRECTED_FEATURE_NAMES)))
    
    for feat in all_features:
        for group_label, group_name in [(1, 'ADHD'), (0, 'Control')]:
            vals = df[y == group_label][feat].dropna().values
            n_val = len(vals)
            mean_val = float(np.mean(vals)) if n_val > 0 else np.nan
            sd_val = float(np.std(vals, ddof=1)) if n_val > 1 else np.nan
            median_val = float(np.median(vals)) if n_val > 0 else np.nan
            
            if n_val > 1:
                q25, q75 = np.percentile(vals, [25, 75])
                iqr_val = float(q75 - q25)
            else:
                iqr_val = np.nan
                
            min_val = float(np.min(vals)) if n_val > 0 else np.nan
            max_val = float(np.max(vals)) if n_val > 0 else np.nan
            
            desc_rows.append({
                'Feature': feat,
                'Group': group_name,
                'N': n_val,
                'Mean': mean_val,
                'SD': sd_val,
                'Median': median_val,
                'IQR': iqr_val,
                'Min': min_val,
                'Max': max_val
            })
            
    desc_df = pd.DataFrame(desc_rows)
    desc_df.to_csv(os.path.join(output_dir, "descriptive_statistics.csv"), index=False)
    
    # ----------------------------------------------------
    # 2. INFERENTIAL STATISTICS
    # ----------------------------------------------------
    print("[INFERENTIAL STATS]")
    inf_rows = []
    p_vals = []
    
    for feat in all_features:
        adhd_vals = df[y == 1][feat].dropna().values
        ctrl_vals = df[y == 0][feat].dropna().values
        
        stat, p_val = stats.mannwhitneyu(adhd_vals, ctrl_vals, alternative='two-sided')
        p_vals.append(p_val)
        
        d = calculate_cohens_d(adhd_vals, ctrl_vals)
        d_abs = abs(d)
        if d_abs < 0.2:
            interp = "Negligible"
        elif d_abs < 0.5:
            interp = "Small"
        elif d_abs < 0.8:
            interp = "Medium"
        else:
            interp = "Large"
            
        inf_rows.append({
            'Feature': feat,
            'Test': 'Mann-Whitney U',
            'Statistic': stat,
            'Raw p-value': p_val,
            'Effect size': d,
            'Effect-size interpretation': interp
        })
        
    q_vals = benjamini_hochberg(np.array(p_vals))
    for idx, r in enumerate(inf_rows):
        r['FDR-adjusted p-value'] = q_vals[idx]
        
    inf_df = pd.DataFrame(inf_rows)
    inf_df.to_csv(os.path.join(output_dir, "statistical_comparisons.csv"), index=False)
    
    # ----------------------------------------------------
    # 3. COMPLETE MODEL PERFORMANCE (Analysis B)
    # ----------------------------------------------------
    print("[MODEL PERFORMANCE]")
    detailed_perf_rows = []
    oof_predictions_rows = []
    summary_perf_rows = []
    
    X_corrected = df[CORRECTED_FEATURE_NAMES]
    
    for m_name, config in models_config.items():
        detailed_folds, oof_predictions = evaluate_nested_cv_detailed(
            X_corrected, y, subject_ids, m_name, config['estimator'], config['param_grid']
        )
        detailed_perf_rows.extend(detailed_folds)
        oof_predictions_rows.extend(oof_predictions)
        
        # Calculate summary metrics (mean, std, 95% CI)
        folds_df = pd.DataFrame(detailed_folds)
        metrics = ['Accuracy', 'Balanced_Accuracy', 'Precision', 'Recall', 'Specificity', 'F1_Score', 'ROC_AUC', 'PR_AUC']
        
        summary_entry = {'Model': m_name}
        for m in metrics:
            m_mean = folds_df[m].mean()
            m_std = folds_df[m].std()
            # SE = std/sqrt(5)
            se = m_std / np.sqrt(5)
            # t-dist value for df=4, 95% CI is t=2.776
            ci_half = 2.776 * se
            summary_entry[f'{m}_Mean'] = m_mean
            summary_entry[f'{m}_SD'] = m_std
            summary_entry[f'{m}_95CI_Lower'] = m_mean - ci_half
            summary_entry[f'{m}_95CI_Upper'] = m_mean + ci_half
            
        summary_perf_rows.append(summary_entry)
        
    pd.DataFrame(detailed_perf_rows).to_csv(os.path.join(output_dir, "model_performance_detailed.csv"), index=False)
    pd.DataFrame(summary_perf_rows).to_csv(os.path.join(output_dir, "model_performance_summary.csv"), index=False)
    pd.DataFrame(oof_predictions_rows).to_csv(os.path.join(output_dir, "out_of_fold_predictions.csv"), index=False)
    
    # ----------------------------------------------------
    # 4. SINGLE-FEATURE PERFORMANCE (Analysis B)
    # ----------------------------------------------------
    print("[SINGLE FEATURE PERFORMANCE]")
    sf_rows = []
    
    feature_group_mapping = {
        'mean_reaction_time_ms': 'Reaction Time',
        'median_reaction_time_ms': 'Reaction Time',
        'rt_variability': 'Reaction Time',
        'rt_coefficient_of_variation': 'Reaction Time',
        'accuracy_overall': 'Behavioral',
        'accuracy_by_load_diff': 'Behavioral',
        'accuracy_by_distractor_diff': 'Behavioral',
        'omission_rate': 'Behavioral',
        'false_alarm_rate': 'Behavioral',
        'hit_rate': 'Behavioral',
        'normalized_fixation_instability': 'Gaze',
        'normalized_gaze_dispersion': 'Gaze',
        'pupil_variability': 'Pupil'
    }
    
    for feat in CORRECTED_FEATURE_NAMES:
        X_feat = df[[feat]]
        # Use simple Logistic Regression for single feature baseline
        lr_clf = LogisticRegression(random_state=RANDOM_SEED, solver='liblinear')
        lr_grid = {'clf__C': [0.01, 0.1, 1.0, 10.0]}
        
        detailed_folds, _ = evaluate_nested_cv_detailed(
            X_feat, y, subject_ids, f'LR_{feat}', lr_clf, lr_grid
        )
        folds_df = pd.DataFrame(detailed_folds)
        
        sf_rows.append({
            'Feature': feat,
            'Group': feature_group_mapping.get(feat, 'Other'),
            'Balanced Accuracy': folds_df['Balanced_Accuracy'].mean(),
            'F1': folds_df['F1_Score'].mean(),
            'ROC-AUC': folds_df['ROC_AUC'].mean(),
            'PR-AUC': folds_df['PR_AUC'].mean()
        })
        
    pd.DataFrame(sf_rows).to_csv(os.path.join(output_dir, "single_feature_performance.csv"), index=False)
    
    # ----------------------------------------------------
    # 5. FEATURE-GROUP ABLATION
    # ----------------------------------------------------
    print("[FEATURE-GROUP ABLATION]")
    ablation_groups = {
        'A_Behavioral_only': ['accuracy_overall', 'accuracy_by_load_diff', 'accuracy_by_distractor_diff', 'omission_rate', 'false_alarm_rate', 'hit_rate'],
        'B_Reaction_Time_only': ['mean_reaction_time_ms', 'median_reaction_time_ms', 'rt_variability', 'rt_coefficient_of_variation'],
        'C_Gaze_only': ['normalized_fixation_instability', 'normalized_gaze_dispersion'],
        'D_Pupil_only': ['pupil_variability'],
        'E_Gaze_and_Pupil': ['normalized_fixation_instability', 'normalized_gaze_dispersion', 'pupil_variability'],
        'F_Behavioral_and_RT': ['accuracy_overall', 'accuracy_by_load_diff', 'accuracy_by_distractor_diff', 'omission_rate', 'false_alarm_rate', 'hit_rate',
                              'mean_reaction_time_ms', 'median_reaction_time_ms', 'rt_variability', 'rt_coefficient_of_variation'],
        'G_Behavioral_RT_and_Gaze': ['accuracy_overall', 'accuracy_by_load_diff', 'accuracy_by_distractor_diff', 'omission_rate', 'false_alarm_rate', 'hit_rate',
                                     'mean_reaction_time_ms', 'median_reaction_time_ms', 'rt_variability', 'rt_coefficient_of_variation',
                                     'normalized_fixation_instability', 'normalized_gaze_dispersion'],
        'H_Behavioral_RT_and_Pupil': ['accuracy_overall', 'accuracy_by_load_diff', 'accuracy_by_distractor_diff', 'omission_rate', 'false_alarm_rate', 'hit_rate',
                                      'mean_reaction_time_ms', 'median_reaction_time_ms', 'rt_variability', 'rt_coefficient_of_variation',
                                      'pupil_variability'],
        'I_Behavioral_RT_and_GazePupil': CORRECTED_FEATURE_NAMES
    }
    
    ablation_detailed_rows = []
    ablation_summary_rows = []
    
    for g_name, g_feats in ablation_groups.items():
        X_group = df[g_feats]
        for m_name, config in models_config.items():
            detailed_folds, _ = evaluate_nested_cv_detailed(
                X_group, y, subject_ids, m_name, config['estimator'], config['param_grid']
            )
            
            # Record detailed fold variation
            for fold in detailed_folds:
                fold['Ablation_Group'] = g_name
                ablation_detailed_rows.append(fold)
                
            folds_df = pd.DataFrame(detailed_folds)
            ablation_summary_rows.append({
                'Ablation_Group': g_name,
                'Model': m_name,
                'Balanced Accuracy': folds_df['Balanced_Accuracy'].mean(),
                'Balanced Accuracy SD': folds_df['Balanced_Accuracy'].std(),
                'F1': folds_df['F1_Score'].mean(),
                'F1 SD': folds_df['F1_Score'].std(),
                'ROC-AUC': folds_df['ROC_AUC'].mean(),
                'ROC-AUC SD': folds_df['ROC_AUC'].std(),
                'PR-AUC': folds_df['PR_AUC'].mean(),
                'PR-AUC SD': folds_df['PR_AUC'].std()
            })
            
    pd.DataFrame(ablation_detailed_rows).to_csv(os.path.join(output_dir, "ablation_detailed.csv"), index=False)
    pd.DataFrame(ablation_summary_rows).to_csv(os.path.join(output_dir, "ablation_summary.csv"), index=False)
    
    # ----------------------------------------------------
    # 6. SENSITIVITY COMPARISON (mean_pupil_proxy)
    # ----------------------------------------------------
    print("[SENSITIVITY COMPARISON]")
    # Run nested CV on corrected features PLUS mean_pupil_proxy
    X_sens = df[CORRECTED_FEATURE_NAMES + ['mean_pupil_proxy']]
    
    sens_rows = []
    for m_name, config in models_config.items():
        detailed_folds, _ = evaluate_nested_cv_detailed(
            X_sens, y, subject_ids, m_name, config['estimator'], config['param_grid']
        )
        folds_df = pd.DataFrame(detailed_folds)
        sens_rows.append({
            'Model': m_name,
            'With_Pupil_Proxy_F1': folds_df['F1_Score'].mean(),
            'With_Pupil_Proxy_AUC': folds_df['ROC_AUC'].mean()
        })
    sens_df = pd.DataFrame(sens_rows)
    print("Sensitivity results (WITH mean_pupil_proxy):")
    print(sens_df.to_string(index=False))
    sens_df.to_csv(os.path.join(output_dir, "sensitivity_pupil_proxy.csv"), index=False)

    print("\n[SUCCESS] Generated all publication evidence files!")

if __name__ == "__main__":
    main()
