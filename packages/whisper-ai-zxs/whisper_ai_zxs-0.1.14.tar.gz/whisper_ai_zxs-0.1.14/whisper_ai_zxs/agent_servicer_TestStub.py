import logging

#from .resources.agent_servicer import AgentServicer
from .agent_servicer import AgentServicer

class Agent_TestStub(AgentServicer):
    def call(self, name, *args, **kwargs):
        logging.debug(f"开始执行Agent函数：{name}，参数：{args}")
        return "success"
