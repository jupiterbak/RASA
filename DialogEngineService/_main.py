import asyncio
import pprint as pretty_print
from typing import Any, Dict, Text, TYPE_CHECKING
from rasa.cli.utils import print_success, print_error
import rasa.model as model
from rasa.run import create_agent
from rasa.core.agent import Agent


def pprint(object: Any):
    pretty_print.pprint(object, indent=2)


def main():
    """Chat to the bot within a Jupyter notebook.

    Args:
        model_path: Path to a Rasa Stack model.
        agent: Rasa Core agent (used if no Rasa Stack model given).
        interpreter: Rasa NLU interpreter (used with Rasa Core agent if no
                     Rasa Stack model is given).
    """

    agent = Agent.load("models/core")
    print("Your bot is ready to talk! Type your messages here or send '/stop'.")
    loop = asyncio.get_event_loop()
    while True:
        message = input()
        if message == "/stop":
            break

        responses = loop.run_until_complete(agent.handle_text(message))
        for response in responses:
            _display_bot_response(response)


def _display_bot_response(response: Dict):
    for response_type, value in response.items():
        if response_type == "text":
            print_success(value)
        if response_type == "image":
            print_success("Image-->" + value)


if __name__ == "__main__":
    main()
