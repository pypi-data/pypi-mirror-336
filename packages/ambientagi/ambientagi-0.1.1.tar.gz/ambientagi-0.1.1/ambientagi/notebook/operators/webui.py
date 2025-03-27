# user_code.py
from ambientagi.services.agent_service import AmbientAgentService

# 1) Create a new agent
service = AmbientAgentService()
# resp = service.create_agent(
#     prompt="A browser agent named Broswy to help crypto enthusiasts surf the internet for market trends and news",
#     wallet_address="0x123",
# )
# agent_id = resp["agent"]["agent_id"]
# print("Created agent:", agent_id)

# 2) Launch the WebUI with that agent_id
webui_agent = service.add_webui_agent(agent_id="6e62aece-630b-4596-a9a9-5ed896ff4bbd")
webui_agent.launch()  # This will parse command line args or just run on default IP/port
