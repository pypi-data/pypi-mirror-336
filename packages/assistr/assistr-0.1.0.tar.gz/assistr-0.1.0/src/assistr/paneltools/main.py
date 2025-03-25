import panel as pn
from assistr.paneltools.golden import IRISGoldenTemplate
from collections import defaultdict

pn.extension()

default_icon = "/assets/square.svg"

class SPApp():

    def __init__(self, module):
        self.module = module
    

class MainTemplate(IRISGoldenTemplate):
    
    def __init__(self, title:str, header_background: str = '#FFFFFF',
                 logo: str='/assets/intersystems-logo.svg', sidebar_width: int=10):
        super().__init__(title=title, header_background=header_background, 
                         logo=logo, sidebar_width=sidebar_width)
        
        self.apps = []
         
    def add_app(self, app_module):
        """Add the app to the app list"""
        app = self.load_app(app_module)
        self.apps.append(app)

    def load_app(self, app_module):
        """Load the app"""
        for comp in app_module.app_components:
            self.main.append(comp)

        self.sidebar.append(app_module.icon)


class Component:

    def __init__(self, name, obj):
        self.name = name 
        self.obj = obj 
        self.id = id(obj)

    def __repr__(self):
        return f"{self.id}:{self.name}:{type(self.obj)}"


class ComponentRegistry:

    def __init__(self):
        self.components = {}    
    
    def add_component(self, name: str, component: object):
        new_comp = Component(name, component)
        if name not in self.components.keys():
            self.components[name] = new_comp
        else:
            raise Exception(f"Cannot add component with the same name as existing component - {name}")


class Subscriptions:

    def __init__(self):

        # A subscriber listens to the events of a component. Each component has a list of subscribers
        self.subscribers = defaultdict(list)


    def subscribe(self, target, listener):
        self.subscribers[target.name].append(listener.name)