from dash import html, dcc
import dash
from dash.dependencies import Input, Output, State, ALL
from core.pipeline.image_pipeline import ImagePipeline
from core.pipeline.filters.brightness import BrightnessParams, BrightnessFilter
from core.pipeline.filters.contrast import ContrastParams, ContrastFilter
from core.pipeline.filters.grayscale import GrayscaleParams, GrayscaleFilter
from core.pipeline.filters.binarization import BinarizationParams, BinarizationFilter
from core.pipeline.filters.negative import NegativeParams, NegativeFilter
from core.pipeline.convolutions.average import AverageParams, AverageConvolution
from core.pipeline.convolutions.gaussian import GaussianParams, GaussianConvolution
from core.pipeline.convolutions.sharpening import SharpeningParams, SharpeningConvolution
from core.pipeline.edges.sobel import SobelParams, SobelEdge
from core.pipeline.edges.roberts import RobertsParams, RobertsEdge
import base64
import io
import numpy as np
from PIL import Image
import dash_bootstrap_components as dbc
from .utils import parse_contents, generate_histogram, generate_projections, generate_image_stats

FILTER_PARAM_MAPPING = {
    'brightness': BrightnessParams,
    'contrast': ContrastParams,
    'grayscale': GrayscaleParams,
    'binarization': BinarizationParams,
    'negative': NegativeParams,
    'average': AverageParams,
    'gaussian': GaussianParams,
    'sharpening': SharpeningParams,
    'sobel': SobelParams,
    'roberts': RobertsParams
}

