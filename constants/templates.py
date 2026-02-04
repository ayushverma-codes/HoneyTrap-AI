import random


TEMPLATES = {

    "elderly": {

        "greet": [
            "hello beta",
            "hi"
        ],

        "acknowledge": [
            "ok",
            "hmm"
        ],

        "request_upi": [
            "sir pls send upi",
            "where send money?"
        ],

        "request_bank": [
            "upi not working send bank acc",
        ],

        "fake_payment_error": [
            "showing error pls resend",
        ],

        "confirm_details": [
            "is this correct?",
        ],

        "delay": [
            "wait net slow",
        ]
    },

    "student": {

        "greet": ["hi"],

        "request_upi": [
            "pls share upi id",
        ],

        "request_bank": [
            "upi failed can send bank?"
        ],

        "confirm_details": [
            "this correct right?"
        ],

        "delay": [
            "one min"
        ]
    },

    "worker": {

        "greet": ["hi"],

        "request_upi": [
            "send upi"
        ],

        "request_bank": [
            "upi not working give bank"
        ],

        "confirm_details": [
            "pls confirm"
        ],

        "delay": [
            "checking"
        ]
    }
}


def get_template(persona, action):

    persona_templates = TEMPLATES.get(persona, {})
    action_templates = persona_templates.get(action)

    if not action_templates:
        return None

    return random.choice(action_templates)
