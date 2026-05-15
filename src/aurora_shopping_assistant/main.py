#!/usr/bin/env python
import sys
import warnings

from aurora_shopping_assistant.crew import AuroraShoppingAssistant

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run(user_message: str = ""):
    """
    Run the crew with a user message.
    
    Args:
        user_message: The user's input message to process
    """
    if not user_message:
        user_message = "Liste os produtos disponíveis"
    
    try:
        result = AuroraShoppingAssistant().crew().kickoff(inputs={"message": user_message})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    try:
        AuroraShoppingAssistant().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs={"message": ""}
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AuroraShoppingAssistant().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


def test():
    """
    Test the crew execution and returns the results.
    """
    try:
        AuroraShoppingAssistant().crew().test(
            n_iterations=int(sys.argv[1]),
            eval_llm=sys.argv[2] if len(sys.argv) > 2 else None,
            inputs={"message": "Qual produto voce tem disponivel?"}
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    try:
        result = AuroraShoppingAssistant().crew().kickoff(
            inputs={"trigger_payload": trigger_payload, "message": ""}
        )
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
