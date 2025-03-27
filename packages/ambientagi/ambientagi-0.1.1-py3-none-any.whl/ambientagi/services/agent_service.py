from typing import Any, Dict, Optional, Set

from ambientagi.providers.email_provider import EmailProvider
from ambientagi.providers.telegram_provider import TelegramProvider
from ambientagi.services.ambient_blockchain import BlockchainService
from ambientagi.services.ambient_browser import BrowserAgent
from ambientagi.services.ambient_firecrawl import AmbientFirecrawl
from ambientagi.services.scheduler import AgentScheduler
from ambientagi.services.twitter_service import TwitterService
from ambientagi.services.webui_agent import WebUIAgent
from ambientagi.utils.http_client import HttpClient


class AmbientAgentService:
    DEFAULT_BASE_URL = (
        "http://insight-md-docker.eba-gen8ppse.eu-west-1.elasticbeanstalk.com"
    )

    def __init__(
        self,
        base_url: Optional[str] = None,
        scheduler: Optional[AgentScheduler] = None,
    ):
        """
        Initialize the AmbientAgentService with a centralized HTTP client for the main orchestrator.
        """
        default_headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self.client = HttpClient(
            base_url=base_url or self.DEFAULT_BASE_URL,
            default_headers=default_headers,
        )
        self.scheduler = scheduler

    def create_agent(
        self,
        prompt: str,
        wallet_address: str,
        twitter_handle: Optional[str] = None,
        twitter_id: Optional[str] = None,
    ):
        """
        Create an agent in the orchestrator.

        :param prompt: The prompt to initialize the agent.
        :param wallet_address: The wallet address associated with the agent.
        :param task: A description of what the agent is supposed to do (used for registration only).
        :return: Response from the orchestrator API.
        """
        payload = {
            "prompt": prompt,
            "wallet_address": wallet_address,
            "twitter_handle": twitter_handle,
            "twitter_id": twitter_id,
        }
        response = self.client.post("/ambient-agents/create", data=payload)

        return response

    def update_agent(self, agent_id: str, data: dict) -> Dict[str, Any]:
        """
        POST /ambient-agents/{agent_id}/update
        Content-Type: application/json
        """
        headers = {"Content-Type": "application/json"}  # Override for JSON content
        # Use kwargs directly as the payload
        payload = data

        # Use f-string to dynamically inject the agent_id into the URL
        return self.client.post(
            f"/ambient-agents/{agent_id}/update", json=payload, headers=headers
        )

    def chat_with_agent(
        self, agent_id: str, message: str, wallet_address: str, **kwargs
    ) -> Dict[str, Any]:
        """
        POST /ambient-agents/{agent_id}/chat
        Content-Type: application/x-www-form-urlencoded
        """
        # Payload as form data (not JSON)
        payload = {"message": message, "wallet_address": wallet_address}
        payload.update(kwargs)  # Add any additional parameters dynamically

        return self.client.post(f"/ambient-agents/{agent_id}/chat", data=payload)

    def get_stats(self, agent_id: str) -> Dict[str, Any]:
        """
        GET /ambient-agents/{agent_id}/stats
        """
        return self.client.get(f"/ambient-agents/{agent_id}/stats")

    def get_agent_info(self, agent_id: str) -> Dict[str, Any]:
        """
        GET /ambient-agents/{agent_id}/get
        """
        return self.client.get(f"/ambient-agents/{agent_id}/get")

    def create_browser_agent(self, agent_id: str):
        agent = self.get_agent_info(agent_id)
        return BrowserAgent(agent)

    def create_firecrawl_agent(self, agent_id: str):
        agent = self.get_agent_info(agent_id)
        return AmbientFirecrawl(agent)

    def add_blockchain(self, agent_id: str):
        agent = self.get_agent_info(agent_id)
        return BlockchainService(agent)

    def create_twitter_agent(self, agent_id: str):
        agent = self.get_agent_info(agent_id)
        return TwitterService(agent)

    def schedule_agent(self, agent_id: str, func, interval: int, **kwargs):
        """
        Schedule a task for the agent.
        """
        if self.scheduler is None:
            raise ValueError("Scheduler is not set.")

        job_id = f"agent_{agent_id}"
        self.scheduler.add_job(
            job_id=job_id, func=func, trigger="interval", seconds=interval, **kwargs
        )
        print(f"Agent {agent_id} scheduled every {interval} seconds.")

    def add_webui_agent(
        self,
        agent_id: str,
        config: Optional[Dict[str, Any]] = None,
        theme="Ocean",
        ip="127.0.0.1",
        port=7788,
    ) -> WebUIAgent:
        """
        Creates and returns a WebUIAgent for controlling the browser-based AI interface.
        """
        if config is None:
            from ambientagi.utils.webui.utils.default_config_settings import (
                default_config,
            )

            config = default_config()

        config["agent_id"] = agent_id
        return WebUIAgent(config=config, theme=theme, ip=ip, port=port)

    def create_email_agent(
        self,
        agent_id: str,
        smtp_server: str = "smtp.gmail.com",  # Default to Gmail
        smtp_port: int = 587,  # TLS port
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
    ):
        """
        Instantiate an EmailProvider for the given agent with optional SMTP configuration.
        By default, this is set up for Gmail over TLS on port 587.

        If you're using a Gmail account with two-factor authentication (2FA) enabled,
        you'll need to generate an App Password (see https://myaccount.google.com/security).
        """
        agent_info = self.get_agent_info(agent_id)
        return EmailProvider(
            agent_info=agent_info,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            username=username,
            password=password,
            use_tls=use_tls,
        )

    def create_telegram_agent(
        self,
        agent_id: str,
        bot_token: str,
        mentions: Optional[Set[str]] = None,
    ) -> TelegramProvider:
        """
        Instantiate a TelegramProvider for the given agent with a bot token and optional mention filters.
        """
        agent_info = self.get_agent_info(agent_id)
        return TelegramProvider(
            agent_info=agent_info, bot_token=bot_token, mentions=mentions
        )
