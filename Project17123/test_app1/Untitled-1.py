"""
Call this function to delete all objects
from all models in test_app1
"""

def get_all_models():
    import importlib
    # app_models = importlib.import_module('test_app1.models')
    from test_app1 import models
    model_list = dir(models)
    model_list = [x for x in model_list if x.endswith('model')]
    for m in model_list:
        print(eval('models.'+m).objects.delete())

