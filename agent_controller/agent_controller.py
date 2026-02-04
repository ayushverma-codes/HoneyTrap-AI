from agent_controller.components.fsm import FSM
from agent_controller.components.strategy_engine import StrategyEngine
from agent_controller.components.persona_engine import PersonaEngine
from constants import DEFAULT_PERSONA


class AgentController:

    def __init__(self):
        self.fsm = FSM()
        self.strategy = StrategyEngine()
        self.persona_engine = PersonaEngine()

    def handle(self, payload: dict):

        # ---------------------------------
        # 1. Load input
        # ---------------------------------

        context = payload.get("context", {})
        current_msg = payload.get("current_msg", "")
        scam_score = payload.get("scam_score", 0.0)

        # ---------------------------------
        # 2. Initialize context
        # ---------------------------------

        context.setdefault("state", "NORMAL_CHAT")
        context.setdefault("slots", {})
        context.setdefault("persona", DEFAULT_PERSONA)
        context.setdefault("history", [])
        context.setdefault("last_action", None)
        context.setdefault("turn", 0)

        # ---------------------------------
        # 3. FSM transition
        # ---------------------------------

        new_state = self.fsm.transition(
            context["state"],
            scam_score,
            context["slots"],
            context["turn"]
        )

        context["state"] = new_state

        # ---------------------------------
        # 4. StrategyEngine → action
        # ---------------------------------

        action = self.strategy.decide(
            new_state,
            context["slots"],
            context,
            current_msg
        )

        # ---------------------------------
        # 5. PersonaEngine → reply
        # ---------------------------------

        reply_text = self.persona_engine.render(
            action,
            context["persona"],
            current_msg,
            context["history"]
        )

        # ---------------------------------
        # 6. Update context
        # ---------------------------------

        context["last_action"] = action
        context["turn"] += 1

        context["history"].append({
            "role": "agent",
            "text": reply_text
        })

        # ---------------------------------
        # 7. Return structured response
        # ---------------------------------

        return {
            "reply_text": reply_text,
            "state": new_state,
            "action": action,
            "context": context
        }
