from dash import html
import base64
import io
import numpy as np
import pandas as pd
from PIL import Image
import plotly.express as px

def parse_contents(contents):
    return html.Img(src=contents, style={'width': '100%', 'height': 'auto'})

def generate_histogram(image):
    """Generate an RGB histogram plot for the image with frequency on the y-axis."""
    r = image[:, :, 0].flatten()
    g = image[:, :, 1].flatten()
    b = image[:, :, 2].flatten()

    df = pd.DataFrame({
        'Channel': ['R'] * len(r) + ['G'] * len(g) + ['B'] * len(b),
        'Value': np.concatenate([r, g, b])
    })

    fig = px.histogram(
        df,
        x='Value',
        color='Channel',
        nbins=256,
        barmode='overlay',
        color_discrete_map={'R': 'red', 'G': 'green', 'B': 'blue'}
    )
    fig.update_layout(
        title='RGB Histogram',
        xaxis_title='Channel Value',
        yaxis_title='Frequency'
    )
    return fig

def generate_projections(image):
    """Generate horizontal and vertical projection figures by converting image to grayscale first, then summing pixel values."""
    gray = np.mean(image, axis=2)
    h_proj = np.sum(gray, axis=1)
    v_proj = np.sum(gray, axis=0)

    fig_h = px.line(y=h_proj, title="Horizontal Projection")
    fig_h.update_layout(xaxis_title="Row", yaxis_title="Sum of Intensity")

    fig_v = px.line(y=v_proj, title="Vertical Projection")
    fig_v.update_layout(xaxis_title="Column", yaxis_title="Sum of Intensity")

    return fig_h, fig_v

def generate_image_stats(image):
    """Return a Dash component with basic image stats, like dimensions, min/max, and mean pixel."""
    height, width, channels = image.shape
    min_val = image.min()
    max_val = image.max()
    mean_val = image.mean()

    return html.Div([
        html.P(f"Dimensions: {width} x {height}"),
        html.P(f"Channels: {channels}"),
        html.P(f"Min Pixel Value: {min_val}"),
        html.P(f"Max Pixel Value: {max_val}"),
        html.P(f"Mean Pixel Value: {mean_val:.2f}")
    ])