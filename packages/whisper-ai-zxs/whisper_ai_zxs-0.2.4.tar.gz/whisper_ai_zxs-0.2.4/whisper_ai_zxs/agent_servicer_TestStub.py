import logging

#from .resources.agent_servicer import AgentServicer
from .agent_servicer import AgentServicer
logger_whisper = logging.getLogger("whisper_ai")

class Agent_TestStub(AgentServicer):
    def call(self, name, *args, **kwargs):
        logger_whisper.debug(f"开始执行Agent函数：{name}，参数：{args}")
        return "success"
