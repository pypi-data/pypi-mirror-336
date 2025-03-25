import os

from litellm import completion

from assistr.models import Configuration, get_from_list
from assistr.utils import logger, dynamic_import, NoOverwriteDict, default_llm_msg_format
from assistr.db_utils import get_alchemy_engine, get_metadata

from sqlalchemy.schema import CreateTable

class Assistant:
    """The Assistant class manages the workflow, which includes User interaction, communication with the DB's and models(usually LLMS),
    and other required computations or service communication.
    """
    def __init__(self, config: Configuration):
        self.config = config
        self.workflow = Workflow(self.config.workflow, self)
        self.llm = LLM(self.config)
        self.DB = DB(self.config)

        prompt_dir = os.path.join(os.getcwd(), config.prompt_dir)
        self.prompt_manager = PromptManager(prompt_dir)

    def get_prompt(self, prompt_name: str):
        return self.prompt_manager.prompts.get(prompt_name)

class LLM:
    def __init__(self, config: Configuration):
        self.config = config
        logger.debug(f" {config.default_llm}, {config.llms}")
        self.active_llm_config = get_from_list(config.llms, config.default_llm)
        self.request_reponses = []

    def send_msg(self, msgs):    

        # This will usually be a list of messages that will be populated with
        # a prompt template and determining what other previous messages to send
        if not isinstance(msgs, list):
            msg_dict = dict(default_llm_msg_format)
            msg_dict["content"] = msgs
            msgs = [msg_dict]

        logger.debug(msgs)
        # TODO - Save the config, request and reponse in a request-reponse object and store in self.request_reponses
        logger.debug(f"MODEL DUMP {self.active_llm_config.params}")
        response = completion(messages=msgs, **self.active_llm_config.params)

        text_repsonse = response.choices[0].message.content
        return text_repsonse 

class DB:
    def __init__(self, config: Configuration):
        self.config = config
        self.sqlalchemy_engine = get_alchemy_engine(self.config)
        self.metadata = None
        self.alchemy_metadata = None

    def load_metadata(self):
        metadata, sql_metadata = get_metadata(config=self.config)
        self.create_table_text = ""
        self.create_table_list = []
        for table in sql_metadata.tables.values():
            self.create_table_text += CreateTable(table).compile(self.sqlalchemy_engine).string
            self.create_table_list.append(CreateTable(table).compile(self.sqlalchemy_engine).string)
        
        return metadata, sql_metadata

class Workflow:
    """ A Workflow is primarily a set of "actions"(functions) which serve as entrypoints to the workflow. The 
    purpose is to provide a standard way of handling the problem of working with the unknown starting input of 
    a user's NL query and having a model handle the intention of the users query by setting the action in it's response.

    ??The Workflow class just manages the dynamic invocation of the necessary workflow actions, which are all contained in
    a workflow module, and communication with the assistant.??
    """
    def __init__(self, config, assistant):
        self.config = config
        self.workflow_modules = dynamic_import("workflows")
        self.workflow_module = self.workflow_modules.get(config.active_workflow)
        self.workflow_module.assistant = assistant

class PromptManager:
    """ Replace with agent_fp PromptManager using Jinja
    """

    def __init__(self, dir_path: str):

        if not os.path.isdir(dir_path):
            logger.error(f"PromptManager dir {dir_path} does not exist")
        else:
            self.prompts = self.load_prompts(dir_path)

    def load_prompts(self, dir_path):
        prompts = NoOverwriteDict()
        for file in os.listdir(dir_path):
            if file.endswith('.txt'):
                file_path = os.path.join(dir_path, file)
                with open(file_path) as fi:
                    prompt_content = fi.read()
                    filename = os.path.basename(file)
                    name_only, _ = os.path.splitext(filename)
                    prompts[name_only] = prompt_content      
                    logger.debug(f"Add prompt_template {name_only}")
        return prompts
    
