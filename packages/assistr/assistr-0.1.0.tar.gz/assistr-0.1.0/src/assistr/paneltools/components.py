import panel as pn
from panel.chat import ChatInterface


class Chat:

    def __init__(self, callback, name: str, metadata: dict):
        self.metadata = metadata
        self.callback = callback
        self.name = name
        self.chat = self.create_chat()

    def _internal_callback(self, contents, user, instance):
        
        self.metadata.update({"id": id(self), "name": self.name})
        print(f"METADATA {self.metadata}")
        setattr(instance, "metadata", self.metadata)
        return self.callback(contents, user, instance)

    def create_chat(self):

        chat = ChatInterface(
            callback=self._internal_callback,
            widgets=pn.widgets.TextAreaInput(
                placeholder="Question?",
                auto_grow=True,
                max_rows=3,
                min_height=20,
                sizing_mode="stretch_both",
            ),
            #avatar=pn.state.user or "User",
            user=pn.state.user or "User",
            callback_user="IRIS SQL Assistant",
            align=('end','end'),
            callback_exception='verbose'
        )
     
        return chat
    

    class Templates(pn.viewable.Viewer):

        # Load all of the selects from the database
        master_message_templates = pn.widgets.Select(name="master_message_select")
        master_message = pn.widgets.TextInput(name="master_message_new")
        master_message = pn.widgets.TextAreaInput(name="master_message")

        system_message_templates = pn.widgets.Select(name="system_message_select")
        system_message = pn.widgets.TextAreaInput(name="system_message")

        user_message_templates = pn.widgets.Select(name="user_message_select")
        user_message = pn.widgets.TextAreaInput(name="user_message")

        examples_message_templates = pn.widgets.Select(name="examples_message_select")
        examples_message = pn.widgets.TextAreaInput(name="examples_message")

        suffix_message_templates = pn.widgets.Select(name="suffix_message_select")
        suffix_message = pn.widgets.TextAreaInput(name="suffix_message")
