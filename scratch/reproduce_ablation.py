import os
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, precision_recall_curve, auc, confusion_matrix

RANDOM_SEED = 42

df = pd.read_csv('data/processed/dataset_features_REAL_v1.0.csv')
feature_cols = [c for c in df.columns if c not in ['subject_id', 'group']]
X = df[feature_cols]
y = df['group'].map({'ADHD': 1, 'Control': 0})
subject_ids = df['subject_id']

models_config = {
    'Logistic_Regression': {
        'estimator': LogisticRegression(solver='liblinear', random_state=RANDOM_SEED),
        'param_grid': {'clf__C': [0.01, 0.1, 1.0, 10.0]}
    },
    'Random_Forest': {
        'estimator': RandomForestClassifier(random_state=RANDOM_SEED),
        'param_grid': {'clf__n_estimators': [50, 100], 'clf__max_depth': [3, 5, None]}
    },
    'XGBoost': {
        'estimator': XGBClassifier(random_state=RANDOM_SEED, eval_metric='logloss'),
        'param_grid': {'clf__n_estimators': [50, 100], 'clf__max_depth': [3, 5], 'clf__learning_rate': [0.05, 0.1]}
    }
}

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
    'I_Behavioral_RT_and_GazePupil': feature_cols
}

def evaluate_nested_cv_detailed(X_sub, y, subject_ids, model_name, classifier, param_grid):
    outer_cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_SEED)
    inner_cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=RANDOM_SEED)
    detailed_folds = []
    
    for fold_idx, (train_idx, test_idx) in enumerate(outer_cv.split(X_sub, y)):
        X_train, X_test = X_sub.iloc[train_idx], X_sub.iloc[test_idx]
        y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
        
        pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
            ('clf', classifier)
        ])
        
        grid_search = GridSearchCV(
            pipeline,
            param_grid=param_grid,
            cv=inner_cv,
            scoring='f1',
            n_jobs=-1
        )
        
        grid_search.fit(X_train, y_train)
        best_model = grid_search.best_estimator_
        
        y_pred = best_model.predict(X_test)
        y_prob = best_model.predict_proba(X_test)[:, 1] if hasattr(best_model, 'predict_proba') else y_pred
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        auc_score = roc_auc_score(y_test, y_prob)
        p_prec, p_rec, _ = precision_recall_curve(y_test, y_prob)
        pr_auc_val = auc(p_rec, p_prec)
        
        cm = confusion_matrix(y_test, y_pred)
        tn, fp, fn, tp = cm.ravel() if cm.shape == (2, 2) else (0, 0, 0, 0)
        spec = tn / (tn + fp) if (tn + fp) > 0 else 0
        bal_acc = (rec + spec) / 2
        
        detailed_folds.append({
            'Model': model_name,
            'Fold': fold_idx + 1,
            'Accuracy': acc,
            'Balanced_Accuracy': bal_acc,
            'Precision': prec,
            'Recall': rec,
            'Specificity': spec,
            'F1_Score': f1,
            'ROC_AUC': auc_score,
            'PR_AUC': pr_auc_val
        })
    return detailed_folds

out_dir = 'experimental_audit/final_ablation_verification'
os.makedirs(out_dir, exist_ok=True)

ablation_detailed_rows = []
ablation_summary_rows = []

for g_name, g_feats in ablation_groups.items():
    X_group = df[g_feats]
    for m_name, config in models_config.items():
        detailed_folds = evaluate_nested_cv_detailed(
            X_group, y, subject_ids, m_name, config['estimator'], config['param_grid']
        )
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

df_det = pd.DataFrame(ablation_detailed_rows)
df_sum = pd.DataFrame(ablation_summary_rows)

df_det.to_csv(os.path.join(out_dir, 'ablation_detailed_REPRODUCED.csv'), index=False)
df_sum.to_csv(os.path.join(out_dir, 'ablation_summary_REPRODUCED.csv'), index=False)
print("Reproduction complete! Saved to experimental_audit/final_ablation_verification/")
