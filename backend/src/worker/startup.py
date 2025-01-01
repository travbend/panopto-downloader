import os
import importlib

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
TASKS_DIR = "tasks"

def initialize():
    for filename in os.listdir(os.path.join(ABS_PATH, TASKS_DIR)):
        if filename.endswith('.py') and filename != '__init__.py':
            model_name = f'{TASKS_DIR}.{filename[:-3]}'
            importlib.import_module(model_name)