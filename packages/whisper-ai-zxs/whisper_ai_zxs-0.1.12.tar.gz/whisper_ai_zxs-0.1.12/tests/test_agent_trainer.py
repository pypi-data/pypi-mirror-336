
from whisper_ai_zxs.agent_trainer import AgentTrainer
from whisper_ai_zxs.agent_servicer_TestStub import Agent_TestStub
agent = Agent_TestStub("植想说小红书店")
tools1 = AgentTrainer()

tools1.run([agent])
tools1.run([agent])
tools1.run([agent])
tools1.run([agent])
tools1.clear_run()
