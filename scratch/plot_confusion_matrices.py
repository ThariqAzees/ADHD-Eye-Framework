import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, "experimental_audit", "publication_evidence", "out_of_fold_predictions.csv")
    df = pd.read_csv(csv_path)
    
    models = df['model'].unique()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    
    # Custom colors
    cmap = sns.light_palette("#2b5c8f", as_cmap=True)
    
    for i, model in enumerate(['Logistic_Regression', 'Random_Forest', 'XGBoost']):
        m_df = df[df['model'] == model]
        y_true = m_df['true_class'].values
        y_pred = m_df['predicted_class'].values
        
        cm = confusion_matrix(y_true, y_pred)
        
        # Format labels
        group_names = ['True Neg\n(Control)', 'False Pos\n(ADHD)', 'False Neg\n(Control)', 'True Pos\n(ADHD)']
        group_counts = [f"{v:d}" for v in cm.flatten()]
        # Percentage of total predictions
        group_percentages = [f"{v:.1%}" for v in cm.flatten() / np.sum(cm)]
        labels = [f"{v1}\n{v2}\n({v3})" for v1, v2, v3 in zip(group_names, group_counts, group_percentages)]
        labels = np.asarray(labels).reshape(2, 2)
        
        ax = axes[i]
        sns.heatmap(cm, annot=labels, fmt='', cmap=cmap, cbar=False, ax=ax,
                    xticklabels=['Control', 'ADHD'], yticklabels=['Control', 'ADHD'],
                    annot_kws={"size": 10, "weight": "bold"})
        
        model_title = model.replace('_', ' ')
        ax.set_title(f"{model_title}\nConfusion Matrix", fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel('Predicted Label', fontsize=10, labelpad=8)
        ax.set_ylabel('True Label', fontsize=10, labelpad=8)
        
    plt.tight_layout()
    fig_dir = os.path.join(base_dir, "experimental_audit", "figures")
    os.makedirs(fig_dir, exist_ok=True)
    fig_path = os.path.join(fig_dir, "confusion_matrices.png")
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    print(f"[SUCCESS] Saved confusion matrices plot to {fig_path}")
    
    # Also copy to handoff_v1.1
    dest_path = os.path.join(base_dir, "conference_paper_handoff_v1.1", "figures", "confusion_matrices.png")
    shutil.copy2(fig_path, dest_path)
    print(f"[SUCCESS] Copied to {dest_path}")
    
if __name__ == '__main__':
    main()
