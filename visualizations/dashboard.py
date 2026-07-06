import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_accuracy_by_load(df_resp: pd.DataFrame) -> go.Figure:
    """
    Plots a bar chart of Sternberg task memory accuracy by working memory load.
    """
    # Calculate accuracies
    acc_load1 = df_resp[df_resp['load'] == 1]['accuracy'].mean() * 100
    acc_load2 = df_resp[df_resp['load'] == 2]['accuracy'].mean() * 100
    
    # Fill NaN values if no trials present
    import numpy as np
    if np.isnan(acc_load1): acc_load1 = 0.0
    if np.isnan(acc_load2): acc_load2 = 0.0

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Load 1 (1 dot)', 'Load 2 (2 dots)'],
        y=[acc_load1, acc_load2],
        marker_color=['#00E5FF', '#58A6FF'],
        name='Accuracy by Load'
    ))
    fig.update_layout(
        title="Sternberg Memory Accuracy by Working Memory Load",
        yaxis=dict(title="Accuracy (%)", range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def plot_accuracy_by_distractor(df_resp: pd.DataFrame) -> px.bar:
    """
    Plots a bar chart of working memory accuracy by distractor interference type.
    """
    dist_means = df_resp.groupby('distractor_type')['accuracy'].mean() * 100
    
    fig = px.bar(
        x=dist_means.index.str.replace('_', ' ').str.title(),
        y=dist_means.values,
        labels={'x': 'Distractor Type', 'y': 'Accuracy (%)'},
        title="Working Memory Accuracy by Distractor Interference"
    )
    fig.update_traces(marker_color='#FFD700')
    fig.update_layout(
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        yaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig
