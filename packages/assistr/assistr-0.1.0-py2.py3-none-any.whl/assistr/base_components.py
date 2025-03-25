from assistr.paneltools.main import pn
from assistr.base import RegisterComponent, chat_callback

## CREATE COMPONENTS FUNCTIONS
####################################
@RegisterComponent
def create_code_editor(name: str, language: str, 
                       readonly: bool = False, options: dict = {}):
    
    sizing_mode = "stretch_both" if not options.get("sizing_mode") else options.get("sizing_mode")
    font_size = "20pt" if not options.get("setFontSize") else options.get("setFontSize") 
    
    editor = pn.widgets.CodeEditor(name=name, value="", sizing_mode=sizing_mode)
    editor.readonly = readonly
    editor.language = language
    editor.name = name
    editor.setFontSize = font_size

    return editor

@RegisterComponent
def create_chat(name: str, events):
    # TODO - Make callback_user="IRIS Assistant" configurable

    textarea = pn.widgets.TextAreaInput(auto_grow=True, rows=2)
    chat = pn.chat.ChatInterface(
        callback=chat_callback,
        widgets = [textarea],
        user=pn.state.user or "User",
        callback_user="IRIS Assistant",
        align=('end','end'),
        callback_exception = 'verbose',
        show_rerun=False,
        show_undo=False,
        name=name,
        message_params={
        "stylesheets": [
            """
            .message {
                  background-color: #fffffc;
            #     font-family: "Courier New";
            #     font-size: 12px;
            }
            """
        ],
        "reaction_icons": {},
        "show_avatar": False,
        "show_copy_icon": False,
        "timestamp_format": "%b %d, %Y %I:%M %p"
    } )


    # These are extra properties that we use on the callback event
    chat.events = events

    return chat

@RegisterComponent
def create_sidebar(name: str, events: list = [], params: dict = {}):

    column = pn.Column(pn.Spacer(styles=dict(background='white'),   sizing_mode='stretch_both'), name=name)
    column.events = events
  

    return column
####################################
