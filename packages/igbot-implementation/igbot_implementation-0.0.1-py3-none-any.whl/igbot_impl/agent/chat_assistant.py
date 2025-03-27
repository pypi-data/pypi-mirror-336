from igbot_impl.igbot_impl.agent import Agent
from igbot_base.igbot_base.agent_response import AgentResponse
from igbot_base.igbot_base.llm import Llm
import asyncio


class ChatAssistant(Agent):
    # todo: change it
    def __init__(self,
                 agent_id,
                 main_llm: Llm,
                 async_delegate: Agent):
        self.__id = agent_id
        self.__llm = main_llm
        self.__delegate_assistant = async_delegate

    async def invoke(self, query) -> AgentResponse:
        links_response = asyncio.create_task(self.get_links(query))
        chat_response = self.__llm.call(query, {})
        await links_response
        links_message = links_response.result()
        if links_message.is_successful():
            return AgentResponse.success(chat_response + "\n\n" + links_message.get_response())
        return AgentResponse.success(chat_response)

    async def get_links(self, query):
        return self.__delegate_assistant.invoke(query)
