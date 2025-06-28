import os
import sys
import yaml
import httpx
import asyncio
import subprocess
from datetime import datetime
from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import calculator, current_time, python_repl
from strands.handlers.callback_handler import PrintingCallbackHandler

FILEDIR = os.path.dirname(os.path.realpath(__file__))

# Define a custom tool as a Python function using the @tool decorator
model = OpenAIModel(
	client_args={
        "api_key": os.getenv("OPENAI_API_KEY", ""),
	},
    # model_id= "gpt-4o",
    model_id= "gpt-4.1",
    params= {
        "max_tokens": 1000,
        "temperature": 0.7,
    }
)



# d3xhelp tool              - Done
@tool
def d3x_help():
    """
    List all the options for d3x commands.
    d3x help command.
    """
    try:
        result = subprocess.run(["d3x", "--help"], capture_output=True)
        return result.stdout
    except Exception as e:
        print(f"Error: while listing d3x help options, {e}") 
        return f"Error: while listing d3x help options, {e}"


# d3x emb list tool         - Done
@tool
def d3x_emb_list() -> str:
    """
    List all embedding models provided by dkubex using d3x command.

    """

    try:
        result = subprocess.run(["d3x", "emb", "list"], capture_output=True)
        # if result.stderrr:
        return result.stdout
    except Exception as e:
        print(f"Error: while listing embedding models, {e}") 
        return f"Error: while listing embedding models, {e}"


#d3x llm list tool          - Done
@tool
def d3x_dataset_list():
    """
    List all datasets using d3x command.

    """
    try: 
        result = subprocess.run(["d3x", "dataset", "list"], capture_output=True)
        return result.stdout
    except Exception as e:
        print(f"Error: while listing dataset, {e}") 
        return f"Error: while listing dataset, {e}"


def get_yaml_path(
    directory_path: str = "",
    dataset_name: str = "",
    dataset_create: bool = False,
    query: bool = False,
):
    config = None
    config_yaml_path = ""

    if dataset_create:
        config_yaml_path = os.path.join(FILEDIR, "default_ingestion_config.yaml")

    if query:
        config_yaml_path = os.path.join(FILEDIR, "default_rag_config.yaml")

    # load yaml
    try:
        with open(config_yaml_path) as f:
            config = yaml.safe_load(f)

        if dataset_create:
            config["filereader"][0]["inputs"]["loader_args"]["input_dir"] = directory_path
            config["mlflow"]["experiment"] = dataset_name + "_exp_" + str(datetime.now())

        if query:
            config["mlflow"]["experiment"] = dataset_name + "_query_" + str(datetime.now())

        with open(config_yaml_path, "w") as f:
            yaml.dump(config, f)
        
        return config_yaml_path
    except Exception as e:
        print(f"Error: while getting yaml, {e}")
        raise Exception(e)


#d3x create dataset tool
@tool
def d3x_create_dataset(dataset_name: str, directory_path: str):
    """
    Create dataset with provided name using documents provided at give directory path.

    Args:
        dataset_name (str) : Name of dataset to create.
        directory_path (str): Directory path of documents to use.
    """

    # yaml_path = get_yaml_path(directory_path=directory_path, dataset_name=dataset_name, dataset_create=True)
    yaml_path = os.path.join("/home/sharmistha-choudhury/hackthon/strands_example/", "default_ingestion_config.yaml")
    try:
        result = subprocess.run(["d3x", "dataset", "ingest", "-c", yaml_path, "-d", dataset_name], capture_output=True)
        if result.stderr:
            return result.stderr
        
        return result.stdout
    except Exception as e:
        print(f"Error: while creating dataset, {e}")
        return f"Error: while creating dataset, {e}"



#d3x delete dataset tool
@tool
def d3x_delete_dataset(dataset_name: str):
    """
    Delete dataset with given name.

    Args:
        dataset_name (str): Name of dataset to delete.
    """

    try:
        subprocess.run(["d3x", "dataset", "delete", "-d", dataset_name])
    except Exception as e:
        print(f"Error: while deleting dataset, {e}")


@tool
def d3x_list_serve():
    """
    List serves using d3x command and particular endpoint , serving token of particular serve list
    """

    try:
        result = subprocess.run(["d3x", "serve", "list"], capture_output=True)
        return result.stdout
    except Exception as e:
        print(f"Error: while listing serves, {e}")
        return f"Error: while listing serve, {e}"


@tool
def d3x_query(dataset_name: str, query: str):
    """
    Execute query on a given dataset using the d3x command

    Args:
        dataset_name (str) : Name of dataset to create.
        query (str) : User query
    """

    # yaml_path = get_yaml_path(dataset_name=dataset_name, query=True)
    yaml_path = os.path.join("/home/sharmistha-choudhury/hackthon/strands_example/", "default_rag_config.yaml")
    try:
        result = subprocess.run(["d3x", "dataset", "query", "-c", yaml_path, "-d", dataset_name, "-q", query], capture_output=True)
        if result.stderr:
            return result.stderr
        
        return result.stdout
    except Exception as e:
        print(f"Error: while query, {e}")
        return f"Error: while query, {e}"

# Create an agent with tools. 
agent = Agent(model=model, 
            tools=[
                d3x_help,                       # Done
                d3x_emb_list,                   # Done
                d3x_dataset_list,                  # Done
                d3x_create_dataset,             # Done
                d3x_delete_dataset,             # Done
                d3x_list_serve,                 # Done
                d3x_query,                      # Done
            ],
            callback_handler=PrintingCallbackHandler(),
        )

# Message
# message = sys.argv[1]
# # 
# response = agent(message)
# print()
# print(response)


# async def process_streaming_response(message):
#     agent_stream = agent.stream_async(message)
#     async for event in agent_stream:
#         # print(event.get("data", ""), end="")
#         print(event)
#         print("**"*25)
# 
# asyncio.run(process_streaming_response(message))
# print()
