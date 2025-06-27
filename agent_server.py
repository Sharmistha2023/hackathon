import uvicorn

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from agent_executor import D3xCommandAgentExecutor


if __name__=='__main__':
    d3x_skill = AgentSkill(
        id = "d3x commands",
        name="Executes d3x commands related to d3x or dkubex.",
        description="Just returns d3x commands output.",
        tags=["d3x commands"],
        examples=["d3x", "d3x --help", "d3x dataset"],
    )

    d3x_agent_card = AgentCard(
        name= "D3x commands agent",
        description= "Just d3x commands agent.",
        url= "http://localhost:9999/",
        version='1.0.0',
        defaultInputModes=['text'],
        defaultOutputModes=['text'],
        capabilities=AgentCapabilities(streaming=True),
        skills=[d3x_skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=D3xCommandAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=d3x_agent_card,
        http_handler=request_handler,
    )

    uvicorn.run(server.build(), host='0.0.0.0', port=9999)


