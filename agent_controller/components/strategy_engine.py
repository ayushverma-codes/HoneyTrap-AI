from constants import FSM_ACTIONS
from llm import get_llm


class StrategyEngine:

    def __init__(self):
        # LLM used only for micro-choice
        self.llm = get_llm("strategy")

    def decide(self, state, slots, context, current_msg):
        """
        Always returns single action string.
        """

        # ------------------------------------------------
        # HARD SLOT OVERRIDES (NO LLM)
        # ------------------------------------------------

        if state in ["CONFIRMED_SCAM", "EXTRACTION"]:

            if not slots.get("upi"):
                return "request_upi"

            if not slots.get("bank"):
                return "request_bank"

            if not slots.get("url"):
                return "request_url"

        # ------------------------------------------------
        # FSM ACTION SET
        # ------------------------------------------------

        allowed = FSM_ACTIONS.get(state, {}).copy()

        # ------------------------------------------------
        # EXTRACTION SLOT FILTERING
        # ------------------------------------------------

        if state == "EXTRACTION":

            if slots.get("upi"):
                allowed.pop("request_upi_again", None)

            if slots.get("bank"):
                allowed.pop("request_bank", None)

            if slots.get("url"):
                allowed.pop("request_url", None)

            # ------------------------------------------------
            # FINAL HARVEST LOOP (all slots filled)
            # ------------------------------------------------

            if slots.get("upi") and slots.get("bank") and slots.get("url"):
                allowed = {
                    "confirm_details": "Confirm received information",
                    "pretend_typo": "Say typed wrong",
                    "delay": "Delay response"
                }

        if not allowed:
            return None

        # ------------------------------------------------
        # SINGLE OPTION
        # ------------------------------------------------

        if len(allowed) == 1:
            return next(iter(allowed.keys()))

        # ------------------------------------------------
        # EARLY STATES: NO LLM
        # ------------------------------------------------

        if state in ["NORMAL_CHAT", "SUSPICIOUS"]:
            return next(iter(allowed.keys()))

        # ------------------------------------------------
        # LLM MICRO-CHOICE
        # ------------------------------------------------

        prompt = self._build_prompt(
            state=state,
            allowed=allowed,
            current_msg=current_msg,
            history=context.get("history", [])
        )

        try:
            llm_action = self.llm.generate(prompt).strip()
        except Exception:
            llm_action = None

        # Guardrail
        if llm_action in allowed:
            return llm_action

        # Fallback
        return next(iter(allowed.keys()))

    def _build_prompt(self, state, allowed, current_msg, history):

        actions_text = "\n".join([
            f"- {k}: {v}" for k, v in allowed.items()
        ])

        last_msgs = history[-3:] if history else []

        return f"""
You are selecting the next conversational action.

FSM State: {state}

Allowed actions:
{actions_text}

Recent conversation:
{last_msgs}

Current scammer message:
{current_msg}

Choose EXACTLY ONE action name from the list.
Return ONLY the action name.
Do NOT explain.
"""
