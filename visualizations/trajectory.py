import pandas as pd
import plotly.graph_objects as go

def plot_gaze_vs_target_trajectory(df_valid: pd.DataFrame) -> go.Figure:
    """
    Plots spatial overlay of predicted gaze positions (scatter) vs the target path (line).
    """
    fig = go.Figure()
    
    # Gaze positions
    fig.add_trace(go.Scatter(
        x=df_valid['gaze_x'], 
        y=df_valid['gaze_y'],
        mode='markers',
        marker=dict(size=4, color='#39FF14', opacity=0.5),
        name='Gaze Position'
    ))
    
    # Target path
    fig.add_trace(go.Scatter(
        x=df_valid['target_x'], 
        y=df_valid['target_y'],
        mode='lines',
        line=dict(color='#00E5FF', width=3),
        name='Target Path'
    ))
    
    fig.update_layout(
        title="Gaze Trajectory vs Target Path Overlay",
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        xaxis=dict(showgrid=False, title='Screen X (px)', range=[0, 1920]),
        yaxis=dict(showgrid=False, title='Screen Y (px)', range=[1080, 0]), # inverted Y to match screen coords
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

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
