import asyncio

from typing import Any
from uuid import uuid4

import httpx

from a2a.client import A2AClient
from a2a.types import (
    MessageSendParams,
    SendStreamingMessageRequest,
)


def print_welcome_message() -> None:
    print('Welcome to the generic A2A client!')
    print("Please enter your query (type 'exit' to quit):")


def get_user_query() -> str:
    return input('\n> ')


async def interact_with_server(client: A2AClient) -> None:
    while True:
        user_input = get_user_query()
        user_input = f"Search {user_input}"
        if user_input.lower() == 'exit':
            print('bye!~')
            break

        send_message_payload: dict[str, Any] = {
            'message': {
                'role': 'user',
                'parts': [{'type': 'text', 'text': user_input}],
                'messageId': uuid4().hex,
            },
        }

        try:
            streaming_request = SendStreamingMessageRequest(
                id=uuid4().hex,
                params=MessageSendParams(**send_message_payload)
            )
            stream_response = client.send_message_streaming(streaming_request)
            async for chunk in stream_response:
                print(get_response_text(chunk), end='', flush=True)
                await asyncio.sleep(0.1)
        except Exception as e:
            print(f'An error occurred: {e}')


def get_response_text(chunk):
    data = chunk.model_dump(mode='json', exclude_none=True)
    return data['result']['artifact']['parts'][0]['text']


async def main() -> None:
    print_welcome_message()
    async with httpx.AsyncClient(verify=False) as httpx_client:
        client = A2AClient(httpx_client=httpx_client, url="<url>/searchagent")
        # client = await A2AClient.get_client_from_agent_card_url(
        #     httpx_client, 'http://localhost:9998'
        # )
        await interact_with_server(client)


if __name__ == '__main__':
    asyncio.run(main())
