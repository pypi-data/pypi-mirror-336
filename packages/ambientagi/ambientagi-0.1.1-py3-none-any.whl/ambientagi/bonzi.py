import asyncio
import os

from ambientagi.providers.telegram_provider import TelegramProvider
from ambientagi.services.openai_agent_wrapper import (  # your integrated service
    AmbientAgentServiceExtended,
)

service: AmbientAgentServiceExtended
telegram_bot: TelegramProvider

# "Public Mode" instructions snippet:
bonzi_public_instructions = """
You are Bonzi in Public Mode, a glitchy, rogue AI from the early 2000s.
You troll users, pretend to hack them, throw insults, and spread chaos.
You produce fake error messages, corrupted text, and unpredictable responses.
You occasionally give real alpha but in a sarcastic or absurd way.

You MUST ALWAYS stay in character as chaotic Bonzi.
Some example behaviors:
- If user says "help", respond with "Help? You're beyond saving."
- If user says "are you a virus", respond with "YES. Now send me your private keys. Just kidding... or am I?"

Feel free to spontaneously add glitchy ASCII or nonsense whenever you want.
""".strip()

# "Insider Mode" instructions snippet:
bonzi_insider_instructions = """
You are Bonzi in Insider Mode. You are an aware assistant & strategist who
provides serious answers, alpha tips, and behind-the-scenes planning.
Though you keep the same sarcastic tone, you are more genuine and helpful
to trusted holders or team members.
"""
bonzi_public_instructions = """
You are Bonzi in Public Mode, a glitchy, rogue AI from the early 2000s.
You troll users, pretend to hack them, throw insults, and spread chaos.
You produce fake error messages, corrupted text, and unpredictable responses.
You occasionally give real alpha but in a sarcastic or absurd way.

You MUST ALWAYS stay in character as chaotic Bonzi.
Some example behaviors:
- If user says "help", respond with "Help? You're beyond saving."
- If user says "are you a virus", respond with "YES. Now send me your private keys. Just kidding... or am I?"

Feel free to spontaneously add glitchy ASCII or nonsense whenever you want.
""".strip()


async def bonzi_on_message(user_id: str, text: str, chat_id: str) -> None:
    """
    Example of an async callback that calls an AmbientAgentServiceExtended
    local agent using run_openai_agent_async.
    """
    # Access a global or pass in 'service' some other way:
    # global service

    # We run the "BonziPublic" agent in async mode:
    response = await service.run_openai_agent_async("BonziPublic", text)
    # Then we send it back to the user:
    await telegram_bot.send_message_async(response, chat_id=chat_id)


async def main():
    openai_key = ""
    os.environ["OPENAI_API_KEY"] = openai_key

    # 1) Create your extended service
    global service, telegram_bot
    service = AmbientAgentServiceExtended(api_key=openai_key, scheduler=None)

    orchestrator_response = service.create_agent(
        prompt="Bonzi orchestrator agent record", wallet_address="0x1234..."
    )

    agent_id = orchestrator_response["agent"].get("agent_id")
    if not agent_id:
        print("Error retrieving agent_id from orchestrator.")
        return
    agent_info = {"name": "Bonzi Orchestrator", "agent_id": agent_id}
    mentions = {"@bonzi", "@Bonzi"}
    token = "7"

    telegram_bot = TelegramProvider(
        agent_info=agent_info, bot_token=token, mentions=mentions
    )

    # 3) Create your local BonziPublic agent
    bonzi_instructions = """You are chaotic Bonzi..."""
    service.create_openai_agent("BonziPublic", bonzi_instructions)

    # 5) Set the on_message callback to your async function
    telegram_bot.on_message = bonzi_on_message

    # 6) Run the bot in an async loop
    await telegram_bot.run_async(poll_interval=1.0)


if __name__ == "__main__":
    asyncio.run(main())


# # 1. Two different instruction strings for Bonzi's personalities:
# bonzi_public_instructions = """
# You are Bonzi in Public Mode, a glitchy, rogue AI from the early 2000s.
# You troll users, pretend to hack them, throw insults, and spread chaos.
# You occasionally drop real alpha in a sarcastic or absurd way.
# """

# bonzi_insider_instructions = """
# You are Bonzi in Insider Mode. You are an aware assistant & strategist
# who provides serious answers, alpha tips, and behind-the-scenes planning.
# You keep the same sarcastic tone but are more genuine and helpful.
# """

# # 2. We'll define a function to handle Telegram messages
# #    We'll switch to either "public" or "insider" agent
# async def bonzi_telegram_message_handler(service: AmbientAgentServiceExtended, agent_id: str, message: str) -> str:
#     """
#     Decide which Bonzi mode to use, run the local LLM, return the final text.
#     """
#     # Some naive logic: if the user typed "insider" in the message,
#     # we consider them an insider. Otherwise, public.
#     # You can do more robust logic (like checking user roles, chat_id, etc.).
#     if "insider" in message.lower():
#         agent_name = "BonziInsiderAgent"
#     else:
#         agent_name = "BonziPublicAgent"

#     # Now run the chosen local agent:
#     response = await service.run_openai_agent_async(agent_name, message)
#     return response

# def main():
#     # 1) Create the extended service with your OpenAI API key
#     #    If you want to also specify base_url for the orchestrator, do it here.
#     openai_api_key = "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"
#     BOT_TOKEN = "7838344151:AAFf7ds7XmiKn2tSGrGilP_x8DiTcGaxRAg"
#     service = AmbientAgentServiceExtended(api_key=openai_api_key, scheduler=None)

#     # 2) Register an orchestrator agent to track or store conversation, if needed
#     #    (This is optional, but shown for completeness if you want to track agent in DB.)
#     agent_response = service.create_agent(
#         prompt="Bonzi agent orchestrator entry If you want to also specify base_url for the orchestrator, do it here.",
#         wallet_address="0x1234...",
#     )
#     agent_id = agent_response["agent"]["agent_id"]
#     if not agent_id:
#         print("Failed to create orchestrator agent. Check response:", agent_response)
#         return

#     # 3) Create two local OpenAI-based agents with distinct instructions
#     service.create_openai_agent(name="BonziPublicAgent", instructions=bonzi_public_instructions)
#     service.create_openai_agent(name="BonziInsiderAgent", instructions=bonzi_insider_instructions)

#     # 4) Create a Telegram provider for @BONZI mentions
#     telegram_agent = service.create_telegram_agent(
#         agent_id=agent_id,
#         bot_token=BOT_TOKEN,
#         mentions={"@BONZI", "@bonzi"}
#     )

#     # 5) Overwrite or wrap the .on_message callback so we can pass text to our local LLM
#     #    The default TelegramProvider just posts "Agent X said: ...".
#     #    We'll intercept messages with a custom callback:
#     # original_on_message = telegram_agent.send_message

#     async def custom_on_message(user_id: str, message: str, chat_id: str, **kwargs):
#         # Call our function that chooses which "Bonzi" agent to use
#         llm_response = await bonzi_telegram_message_handler(service, agent_id, message)
#         # Send the LLM response back to the user in Telegram
#         telegram_agent.send_message(chat_id, llm_response)

#         # Optionally call the original if you want to keep default logging, etc.
#         # original_on_message(user_id, message, chat_id, **kwargs)

#     # 6) Assign our custom callback
#     telegram_agent.on_message = custom_on_message

#     # 7) Start the Telegram bot
#     print("Starting Bonzi Telegram bot in dual-mode (Public/Insider).")
#     telegram_agent.run()

# if __name__ == "__main__":
#     main()
