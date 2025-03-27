import asyncio

from apscheduler.schedulers.background import BackgroundScheduler

from ambientagi.services.openai_agent_wrapper import AmbientAgentServiceExtended


def get_weather(city: str) -> str:
    """
    Returns a hardcoded weather string for the specified city.
    In a real-world scenario, you'd query a weather API here.
    """
    return f"The weather in {city} is sunny with a light breeze."


async def main():
    # 1. Your OpenAI API key
    my_api_key = "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"

    # 2. Start a scheduler (needed only if you want to schedule recurring tasks).
    scheduler = BackgroundScheduler()
    scheduler.start()

    # 3. Create the extended AmbientAgentService
    service = AmbientAgentServiceExtended(api_key=my_api_key, scheduler=scheduler)

    # 4. Create an agent that’s encouraged to call `get_weather`
    service.create_openai_agent(
        name="WeatherAgent",
        instructions=(
            "You are a weather-savvy agent. "
            "When asked about the weather, call the tool 'get_weather' with the city name. "
            "After receiving the tool's response, provide the final answer."
        ),
    )

    # 5. Register our Python function as a tool
    service.openai_wrapper.add_function_tool("WeatherAgent", get_weather)

    # 6. Run the agent asynchronously with a prompt
    prompt = "What is the weather in London right now?"
    result = await service.run_openai_agent_async("WeatherAgent", prompt)
    print("Final agent output:", result)

    # 7. Shutdown the scheduler if you’re done (otherwise leave it running).
    scheduler.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
