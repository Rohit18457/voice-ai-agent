from typing import List, Dict
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, DEFAULT_SYSTEM_PROMPT


class ConversationalAgent:
    """
    Dialogue manager and LLM reasoning agent powered by Groq.
    Maintains a sliding window of multi-turn conversation context.
    """

    def __init__(
        self,
        model: str = GROQ_MODEL,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        max_history_turns: int = 6
    ):
        self.model = model
        self.system_prompt = system_prompt
        self.max_history_turns = max_history_turns
        self.client = Groq(api_key=GROQ_API_KEY)

        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]

    def add_user_message(self, content: str):
        """Append user turn to history."""
        self.messages.append({"role": "user", "content": content})
        self._prune_history()

    def add_assistant_message(self, content: str):
        """Append assistant response to history."""
        self.messages.append({"role": "assistant", "content": content})
        self._prune_history()

    def generate_response(self) -> str:
        """
        Request chat completion from Groq LPUs.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            temperature=0.7,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()

    def _prune_history(self):
        """
        Keep system prompt + last N dialogue turns to prevent token bloat.
        """
        system_message = self.messages[0]
        conversation_turns = self.messages[1:]
        max_messages = self.max_history_turns * 2

        if len(conversation_turns) > max_messages:
            self.messages = [system_message] + conversation_turns[-max_messages:]

    def clear_history(self):
        """Reset conversation history back to initial system prompt."""
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def get_history(self) -> List[Dict[str, str]]:
        """Return current conversation messages."""
        return list(self.messages)
