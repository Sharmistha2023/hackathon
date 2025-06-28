import os
import sys
import httpx
import requests
import asyncio
import subprocess
from bs4 import BeautifulSoup  
from datetime import datetime
from strands import Agent, tool
from strands.models.openai import OpenAIModel
from strands_tools import calculator, current_time, python_repl
from strands.handlers.callback_handler import PrintingCallbackHandler

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


#    Search query and provide url
@tool
def search_engine(query: str) -> str:
    """
    Search query and  strictly provide references.
    
    Args:
        query (str) : User query
    """
    url = "https://html.duckduckgo.com/html/"
    response = requests.post(url, data={"q": query})
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for result in soup.find_all('a', {'class': 'result__a'}):
        title = result.text
        link = result['href']
        results.append(f"- {title}: {link}")
    return "\n".join(results)




agent = Agent(model=model, 
            tools=[
                search_engine,
            ],
            callback_handler=PrintingCallbackHandler(),
        )

# message = f"Search {sys.argv[1]}"
# response = agent(message)
