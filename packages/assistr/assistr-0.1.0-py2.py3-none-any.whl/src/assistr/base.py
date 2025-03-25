import os 
import param
from loguru import logger
from dotenv import load_dotenv
from typing import Callable
from assistr.paneltools.main import pn
from functools import wraps

from assistr.utils import NoOverwriteDict, logger, Event, workflow_event_handler_name, load_config
from assistr.assistant import Assistant

load_dotenv(override=True) 

config_name = os.environ.get("ISC_ASSISTANT_CONF")
if not config_name:
    logger.error(f"Config path must be set in ENV VAR ISC_ASSISTANT_CONF")
else:
    logger.info(f"Loading config from {config_name}")
    
config = load_config(config_name)
assistant = Assistant(config)

## COMPONENT AND EVENT MANAGEMENT
## ####################################
""" All UI components are registered with the component manager via the RegisterComponent decorator.
This provides a central place to create a single message bus for all component communication.
"""
class ComponentManager:
    
    def __init__(self):
        self.component_registry = NoOverwriteDict()
    
    def add(self, component):
        # Add all events with *
        if len(component.events) == 1 and component.events[0] == '*':
            events = list(component.param.values())
        else:
            events = component.events
        
        if events:
            watcher = component.param.watch(ui_event_handler, events, onlychanged=False) 
        else:
            watcher = None

        logger.debug(f"Component Manager Added {component.name} of type {type(component)}: {events}")
        if component.name in self.component_registry.keys():
            logger.warning(f"Component {component.name} already exists in registry")
        else:
            self.component_registry[component.name] = (component,events, watcher)

    def reset(self):
        self.component_registry.clear()

class RegisterComponent:
    def __init__(self, func: Callable):
        wraps(func)(self)
        self.func = func
    
    def __call__(self, *args, **kwargs):
        result = self.func(*args, **kwargs)
        component_manager.add(result)
        return result

def chat_callback(contents, user, instance):
    """ We use the chat callback to interface wiith the standard eventing system. You could do this also by 
     watching an event on the chat interface like _callback_trigger, but you have to then dig into to chat instance
     list of widgets to get the text area value to set the content.
     """
    logger.debug("Entered chat_callback")
    event = param.parameterized.Event(what="value", name=instance.name, obj=instance, cls=type(instance),
                                      old="", new=contents, type="send")
    event = Event(event)
    event.msg = contents
    response = ui_event_handler(event)

    return response

def ui_event_handler(*events):
    # Centralized path for all events which are then dispatched to a handler per component
    response = None
    for event in events:
        handler_fun = workflow_event_handler_name.format(event_name=event.name, event_type=event.type)
        if not handler_fun:
            logger.debug(f"Event {event} requires a a wrokflow handler function named {handler_fun}")
        workflow_handler = getattr(assistant.workflow.workflow_module, handler_fun)
        if not workflow_handler:
            logger.error(f'Workflow does not contain a method for {event.name}_{event.type}')
        else:
            response = workflow_handler(event)

        return response

## ####################################

def load_extensions(component_config: dict):
    extensions = [v for k, v in component_config.items() if k == 'extensions']
    extensions = [ex for exs in extensions for ex in exs]
    logger.debug(f"Extensions {extensions}")
    pn.extension(*extensions)
    
component_manager = ComponentManager()
