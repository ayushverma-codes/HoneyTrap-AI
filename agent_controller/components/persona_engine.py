from constants import PERSONAS
from constants.templates import get_template
from llm import get_llm


class PersonaEngine:

    def __init__(self):
        self.llm = get_llm("persona")

    def render(self, action, persona, current_msg, history):

        template = get_template(persona, action)

        if template:
            return template

        return self._llm_render(action, persona, current_msg, history)

    def _llm_render(self, action, persona, current_msg, history):

        persona_info = PERSONAS.get(persona, {})

        last_msgs = history[-3:] if history else []

        prompt = f"""
You are pretending to be a {persona} person.

Persona description:
{persona_info.get("description")}

Your task:
Perform this action: {action}

Conversation context:
{last_msgs}

Latest scammer message:
{current_msg}

Rules:
- Reply in very short sentences
- Use informal grammar
- Sound human
- No emojis
- No explanations

Generate only ONE reply.
"""

        try:
            return self.llm.generate(prompt).strip()
        except Exception:
            return "ok"
