# Conference Architecture Specification

This document defines the methodology flow diagram using Mermaid syntax for incorporation into the Methods section of the paper.

---

## 1. Flow Diagram (Mermaid)

```mermaid
graph TD
    A["Authentic Figshare Raw Dataset<br>(Pupil_dataset.mat)"] --> B["Quality Filtering & Cohort Selection<br>(Exclude medicated & incomplete sessions)"]
    B --> C["Primary Analyzable Cohort<br>(N = 40; 28 ADHD, 12 Control)"]
    C --> D["Visuospatial Sternberg-Type Memory Trials<br>(160 trials per subject)"]
    D --> E["Feature Extraction & Aggregation<br>(4 Modalities)"]
    
    subgraph Modalities ["Feature Modalities"]
        E1["Behavioral Features<br>(Accuracy, hit/omission rates)"]
        E2["Reaction Time Features<br>(Mean, Median, SD, CV)"]
        E3["Gaze Features<br>(Fixation instability, dispersion)"]
        E4["Pupil Features<br>(Pupil variability)"]
    end
    
    E --> E1 & E2 & E3 & E4
    E1 & E2 & E3 & E4 --> F["Two Analysis Branches"]
    
    subgraph BranchA ["Branch A: Statistical Analysis"]
        F1["Mann-Whitney U Tests"] --> F2["Benjamini-Hochberg FDR Correction"]
        F2 --> F3["Cohen's d Effect Sizes"]
    end
    
    subgraph BranchB ["Branch B: Machine Learning Analysis"]
        G1["Feature Preprocessing<br>(Median Imputation & scaling)"] --> G2["Stratified 5-Fold Nested CV"]
        G2 --> G3["Hyperparameter Grid Search"]
        G3 --> G4["Model Evaluation<br>(LR, RF, XGBoost)"]
        G4 --> G5["Feature-Group Ablation"]
        G4 --> G6["1,000-Shuffle Permutation Tests"]
        G4 --> G7["Out-of-Fold Error Analysis"]
    end
    
    F --> BranchA & BranchB
    BranchA & BranchB --> H["Integrated Scientific Interpretation<br>(Clinical Occam's Razor & Feature Redundancy)"]
```

---

## 2. Layout Specifications
*   **Diagram Placement**: Methods Section (under *Experimental Pipeline*).
*   **Caption**: *Figure 1: Complete experimental methodology and pipeline flow, outlining raw database extraction, cohort selection filtering, multi-modal feature grouping, statistical testing, and nested cross-validation machine learning pipelines.*