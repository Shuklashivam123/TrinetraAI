from agent import get_agent

agent = get_agent("openai/gpt-oss-120b")

config = {
    "configurable": {
        "thread_id": "thread1"
    }
}

for event in agent.stream(
    {
        "messages": [
            ("user", "Mahakal ke baare me bata bhai? Unke kitne naam hai?")
        ]
    },
    config=config,
    stream_mode="values"
):
    event["messages"][-1].pretty_print()