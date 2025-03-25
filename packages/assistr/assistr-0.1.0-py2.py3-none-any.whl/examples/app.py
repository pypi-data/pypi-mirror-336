from assistr.paneltools.main import pn
from loguru import logger

from assistr.paneltools.golden import IRISGoldenTemplate
from assistr.app_config import frost_css
from assistr.utils import logger

from assistr.base import component_manager, load_extensions
from assistr.base_components import create_chat, create_sidebar

# This is an important configuration. It maps the components with the events
# that you want to subscribe to. To listen to all events set it to ['*']
# Some components, like chat, can be provided with a callback, which can be 
# used instead to capture initial event if this is easier(and it is for chat)
component_config = {"chat": {"events": []}, "extensions": ["perspective"],
                    "sidebar": {"events": []}, "extensions": [""],
                    }


# Reset component manager as it will load when app starts and on refresh
component_manager.reset()
logger.debug(f"Component registry: {component_manager.component_registry}")

def create_ui():

    # Load the required extensions before creating components
    # This can be removed and let each be lazy loaded but warnings will be issued 
    load_extensions(component_config)

    ## CREATE COMPONENTS
    ###########################
    logger.info("Creating components")
    
    chat_name = 'chat'
    chat_config = component_config.get(chat_name)
    chat = create_chat(name=chat_name, events=chat_config.get('events'))
    
    params = {}
    params["stylesheets"] = [
            """ {
                  background-color: #fffffc;
            }
            """
        ]
    sidebar_name = 'sidebar'
    sidebar_config = component_config.get(sidebar_name)
    sidebar = create_sidebar(name=sidebar_name, events=sidebar_config.get('events'), params=params)
    

    logger.trace(f"Component registry: {component_manager.component_registry}")
    logger.info("Finished creating components")
    ###########################
    ## CREATE COMPONENTS


    ## BEGIN CREATE TEMPLATE
    ###########################
    logger.info("Creating Template, adding components and css")
    header_row = pn.Row(styles={"text-align": "center"}, height=40) 

    template = IRISGoldenTemplate(
            title="IRIS Assistant",
            header=[header_row],
            header_background = '#FFFFFF')

    template.main.append(pn.Card(chat, title="Chat", name="Chat", hide_header=True))
    template.main.append(pn.Card(sidebar, title="Sidebar", name="Sidebar", hide_header=True))

    pn.extension(raw_css=[frost_css])
    logger.info("Completed Template creation")
    ###########################
    ## END CREATE TEMPLATE

    return template
    
template = create_ui()

logger.debug(f"Template.main {[f'{w}\n' for w in template.main]}")
template.servable()
