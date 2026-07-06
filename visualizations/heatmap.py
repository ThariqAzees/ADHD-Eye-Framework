import pandas as pd
import plotly.express as px

def plot_gaze_density_heatmap(df_valid: pd.DataFrame, title: str = "Gaze Position Density Layout") -> px.density_heatmap:
    """
    Plots a 2D density heatmap of predicted gaze coordinates.
    """
    fig = px.density_heatmap(
        df_valid, 
        x='gaze_x', 
        y='gaze_y',
        nbinsx=40, 
        nbinsy=30,
        labels={'gaze_x': 'Screen X (px)', 'gaze_y': 'Screen Y (px)'},
        title=title
    )
    fig.update_layout(
        paper_bgcolor='#161B22',
        plot_bgcolor='#161B22',
        font=dict(color='#FFFFFF'),
        yaxis=dict(autorange='reversed'), # inverted Y to match screen coords
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig
