import os 
from dotenv import load_dotenv

# Remove overide if you want sys level ENV VARS to overide the config,
# which is standard behavior
load_dotenv(override=True)

host = os.environ.get("IRIS_HOST")
db = os.environ.get("DATABASE")
user = os.environ.get("IRIS_USER")
pwd = os.environ.get("IRIS_PWD")
port = os.environ.get("IRIS_PORT")

server_local = {
    "name": "Local",
    "dialect": "iris",
    "database": db,
    "host": host,
    "password": pwd,
    "user": user,
    "port": port,
    "schemas": ['SQLUser'],
    "type": "alchemy"
}
backend_db = {
    "name": "Backend",
    "dialect": "sqlite",
    "database": db,
    "host": host,
    "password": pwd,
    "user": user,
    "port": port,
    "schemas": [],
}

config = {
    "servers": [
        {
            "name": "test",
            "dialect": "sqlite",
            "database": "/temp/test.db",
            "schemas": [],
            "type": "sqlite"
        },
        server_local,
    ],
    "src_server": "Local",
    "back_end_db": "Local",
    "default_llm": "openai",
    "llms": [
        {"name": "openai",
         "api": "chat.completions",
         "api_key": os.environ.get("OPENAI_API_KEY"),
         "params": { 
             "model": "gpt-4o-mini",
             "temperature": 0,
             "top_p" : .2,
             "seed": 497,
             "max_completion_tokens": 20
         }
        }
    ],
    "workflow": {
        "name": "echo",
        "actions": ['execute_sql', 'execute_scalar_sql', 'summary'],
        "active_workflow": "workflow_echo",
        "prompt_template": ""
    },
    "prompt_dir": "src/assistr/prompts"
}