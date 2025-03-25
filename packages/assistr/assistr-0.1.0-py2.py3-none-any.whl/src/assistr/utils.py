import sys
import os 
import importlib
from dotenv import load_dotenv
from loguru import logger
from param.parameterized import Event as ParamEvent
from assistr.models import Configuration

import importlib.resources
from pathlib import Path

load_dotenv()

# Logging
logging_level = os.environ.get('IRIS_SA_LOG_LEVEL', 'DEBUG')
logger.remove()
logger.add(sys.stderr, format="<light-yellow>{time:HH:mm:SS.SSS}</light-yellow>|<level>{level}</level>|{module}.{function}|<white>{message}</white>",
           colorize=True, level=logging_level)

# Directories for workflows and configs
working_dir = os.getcwd()
root_dir = os.environ.get("ISC_ASSISTANT_ROOT", os.path.join(working_dir))
config_dir = os.path.join(root_dir,"configs")

# Event vars
workflow_event_handler_name = 'on_{event_name}_{event_type}'
empty_chat_event = ParamEvent(what="value", name="chat", obj="", cls="", old="", new="", type="send")


## LLM vars
default_llm_msg_format = {"content": "","role": "user"}

def load_config(name: str):
    """
    Configs are stored in individual .py files so module should match filename and be stored in the config_dir
    """
    configs = dynamic_import(config_dir)
    config_module = configs.get(name)
    if not config_module:
        raise Exception(f"Cannot find configuation named {name} in {config_dir}")
    
    config_dict = getattr(config_module, "config")
    config = Configuration(**config_dict)
    return config

class Event():

    def __init__(self, event):
        self.what=event.what
        self.name=event.name
        self.obj=event.obj
        self.cls=event.cls
        self.old=event.old
        self.new=event.new
        self.type=event.type


class NoOverwriteDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise KeyError(f"Key '{key}' already exists and cannot be overwritten")
        super().__setitem__(key, value)


def dynamic_import(dir_name: str, root_dir=root_dir):

    modules_dir = os.path.join(root_dir, dir_name)
    logger.debug(f"Modules dir: {modules_dir}")
    modules = {}
    for file in os.listdir(modules_dir):
        if file.endswith('.py'):
            module_path = os.path.join(modules_dir, file)
            module_name = file.split('.')[0]
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[module_name] = module
    return modules



def get_asset_path(package_name, resource_path):
    """
    Retrieves the path to a resource within a package.

    Args:
        package_name (str): The name of the package.
        resource_path (str): The path to the resource within the package.

    Returns:
        pathlib.Path: The path to the resource.
    """
    package = importlib.resources.files(package_name)
    return package.joinpath(resource_path)
