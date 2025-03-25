"""
This module is for the business logic of your application. 
"""
import sys 
import os 
from assistr.utils import logger, load_config
from assistr.assistant import Assistant

def on_chat_send(event):
    logger.debug(event)
    return event.msg

if __name__ == "__main__":

    # Load config
    config_name = sys.argv[1]
    config = load_config(config_name)

    # Update the config with this workflow
    file_path = os.path.realpath(__file__)
    file_name_no_ext = os.path.basename(file_path).split('.')[0]
    print(file_name_no_ext)
    config.workflow.name=file_name_no_ext

    assistant = Assistant(config)
    assistant.DB.load_metadata()
    logger.debug(assistant.DB.metadata)