from fastapi import FastAPI
import os
import importlib

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
ROUTERS_DIR = "routers"

def initialize(app: FastAPI):
    for filename in os.listdir(os.path.join(ABS_PATH, ROUTERS_DIR)):
        if filename.endswith('.py') and filename != '__init__.py':
            router_name = f'api.{ROUTERS_DIR}.{filename[:-3]}'
            router_module = importlib.import_module(router_name)
            if hasattr(router_module, 'router'):
                app.include_router(router_module.router)