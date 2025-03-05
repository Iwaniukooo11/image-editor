# import numpy as np

# # Globalne zmienne
# original_img = None
# current_img = None

# # Słownik do mapowania filtrów i parametrów
# from layout.callbacks.filter_map import FILTER_MAP

# # Import wszystkich callbacków
# from layout.callbacks.upload_callbacks import register_upload_callbacks
# from layout.callbacks.filter_callbacks import register_filter_callbacks
# from layout.callbacks.processing_callbacks import register_processing_callbacks
# from layout.callbacks.visualization_callbacks import register_visualization_callbacks
# from layout.callbacks.export_callbacks import register_export_callbacks

# def register_callbacks(app):
#     """Rejestruje wszystkie callbacki aplikacji."""
#     register_upload_callbacks(app)
#     register_filter_callbacks(app)
#     register_processing_callbacks(app)
#     register_visualization_callbacks(app)
#     register_export_callbacks(app)