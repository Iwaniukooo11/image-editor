from dash import html
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State,ALL
from core.pipeline.image_pipeline import ImagePipeline
from core.pipeline.filters.brightness import BrightnessParams, BrightnessFilter
from core.pipeline.filters.contrast import ContrastParams,ContrastFilter
from core.pipeline.filters.grayscale import GrayscaleParams, GrayscaleFilter
from core.pipeline.filters.binarization import BinarizationParams, BinarizationFilter
from core.pipeline.filters.negative import NegativeParams, NegativeFilter
from core.pipeline.convolutions.average import AverageParams, AverageConvolution
from core.pipeline.convolutions.gaussian import GaussianParams, GaussianConvolution
from core.pipeline.convolutions.sharpening import SharpeningParams, SharpeningConvolution
from core.pipeline.edges.sobel import SobelParams,SobelEdge
from core.pipeline.edges.roberts import RobertsParams,RobertsEdge
import base64
import io
import numpy as np
from PIL import Image


# Dictionary mapping filter names to their parameter classes
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
                id={'type':'slider','index':f'{param_name}-slider'},
                min=param_info.get('min', 0),
                max=param_info.get('max', 100),
                step=param_info.get('step', 1),
                value=param_info.get('default', 0),
                # marks={i: str(i) for i in range(param_info.get('min', 0), param_info.get('max', 100) + 1, 10)},
                marks=None,
                tooltip={"placement": "bottom", "always_visible": True}
                
            )
        ]
    elif param_info.get('type') == 'dropdown':
        return [
            html.Label(f"{param_name.replace('_', ' ').title()}:"),
            dcc.Dropdown(
                # id=f'{param_name}-dropdown',
                id={'type':'dropdown','index':f'{param_name}-dropdown'},
                options=[{'label': opt, 'value': val} for val, opt in param_info.get('options', {}).items()],
                value=param_info.get('default')
            )
        ]
    elif param_info.get('type') == 'radio':
        return [
            html.Label(f"{param_name.replace('_', ' ').title()}:"),
            dcc.RadioItems(
                # id=f'{param_name}-radio',
                id={'type':'radio','index':f'{param_name}-radio'},
                options=[{'label': opt, 'value': val} for val, opt in param_info.get('options', {}).items()],
                value=param_info.get('default')
            )
        ]
    # Add more UI element types as needed
    return []

def parse_contents(contents):
    return html.Img(src=contents, style={'width': '100%', 'height': 'auto'})

