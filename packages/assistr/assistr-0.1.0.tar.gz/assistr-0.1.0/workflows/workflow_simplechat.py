"""
This module is for the business logic of your application. 
"""
from assistr.utils import logger 
from assistr.assistant import Assistant

# This is will be set by the calling app: UI panel app, headless run_script, etc..
# Set here for intellisense
assistant = None

# TODO - move this to config
prompt_name = "simple_chat"

def on_chat_send(event):
    logger.debug(event)
    
    ## Use the PromptManager to get the Prompt template associated with this workflow and LLM config
    prompt_template = assistant.get_prompt(prompt_name)
    # TODO - need some way to map the template vars to the event or other vars
    user_msg = prompt_template.format(query=event.msg)
    
    response = assistant.llm.send_msg(user_msg)
    return response
     
  
def send_request(system_msg, user_msg):
    """ This is an idealized send_request. The caller just sends each message and the assistant figures out
    what previous messages to send as context.
    """
    topic = assistant.classify_topic(user_msg)
  
    # Gets the related requests from the current conversation
    related_msgs = assistant.converstion.get_related_topic_requests(topic)

    response = assistant.conversation.send_to_llm(system_msg, user_msg, related_msgs)

    return response
