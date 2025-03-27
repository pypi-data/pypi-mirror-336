# ambientagi/providers/telegram_provider.py
# ambientagi/providers/async_telegram_provider.py

import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Optional, Set

import requests


class TelegramProvider:
    """
    A Telegram bot provider built for asynchronous usage:
    - Uses asyncio loop in run_async()
    - Invokes requests.* in a non-blocking way via asyncio.to_thread().
    """

    BASE_URL = "https://api.telegram.org"

    def __init__(
        self,
        agent_info: Dict[str, Any],
        bot_token: str,
        mentions: Optional[Set[str]] = None,
    ):
        """
        :param agent_info: Info about the agent (e.g., name).
        :param bot_token: Telegram bot token from BotFather.
        :param mentions: If not None, we only process messages containing these mentions.
        """
        self.agent_info = agent_info
        self.bot_token = bot_token
        self.mentions = mentions
        self.last_update_id = 0
        self.last_chat_id: Optional[str] = None

        # We'll allow the user to set or override this with an async callback
        # signature: (user_id: str, message: str, chat_id: str, **kwargs) -> Awaitable[None]
        # The callback itself can call an LLM or do other logic
        self.on_message: Optional[Callable[..., Awaitable[None]]] = None

    async def send_message_async(
        self, text: str, chat_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Asynchronously send a message to Telegram via requests, run in a thread.
        """
        if chat_id is None:
            if self.last_chat_id is None:
                raise ValueError("No chat ID available to send_message_async().")
            chat_id = self.last_chat_id

        url = f"{self.BASE_URL}/bot{self.bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}

        def blocking_post():
            return requests.post(url, json=payload, timeout=10)

        # Run the blocking call in a thread pool:
        response = await asyncio.to_thread(blocking_post)
        try:
            return response.json()
        except Exception as e:
            return {"ok": False, "description": str(e)}

    async def get_updates_async(self, timeout: int = 30) -> List[Dict[str, Any]]:
        """
        Asynchronously fetch updates from Telegram, also using requests in a thread.
        """
        url = f"{self.BASE_URL}/bot{self.bot_token}/getUpdates"
        params = {"timeout": timeout, "offset": self.last_update_id + 1}

        def blocking_get():
            return requests.get(url, params=params, timeout=timeout + 5)

        response = await asyncio.to_thread(blocking_get)
        try:
            data = response.json()
            if data.get("ok") and data.get("result"):
                updates = data["result"]
                if updates:
                    self.last_update_id = max(u["update_id"] for u in updates)
                return updates
        except Exception as e:
            print(f"[{self.agent_info['name']}] Error parsing updates: {e}")
        return []

    async def process_updates_async(self) -> None:
        """
        Fetch new updates and process them asynchronously.
        If we detect a mention (or we process all messages), call self.on_message if set.
        """
        updates = await self.get_updates_async()
        for update in updates:
            message = update.get("message", {})
            chat_id = str(message.get("chat", {}).get("id", ""))
            user_id = str(message.get("from", {}).get("id", ""))
            text = message.get("text", "")

            if not chat_id or not text:
                continue

            self.last_chat_id = chat_id

            if self.should_process_message(text):
                if self.on_message:
                    # on_message is an async callback, so we await it
                    await self.on_message(user_id, text, chat_id)
                else:
                    # If no callback, default aggregator response
                    fallback = f"Caught a mention in '{text}'! How can {self.agent_info['name']} help?"
                    await self.send_message_async(fallback)
            else:
                print(
                    f"[{self.agent_info['name']}] Ignored: {text} (no matching mention)"
                )

    def should_process_message(self, text: str) -> bool:
        """
        If mentions is None, we process all. Otherwise we look for any mention in text.
        """
        if self.mentions is None:
            return True
        lower_text = text.lower()
        return any(m.lower() in lower_text for m in self.mentions)

    async def run_async(
        self, poll_interval: float = 1.0, error_delay: float = 5.0
    ) -> None:
        """
        Asynchronously poll for updates in a loop.
        """
        mode = "all messages" if self.mentions is None else f"mentions {self.mentions}"
        print(f"[{self.agent_info['name']}] Starting async bot listener ({mode})...")

        while True:
            try:
                await self.process_updates_async()
                await asyncio.sleep(poll_interval)
            except asyncio.CancelledError:
                print(f"[{self.agent_info['name']}] Cancelled. Stopping bot.")
                break
            except Exception as e:
                print(f"[{self.agent_info['name']}] Error in run loop: {e}")
                await asyncio.sleep(error_delay)


# Example usage
# if __name__ == "__main__":
#     # Case 1: User wants only @BONZI or @bonzi mentions
#     agent_info = {"name": "BonziBot"}
#     bot_token = "7838344151:AAFf7ds7XmiKn2tSGrGilP_x8DiTcGaxRAg"  # Replace with your bot token
#     mentions = {"@BONZI", "@bonzi"}  # Custom mentions for this user
#     bonzi_bot = TelegramProvider(agent_info, bot_token, mentions)
#     bonzi_bot.run()

#     # Case 2: User wants all messages
#     agent_info_all = {"name": "AllChatBot"}
#     all_bot = TelegramProvider(agent_info_all, bot_token, mentions=None)
#     # all_bot.run()
