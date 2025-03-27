from agents import Agent, Runner, function_tool

from ambientagi.services.agent_service import AmbientAgentService


class OpenAIAgentWrapper:
    def __init__(self, api_key, scheduler=None):
        # Assume you set openai.api_key = api_key or use environment variables
        self.agents = {}
        self.scheduler = scheduler

    def create_agent(self, name: str, instructions: str) -> Agent:
        agent = Agent(name=name, instructions=instructions)
        self.agents[name] = agent
        return agent

    def run_agent(self, agent_name: str, input_text: str) -> str:
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        result = Runner.run_sync(agent, input_text)
        return result.final_output

    async def run_agent_async(self, agent_name: str, input_text: str) -> str:
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        result_obj = await Runner.run(agent, input_text)
        return result_obj.final_output

    def add_function_tool(self, agent_name: str, func):
        agent = self.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")

        # Directly decorate `func` with function_tool.
        # This ensures the function signature is used to generate a valid JSON schema.
        decorated_func = function_tool(func)
        agent.tools.append(decorated_func)

    def schedule_agent(self, agent_name: str, input_text: str, interval: int):
        if self.scheduler is None:
            raise ValueError("Scheduler is not set.")

        def run_task():
            output = self.run_agent(agent_name, input_text)
            print(f"[Scheduled Output from '{agent_name}']: {output}")

        self.scheduler.add_job(
            job_id=f"openai_agent_{agent_name}",
            func=run_task,
            trigger="interval",
            seconds=interval,
        )
        print(f"Agent '{agent_name}' scheduled to run every {interval} seconds.")


class AmbientAgentServiceExtended(AmbientAgentService):
    def __init__(self, api_key, scheduler):
        super().__init__(scheduler=scheduler)
        self.openai_wrapper = OpenAIAgentWrapper(api_key=api_key, scheduler=scheduler)

    def create_openai_agent(self, name: str, instructions: str):
        return self.openai_wrapper.create_agent(name, instructions)

    async def run_openai_agent_async(self, agent_name: str, input_text: str):
        agent = self.openai_wrapper.agents.get(agent_name)
        if not agent:
            raise ValueError(f"Agent '{agent_name}' not found.")
        result_obj = await Runner.run(agent, input_text)
        return result_obj.final_output

    def schedule_openai_agent(self, agent_name: str, input_text: str, interval: int):
        self.openai_wrapper.schedule_agent(agent_name, input_text, interval)
