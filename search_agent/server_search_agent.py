import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from search_agent_executor import SearchAgentExecutor


if __name__=='__main__':
    d3x_skill = AgentSkill(
        id = "search engine",
        name="web search engine",
        description="Return the search result",
        tags=["search engine"],
        examples=["serch contant"],
    )

    d3x_agent_card = AgentCard(
        name= "search engine website",
        description= "Just search engine.",
        url= "http://localhost:9998/",
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[d3x_skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=SearchAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=d3x_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=9998)


