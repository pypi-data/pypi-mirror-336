from igbot_impl.igbot_impl.agent import Agent
from igbot_base.igbot_base.agent_response import AgentResponse
from igbot_base.igbot_base.llm import Llm


class ChatAssistantTODO(Agent):
    # todo: change it
    def __init__(self,
                 agent_id,
                 main_llm: Llm):
        self.__id = agent_id
        self.__llm = main_llm

    def invoke(self, query) -> AgentResponse:
        chat_response = self.__llm.call(query, {})
        if chat_response == "":
            return AgentResponse.error(" :(", None)
        return AgentResponse.success(chat_response)

