"""
This module is for the business logic of your application. 
"""
from assistr.utils import logger 

def on_chat_send(event):
    logger.debug(event)
    return event.msg