def create_param_ui(param_name, param_info):
    """Generate UI element based on parameter type and constraints"""
    if param_info.get('type') == 'slider':
        return [
            html.Label(f"{param_name.replace('_', ' ').title()}:"),
            dcc.Slider(
                id={'type': 'slider', 'index': f'{param_name}-slider'},
                min=param_info.get('min', 0),
                max=param_info.get('max', 100),
                step=param_info.get('step', 1),
                value=param_info.get('default', 0),
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ]
    elif param_info.get('type') == 'dropdown':
        return [
            html.Label(f"{param_name.replace('_', ' ').title()}:"),
            dcc.Dropdown(
                id={'type': 'dropdown', 'index': f'{param_name}-dropdown'},
                options=[{'label': opt, 'value': val} for val, opt in param_info.get('options', {}).items()],
                value=param_info.get('default')
            )
        ]
    elif param_info.get('type') == 'radio':
        return [
            html.Label(f"{param_name.replace('_', ' ').title()}:"),
            dcc.RadioItems(
                id={'type': 'radio', 'index': f'{param_name}-radio'},
                options=[{'label': opt, 'value': val} for val, opt in param_info.get('options', {}).items()],
                value=param_info.get('default')
            )
        ]
    return []

def register_callbacks(app):
    @app.callback(
        Output('filter-parameters', 'children'),
        Input('filter-dropdown', 'value')
    )
    def update_filter_parameters(selected_filter):
        """Display parameter controls based on the filter's parameter class"""
        if not selected_filter or selected_filter not in FILTER_PARAM_MAPPING:
            return None
        param_class = FILTER_PARAM_MAPPING[selected_filter]
        param_definitions = param_class.get_param_definitions()
        ui_elements = []
        for param_name, param_info in param_definitions.items():
            ui_elements.extend(create_param_ui(param_name, param_info))
        if not ui_elements:
            return html.P("No parameters for this filter.")
        return dbc.Card([
            dbc.CardBody(ui_elements)
        ])

    @app.callback(Output('add-filter', 'disabled'),
                  [Input('upload-image', 'contents'),
                   Input('filter-dropdown', 'value')])
    def toggle_add_filter_button(contents, filter_value):
        return contents is None or filter_value is None

    @app.callback(
        Output('output-image-upload', 'children', allow_duplicate=True),
        Output('color-histogram', 'figure'),
        Input('add-filter', 'n_clicks'),
        Input('upload-image', 'contents'),
        State('filter-dropdown', 'value'),
        State({'type': 'slider', 'index': ALL}, 'value'),
        State({'type': 'dropdown', 'index': ALL}, 'value'),
        State({'type': 'radio', 'index': ALL}, 'value'),
        State('output-image-upload', 'children'),
        prevent_initial_call=True
    )
    def update_history(n_clicks, upload_image, filter_value, slider_values, dropdown_values, radio_values, image):
        if n_clicks == 0 or n_clicks is None:
            return parse_contents(upload_image), dash.no_update
        header, _, encoded = image['props']['src'].partition(',')
        decoded = base64.b64decode(encoded)
        with io.BytesIO(decoded) as buf:
            pil_img = Image.open(buf).convert('RGB')
            image = np.array(pil_img)
        pipeline = ImagePipeline(image)
        if filter_value == 'brightness':
            pipeline.add_step(filter=BrightnessFilter(), params=BrightnessParams(value=slider_values[0]))
        elif filter_value == 'contrast':
            pipeline.add_step(filter=ContrastFilter(), params=ContrastParams(value=slider_values[0]))
        elif filter_value == 'grayscale':
            pipeline.add_step(filter=GrayscaleFilter(), params=GrayscaleParams(method=radio_values[0], intensity=slider_values[0]))
        elif filter_value == 'binarization':
            pipeline.add_step(filter=BinarizationFilter(), params=BinarizationParams(threshold=slider_values[0]))
        elif filter_value == 'negative':
            pipeline.add_step(filter=NegativeFilter(), params=NegativeParams())
        elif filter_value == 'average':
            pipeline.add_step(filter=AverageConvolution(), params=AverageParams(slider_values[0]))
        elif filter_value == 'gaussian':
            pipeline.add_step(filter=GaussianConvolution(), params=GaussianParams(kernel_size=slider_values[0], sigma=slider_values[1]))
        elif filter_value == 'sharpening':
            pipeline.add_step(filter=SharpeningConvolution(), params=SharpeningParams(kernel_size=slider_values[0], alpha=slider_values[1]))
        elif filter_value == 'sobel':
            pipeline.add_step(filter=SobelEdge(), params=SobelParams(slider_values[0]))
        elif filter_value == 'roberts':
            pipeline.add_step(filter=RobertsEdge(), params=RobertsParams(slider_values[0]))
        result_array = pipeline.execute()
        result_array = result_array.astype(np.uint8)
        result_img = Image.fromarray(result_array)
        buff = io.BytesIO()
        result_img.save(buff, format="PNG")
        encoded_result = base64.b64encode(buff.getvalue()).decode("utf-8")
        base64_uri = f"data:image/png;base64,{encoded_result}"
        fig = generate_histogram(result_array)
        return parse_contents(base64_uri), fig

    @app.callback(
        Output('image-stats-container', 'children'),
        Input('output-image-upload', 'children')
    )
    def update_image_stats_and_projections(image_children):
        if not image_children:
            return dash.no_update
        header, _, encoded = image_children['props']['src'].partition(',')
        decoded = base64.b64decode(encoded)
        with io.BytesIO(decoded) as buf:
            pil_img = Image.open(buf).convert('RGB')
            image_array = np.array(pil_img)
        stats_div = generate_image_stats(image_array)
        fig_h, fig_v = generate_projections(image_array)
        return html.Div([
            stats_div,
            dcc.Graph(figure=fig_h),
            dcc.Graph(figure=fig_v),
        ])

    @app.callback(
        Output('download-link', 'href'),
        Output('download-link', 'download'),
        Output('download-link', 'style'),
        Input('save-photo', 'n_clicks'),
        State('output-image-upload', 'children'),
        State('filename-input', 'value'),
        prevent_initial_call=True
    )
    def save_image(n_clicks, image, filename):
        if n_clicks is None or image is None or filename is None:
            return dash.no_update, dash.no_update, {'display': 'none'}
        header, _, encoded = image['props']['src'].partition(',')
        download_link = f"data:image/png;base64,{encoded}"
        return download_link, filename, {'display': 'block'}

    @app.callback(
        Output('save-status', 'children'),
        Input('download-link', 'href'),
        prevent_initial_call=True
    )
    def update_save_status(href):
        if href:
            return "Image ready for download."
        return "Failed to prepare image for download."