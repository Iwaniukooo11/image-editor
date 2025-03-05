from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Import filter parameter classes
# from core.pipeline.filters.brightness import BrightnessParams
# from core.pipeline.filters.contrast import ContrastParams
# from core.pipeline.filters.grayscale import GrayscaleParams
# from core.pipeline.filters.binarization import BinarizationParams
# from core.pipeline.filters.negative import NegativeParams
# from core.pipeline.filters.average import AverageParams
# from core.pipeline.filters.gaussian import GaussianParams
# from core.pipeline.filters.sharpening import SharpeningParams
# from core.pipeline.filters.sobel import SobelParams
# from core.pipeline.filters.roberts import RobertsParams

# # Dictionary mapping filter names to their parameter classes
# FILTER_PARAM_MAPPING = {
#     'brightness': BrightnessParams,
#     'contrast': ContrastParams,
#     'grayscale': GrayscaleParams,
#     'binarization': BinarizationParams,
#     'negative': NegativeParams,
#     'average': AverageParams,
#     'gaussian': GaussianParams,
#     'sharpening': SharpeningParams,
#     'sobel': SobelParams,
#     'roberts': RobertsParams
# }

# def create_param_ui(param_name, param_info):
#     """Generate UI element based on parameter type and constraints"""
#     if param_info.get('type') == 'slider':
#         return [
#             html.Label(f"{param_name.replace('_', ' ').title()}:"),
#             dcc.Slider(
#                 id=f'{param_name}-slider',
#                 min=param_info.get('min', 0),
#                 max=param_info.get('max', 100),
#                 step=param_info.get('step', 1),
#                 value=param_info.get('default', 0),
#                 marks={
#                     i: str(i) for i in range(
#                         param_info.get('min', 0),
#                         param_info.get('max', 100) + 1,
#                         (param_info.get('max', 100) - param_info.get('min', 0)) // 5
#                     )
#                 },
#                 tooltip={"placement": "bottom", "always_visible": True}
#             )
#         ]
#     elif param_info.get('type') == 'dropdown':
#         return [
#             html.Label(f"{param_name.replace('_', ' ').title()}:"),
#             dcc.Dropdown(
#                 id=f'{param_name}-dropdown',
#                 options=[{'label': opt, 'value': val} for val, opt in param_info.get('options', {}).items()],
#                 value=param_info.get('default')
#             )
#         ]
#     elif param_info.get('type') == 'radio':
#         return [
#             html.Label(f"{param_name.replace('_', ' ').title()}:"),
#             dcc.RadioItems(
#                 id=f'{param_name}-radio',
#                 options=[{'label': opt, 'value': val} for val, opt in param_info.get('options', {}).items()],
#                 value=param_info.get('default')
#             )
#         ]
#     # Add more UI element types as needed
#     return []

# def register_callbacks(app):
#     @app.callback(
#         Output('filter-parameters', 'children'),
#         Input('filter-dropdown', 'value')
#     )
#     def update_filter_parameters(selected_filter):
#         """Display parameter controls based on the filter's parameter class"""
#         if not selected_filter or selected_filter not in FILTER_PARAM_MAPPING:
#             return None
        
#         # Get the parameter class for the selected filter
#         param_class = FILTER_PARAM_MAPPING[selected_filter]
        
#         # Get parameter definitions from the class
#         param_definitions = param_class.get_param_definitions()
        
#         # Generate UI elements for each parameter
#         ui_elements = []
#         for param_name, param_info in param_definitions.items():
#             ui_elements.extend(create_param_ui(param_name, param_info))
        
#         if not ui_elements:
#             return html.P("No parameters for this filter.")
        
#         return dbc.Card([
#             dbc.CardBody(ui_elements)
#         ])