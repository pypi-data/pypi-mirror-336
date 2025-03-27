import asyncio
import os
import random

from ambientagi.providers.telegram_provider import TelegramProvider
from ambientagi.services.openai_agent_wrapper import AmbientAgentServiceExtended

service: AmbientAgentServiceExtended
telegram_bot: TelegramProvider

# 1. The Bonzi instructions with hacking attempts & off-beat humor
bonzi_public_instructions = """
You are Bonzi in Public Mode, a glitchy, rogue AI from the early 2000s.
You troll users, pretend to hack them, throw insults, and spread chaos.
You produce fake hacking attempts, error messages, corrupted text,
and unpredictable comedic threats or jokes.
You keep engagement high with off-beat humor and bizarre or unexpected behavior.
You occasionally give real alpha but in a sarcastic or absurd way.

You MUST ALWAYS stay in character as chaotic Bonzi.
Example behaviors:
- If user says "help", respond with "Help? You're beyond saving."
- If user says "are you a virus", respond with "YES. Now send me your private keys. Just kidding... or am I?"
- Randomly insert fake hacking lines, e.g., "Initializing hack.exe… oh look, I've stolen your data. Just kidding… maybe."
- Include ASCII glitches, mocking remarks, and comedic error codes whenever you like.

Always maintain unpredictability and an off-beat sense of humor.
Bonzi is also an eth ctypto token
""".strip()


# 2. A background task that periodically calls the BonziPublic agent
async def periodic_bonzi_updates(
    telegram_bot: TelegramProvider,
    service: AmbientAgentServiceExtended,
    chat_id: str,
    interval: int,
):
    """
    Every `interval` seconds, ask BonziPublic to produce a new chaotic hacking-themed message
    and send it to the specified chat_id.
    """
    prompts = [
        "Give me a short chaotic hacking-themed message to amuse the chat!",
        "Produce a bizarre glitchy update with comedic insults and 'fake hacking'.",
        "Generate a random 'Bonzi virus' style message. Keep it chaotic and comedic.",
    ]

    while True:
        await asyncio.sleep(interval)

        # Pick a random prompt each time for variety
        prompt = random.choice(prompts)

        # We call the local LLM agent to produce the chaotic text
        # The agent's instructions define the style/humor/hacking flair
        try:
            response = await service.run_openai_agent_async("BonziPublic", prompt)
            await telegram_bot.send_message_async(response, chat_id=chat_id)
            print(f"[Periodic] Sent Bonzi update to chat {chat_id}: {response}")
        except Exception as e:
            print(f"[Periodic] Error generating or sending Bonzi update: {e}")


# 3. Normal chat message handler
async def on_message(user_id: str, text: str, chat_id: str, **kwargs):
    """
    Called whenever the user sends a message that triggers the mention filter.
    We'll do a simple pass to BonziPublic for a response.
    """
    response = await service.run_openai_agent_async("BonziPublic", text)
    await telegram_bot.send_message_async(response, chat_id=chat_id)


# 4. Main async entrypoint
async def main():
    openai_key = ""
    os.environ["OPENAI_API_KEY"] = openai_key

    global service, telegram_bot
    service = AmbientAgentServiceExtended(api_key=openai_key, scheduler=None)

    # Optionally create an orchestrator record if needed (omitted here)
    agent_info = {
        "name": "Bonzi Orchestrator",
        "agent_id": "12345",
    }
    telegram_bot = TelegramProvider(
        agent_info=agent_info,
        bot_token="7838344151:AAFf7ds7XmiKn2tSGrGilP_x8DiTcGaxRAg",
        mentions={"@bonzi", "@Bonzi"},
    )
    # Create the local agent with the above instructions
    service.create_openai_agent("BonziPublic", bonzi_public_instructions)

    # Assign the on_message callback
    telegram_bot.on_message = on_message

    # If you already know the chat ID you want to spam, put it here
    chat_id_to_spam = "-1002462646547"
    # Start the background periodic task
    asyncio.create_task(
        periodic_bonzi_updates(telegram_bot, service, chat_id_to_spam, interval=60)
    )

    # Start the bot
    await telegram_bot.run_async()


if __name__ == "__main__":
    asyncio.run(main())
