"""
End-to-end AgentController pipeline test.

Run:
    python pipeline/test_agent_controller.py

Simulates multi-turn conversation:
- normal → suspicious → confirmed → extraction
"""

import sys
import os
import json

# Allow imports from project root
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agent_controller.agent_controller import AgentController


def divider(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():

    agent = AgentController()

    # ------------------------------------------------
    # Initial input JSON (turn 1)
    # ------------------------------------------------

    payload = {
        "context": {
            "session_id": "abc123",
            "state": "NORMAL_CHAT",
            "slots": {
                "upi": None,
                "bank": None,
                "url": None
            },
            "persona": "elderly",
            "history": [],
            "last_action": None,
            "turn": 0
        },
        "current_msg": "hello",
        "scam_score": 0.1
    }

    divider("TURN 1")

    response = agent.handle(payload)
    print(json.dumps(response, indent=2))

    # ------------------------------------------------
    # Turn 2 — suspicious offer
    # ------------------------------------------------

    payload["context"] = response["context"]
    payload["current_msg"] = "you won prize send small fee"
    payload["scam_score"] = 0.5

    divider("TURN 2")

    response = agent.handle(payload)
    print(json.dumps(response, indent=2))

    # ------------------------------------------------
    # Turn 3 — confirmed scam
    # ------------------------------------------------

    payload["context"] = response["context"]
    payload["current_msg"] = "send 500 now"
    payload["scam_score"] = 0.85

    divider("TURN 3")

    response = agent.handle(payload)
    print(json.dumps(response, indent=2))

    # ------------------------------------------------
    # Turn 4 — simulate slot extraction (UPI arrives)
    # ------------------------------------------------

    payload["context"] = response["context"]
    payload["context"]["slots"]["upi"] = "fraud@upi"
    payload["current_msg"] = "my upi is fraud@upi"
    payload["scam_score"] = 0.9

    divider("TURN 4")

    response = agent.handle(payload)
    print(json.dumps(response, indent=2))

    # ------------------------------------------------
    # Turn 5 — bank arrives
    # ------------------------------------------------

    payload["context"] = response["context"]
    payload["context"]["slots"]["bank"] = "12345678"
    payload["current_msg"] = "bank acc 12345678"
    payload["scam_score"] = 0.9

    divider("TURN 5")

    response = agent.handle(payload)
    print(json.dumps(response, indent=2))

    # ------------------------------------------------
    # Turn 6 — phishing URL arrives
    # ------------------------------------------------

    payload["context"] = response["context"]
    payload["context"]["slots"]["url"] = "http://fake-pay.com"
    payload["current_msg"] = "pay here http://fake-pay.com"
    payload["scam_score"] = 0.9

    divider("TURN 6")

    response = agent.handle(payload)
    print(json.dumps(response, indent=2))

    divider("AGENT CONTROLLER PIPELINE COMPLETE")


if __name__ == "__main__":
    main()
