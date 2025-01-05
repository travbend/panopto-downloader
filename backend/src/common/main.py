import os
import importlib

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "data"
SQLALCHEMY_DIR = "sqlalchemy"
MODELS_DIR = "models"

# for plugin_name in os.listdir(os.path.join(ABS_PATH, PLUGINS_DIR)):
#     plugin_path = os.path.join(ABS_PATH, PLUGINS_DIR, plugin_name)
#     if plugin_name != "__pycache__" and os.path.isdir(plugin_path):
#         for filename in os.listdir(os.path.join(plugin_path, "data", "sqlalchemy", MODELS_DIR)):
#             if filename.endswith('.py') and filename != '__init__.py':
#                 model_name = f'common.{PLUGINS_DIR}.{plugin_name}.{filename[:-3]}'
#                 importlib.import_module(model_name)