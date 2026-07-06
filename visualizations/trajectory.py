import pandas as pd
import plotly.graph_objects as go



def plot_dispersion_vs_stability(df_trial: pd.DataFrame) -> go.Figure:
    """
    Plots bar/line chart comparison of gaze dispersion (array phase) vs fixation stability by trial.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_trial.index + 1,
        y=df_trial['fixation_stability'],
        marker_color='#58A6FF',
        name='Fixation Instability (SD)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_trial.index + 1,
        y=df_trial['gaze_dispersion_during_array'],
        mode='lines+markers',
        line=dict(color='#FF3366', width=2),
        name='Gaze Dispersion (Array Phase)'
    ))
    
    fig.update_layout(
        title="Gaze Dispersion vs Fixation Stability across Trials",
        xaxis_title="Trial Number",
        yaxis_title="Dispersion/Instability (pixels)",
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig
