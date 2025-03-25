"""
This module is for the business logic of your application. 

This example shows executing the workflow_echo without the UI.
"""
import sys 

from assistr.utils import logger, load_config, Event, empty_chat_event, workflow_event_handler_name
from assistr.assistant import Assistant
from assistr.models import Configuration

if __name__ == '__main__':

    config_name = sys.argv[1]

    # Init
    config = load_config(config_name)
    assist = Assistant(config)
    
    # Create a chat message event.
    event = Event(empty_chat_event)
    event.msg = "Hello there"
    logger.info(f"Sending message: {event.msg}")

    # Find the wokflow handler function and invoke
    handler_fun = workflow_event_handler_name.format(event_name=event.name, event_type=event.type)
    workflow_handler = getattr(assist.workflow.workflow_module, handler_fun)
    response = workflow_handler(event)

    logger.info(f"Response: {response}")
