import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_gaze_error_timeline(df_valid: pd.DataFrame) -> px.line:
    """
    Plots the tracking error timeline by trajectory.
    """
    # Prevent warning when modifying a copy by using .copy()
    df = df_valid.copy()
    if len(df) > 0:
        df['time_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]) / 1000.0
    else:
        df['time_sec'] = []
        
    fig = px.line(
        df, 
        x='time_sec', 
        y='error_px',
        color='trial_phase',
        labels={'time_sec': 'Elapsed Time (seconds)', 'error_px': 'Tracking Error (pixels)'},
        title="Tracking Error Timeline by Trajectory"
    )
    fig.update_layout(
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def plot_reaction_time_timeline(df_resp: pd.DataFrame) -> px.scatter:
    """
    Plots the reaction time timeline by trial load & distractor.
    """
    fig = px.scatter(
        df_resp, 
        x='trial', 
        y='reaction_time_ms',
        color='distractor_type',
        size='load',
        labels={'trial': 'Trial Number', 'reaction_time_ms': 'Reaction Time (ms)'},
        title="Reaction Time Timeline by Trial Load & Distractor"
    )
    fig.update_layout(
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

def plot_pupil_proxy_trace(df_trial: pd.DataFrame) -> go.Figure:
    """
    Plots mean pupil size proxy across trials.
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_trial.index + 1,
        y=df_trial['pupil_proxy_mean'],
        mode='lines+markers',
        line=dict(color='#00E5FF'),
        name='Mean Pupil Proxy (px)'
    ))
    fig.update_layout(
        title="Webcam-Based Iris Size Mean Trace across Trials",
        xaxis_title="Trial Number",
        yaxis_title="Average Iris Radius (pixels)",
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig
