import plotly.graph_objects as go
def plot_lines(df, y_columns, labels=None, title="", colors=None):
    """
    Plot multiple lines from a DataFrame using Plotly.

    Args:
        df (pd.DataFrame): DataFrame with a datetime index.
        y_columns (list): List of column names to plot.
        labels (list): Optional list of labels for each line.
        title (str): Title of the chart.
        colors (list): Optional list of line colors.
    """
    fig = go.Figure()
    
    for i, col in enumerate(y_columns):
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col],
            mode="lines",
            name=labels[i] if labels else col,
            line=dict(color=colors[i] if colors and i < len(colors) else None, width=1.8)
        ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Value",
        xaxis_rangeslider_visible=False,
        template="plotly_white"
    )

    return fig
    
