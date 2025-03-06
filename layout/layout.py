from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    """
    Creates and returns the layout for the application.
    """
    return dbc.Container([
        dcc.Store(id='image-store'),
        dcc.Store(id='pipeline-store'),
        dcc.Store(id='original-store'),  # Do przechowywania oryginalnego obrazu
        
        # Nagłówek
        dbc.Row(
            dbc.Col([
                html.H1("Image Editor by Mateusz Iwaniuk", className="text-center my-4"),
                html.P("Biometry Course | Faculty of Mathematics and Information Sciences | Warsaw University of Technology", className="text-center my-4"),
                
    ])
        ),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Upload Image"),
                    dbc.CardBody([
                        dcc.Upload(
                            id='upload-image',
                            children=html.Div([
                                'Drag and Drop or ',
                                html.A('Select a File')
                            ]),
                            style={
                                'width': '100%',
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center'
                            },
                            multiple=False
                        ),
                        html.Div(id='upload-info', className="mt-2"),
                        html.Div(id='image-info', className="mt-2 text-muted small")
                    ])
                ], className="mb-4"),
                
                dbc.Card([
                    dbc.CardHeader("Add Filter"),
                    dbc.CardBody([
                        dbc.CardGroup([
                            dcc.Dropdown(
                                id='filter-dropdown',
                                options=[
                                    {'label': 'Brightness', 'value': 'brightness'},
                                    {'label': 'Contrast', 'value': 'contrast'},
                                    {'label': 'Grayscale', 'value': 'grayscale'},
                                    {'label': 'Binarization', 'value': 'binarization'},
                                    {'label': 'Negative', 'value': 'negative'},
                                    {'label': 'Average Blur', 'value': 'average'},
                                    {'label': 'Gaussian Blur', 'value': 'gaussian'},
                                    {'label': 'Sharpening', 'value': 'sharpening'},
                                    {'label': 'Sobel Edge', 'value': 'sobel'},
                                    {'label': 'Roberts Edge', 'value': 'roberts'},
                                ],
                                placeholder="Select a filter",
                                style={"min-width": "300px"}
                            )
                        ]),
                        html.Div(id='filter-parameters', className="mt-3"),
                        dbc.Button("Add Filter!", id="add-filter", color="success", className="mt-3", disabled=True)
                    ])
                ], className="mb-4"),
                
                dbc.Card([
                    dbc.CardHeader("Save Image"),
                    dbc.CardBody([
                        dbc.Input(id="filename-input", placeholder="Enter filename", className="mb-3"),
                        dbc.Button("Save Image", id="save-photo", color="primary", className="mb-3"),
                        html.Div(id='save-status'),
                        html.A('click here', id='download-link', download='', href='', target='_blank', style={'display': 'none'})
                    ])
                ], className="mb-4"),
                
                dbc.Card([
                    dbc.CardHeader("Image Projections and Statistics"),
                    dbc.CardBody([
                        html.Div(id='image-stats-container')
                    ])
                ], className="mb-4")
            ], md=4),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Image Preview"),
                    dbc.CardBody([
                        html.Div(id='output-image-upload', className="text-center")
                    ])
                ], className="mb-4"),
                
                dbc.Card([
                    dbc.CardHeader("Color Histogram"),
                    dbc.CardBody([
                        dcc.Graph(id='color-histogram')
                    ])
                ])
            ], md=8)
        ])
    ], fluid=True, className="mt-4")