from rasa.core.policies import KerasPolicy, MemoizationPolicy, FallbackPolicy, FormPolicy, MappingPolicy
from rasa.core.agent import Agent
import asyncio


async def main():
    # there is a threshold for the NLU predictions as well as the action predictions
    agent = Agent('domain.yml', policies=[KerasPolicy(epochs=100, max_history=6),
                                          FallbackPolicy(fallback_action_name='action_default_fallback'),
                                          MemoizationPolicy(max_history=5),
                                          FormPolicy(),
                                          MappingPolicy()])

    # loading our neatly defined training dialogues
    training_data = await agent.load_data('data/stories/')

    agent.train(
        training_data,
        validation_split=0.0,
        verbose=True,
        debug=True
    )

    agent.persist('models/')


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