def register_callbacks(app):
    @app.callback(
        Output('filter-parameters', 'children'),
        Input('filter-dropdown', 'value')
    )
    def update_filter_parameters(selected_filter):
        """Display parameter controls based on the filter's parameter class"""
        if not selected_filter or selected_filter not in FILTER_PARAM_MAPPING:
            return None
        print('gowno')
        # Get the parameter class for the selected filter
        param_class = FILTER_PARAM_MAPPING[selected_filter]
        
        # Get parameter definitions from the class
        param_definitions = param_class.get_param_definitions()
        
        # Generate UI elements for each parameter
        ui_elements = []
        for param_name, param_info in param_definitions.items():
            ui_elements.extend(create_param_ui(param_name, param_info))
        
        if not ui_elements:
            return html.P("No parameters for this filter.")
        
        return dbc.Card([
            dbc.CardBody(ui_elements)
        ])


    # @app.callback(Output('output-image-upload', 'children'),
    #               Input('upload-image', 'contents'))
    # def update_output_foo(contents):
    #     if contents is not None:
            
    #         return parse_contents(contents)
    #     return html.Div()
    
    @app.callback(Output('add-filter', 'disabled'),
                  [Input('upload-image', 'contents'),
                   Input('filter-dropdown', 'value')])
    def toggle_add_filter_button(contents, filter_value):
        print('aaaa')
        return contents is None or filter_value is None

 # ...existing code...
    @app.callback(
    # Output('output-image-upload', 'children',allow_duplicate=True),
    # Input('add-filter', 'n_clicks'),
    # Input('filter-dropdown', 'value'),
    # Input({'type': 'slider', 'index': ALL}, 'value'),
    # Input('output-image-upload', 'children'),
    # Input('upload-image', 'contents'),
    # prevent_initial_call=True
    Output('output-image-upload', 'children', allow_duplicate=True),
    Input('add-filter', 'n_clicks'),
    Input('upload-image', 'contents'),
    
    State('filter-dropdown', 'value'),
    State({'type': 'slider', 'index': ALL}, 'value'),
    State({'type': 'dropdown', 'index': ALL}, 'value'),
    State({'type': 'radio', 'index': ALL}, 'value'),
    # State('output-image-upload', 'children'),
    State('output-image-upload', 'children'),
    prevent_initial_call=True
)
    def update_history(n_clicks,upload_image,filter_value, slider_values,dropdown_values,radio_values, image):
        # print('start',filter_value,slider_values)
        # if 'add-filter' not in  [p['prop_id'] for p in dash.callback_context.triggered][0]:
        # # or not filter_value:
        #     print('exiting...')
            
        #     # print(dash.callback_context.triggered[0])
            
        #     if image['props']['children'] is not None:
        #         print('in if')
        #         return parse_contents(image)
        print('start')
        if n_clicks==0 or n_clicks is None:
            print('in if2')
            return parse_contents(upload_image)
        
        # Create a list of parameter information with selected values
        param_info_list = []
        for i, value in enumerate(slider_values):
            print(f"Slider {i + 1}: {value}")
        
        for i, value in enumerate(dropdown_values):
            print(f"Dropdown {i + 1}: {value}")
        
        for i, value in enumerate(radio_values):
            print(f"Radio {i + 1}: {value}")
        
        # Return the filter information
        # print('image',image)
        # print('image',image)
        header, _, encoded = image['props']['src'].partition(',')
        decoded = base64.b64decode(encoded)
        
        with io.BytesIO(decoded) as buf:
            pil_img = Image.open(buf).convert('RGB')
            image = np.array(pil_img)

        # Uzyskujemy przetworzone dane z pipeline
        print('filter_value',filter_value,'n',n_clicks)
        pipeline = ImagePipeline(image)
        # print('!',filter_value,slider_values,'valuye=',value)
        if(filter_value=='brightness'):
            pipeline.add_step(filter=BrightnessFilter(),params=BrightnessParams(value=slider_values[0]))
            
        elif(filter_value=='contrast'):
            pipeline.add_step(filter=ContrastFilter(),params=ContrastParams(value=slider_values[0]))
            
        elif(filter_value=='grayscale'):
            pipeline.add_step(filter=GrayscaleFilter(),params=GrayscaleParams(method=radio_values[0],intensity=slider_values[0]))
        
        elif(filter_value=='binarization'):
            pipeline.add_step(filter=BinarizationFilter(),params=BinarizationParams(threshold=slider_values[0]))
            
        elif(filter_value=='negative'):
            pipeline.add_step(filter=NegativeFilter(),params=NegativeParams())
        elif(filter_value=='average'):
            pipeline.add_step(filter=AverageConvolution(),params=AverageParams(slider_values[0]))
            
        elif(filter_value=='gaussian'):
            pipeline.add_step(filter=GaussianConvolution(),params=GaussianParams(kernel_size=slider_values[0],sigma=slider_values[1]))
            
        elif(filter_value=='sharpening'):
            pipeline.add_step(filter=SharpeningConvolution(),params=SharpeningParams(kernel_size=slider_values[0],alpha=slider_values[1]))
            
        elif(filter_value=='sobel'):
            pipeline.add_step(filter=SobelEdge(),params=SobelParams(slider_values[0]))
        
        
        elif(filter_value=='roberts'):
            pipeline.add_step(filter=RobertsEdge(),params=RobertsParams(slider_values[0]))
        
        result_array=pipeline.execute()
        result_array=result_array.astype(np.uint8)

        # Konwertujemy wynik (NumPy) ponownie na PIL
        result_img = Image.fromarray(result_array)

        # Zapis do pamięci w formacie PNG
        buff = io.BytesIO()
        result_img.save(buff, format="PNG")
        encoded_result = base64.b64encode(buff.getvalue()).decode("utf-8")

        # Budujemy URI data:image/png;base64,...
        base64_uri = f"data:image/png;base64,{encoded_result}"
        print('before return')
        # Zwracamy gotowy obraz przez parse_contents
        return parse_contents(base64_uri)
   
    # @app.callback(
    #     Output('history-steps', 'children'),
    #     Input('value-slider', 'value'),
    #     Input('intensity-slider', 'intensity'),
    #     Input('add-filter', 'n_clicks'),
    #     Input('filter-dropdown', 'value')
    # )
    # def update_history(value, n_clicks, filter_value):
    #     if n_clicks !=1:
    #         return None
    #     return html.Div([
    #         html.P(f"Filter: {filter_value}, Value: {value}")
    #     ])
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

        # Extract base64 image data
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