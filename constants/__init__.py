

# =========================================================
# FSM STATES
# =========================================================

FSM_STATES = {
    "NORMAL_CHAT": "Casual conversation, build trust",
    "SUSPICIOUS": "Scammer hinting offer or opportunity",
    "CONFIRMED_SCAM": "Clear scam, payment discussion started",
    "EXTRACTION": "Collecting payment or phishing details",
    "EXIT": "Terminate conversation"
}


# =========================================================
# ACTION REGISTRY (FSM → Actions → Descriptions)
# =========================================================

FSM_ACTIONS = {

    "NORMAL_CHAT": {
        "greet": "Say simple hello",
        "acknowledge": "Short acknowledgment",
        "mirror_message": "Mirror last scammer message",
        "small_talk": "Light casual conversation"
    },

    "SUSPICIOUS": {
        "probe_offer": "Ask about the offer",
        "ask_process": "Ask how it works",
        "ask_fee": "Ask if payment required",
        "request_details": "Ask for more explanation",
        "show_interest": "Show mild interest"
    },

    "CONFIRMED_SCAM": {
        "agree_to_pay": "Agree to proceed",
        "request_upi": "Ask for UPI ID",
        "request_link": "Ask for payment link",
        "ask_payment_method": "Ask preferred payment method",
        "request_qr": "Ask for QR code"
    },

    "EXTRACTION": {
        "request_upi_again": "Ask for UPI again",
        "request_bank": "Ask bank account",
        "request_url": "Ask phishing or payment link",
        "fake_payment_error": "Pretend payment failed",
        "confirm_details": "Confirm received information",
        "pretend_typo": "Say typed wrong",
        "dual_request": "Ask two payment methods",
        "delay": "Delay response",
        "ask_alternate_method": "Ask alternate payment"
    },

    "EXIT": {
        "exit": "Stop conversation",
        "fake_busy": "Say busy now",
        "promise_later": "Say will pay later"
    }
}


# =========================================================
# PERSONAS
# =========================================================

PERSONAS = {
    "elderly": {
        "description": "Old person, confused with technology, polite",
        "typing_style": "broken",
        "emotion": "anxious"
    },

    "student": {
        "description": "Student looking for opportunities",
        "typing_style": "casual",
        "emotion": "hopeful"
    },

    "worker": {
        "description": "Busy working professional",
        "typing_style": "short",
        "emotion": "neutral"
    }
}


# =========================================================
# STRATEGY MODE
# =========================================================

# Options:
# "LOGIC_FIRST"   -> StrategyEngine selects action
# "PERSONA_FIRST" -> PersonaEngine + LLM selects action

STRATEGY_MODE = "LOGIC_FIRST"


# =========================================================
# GLOBAL CONSTANTS
# =========================================================

MAX_TURNS = 20

DEFAULT_PERSONA = "elderly"

SUPPORTED_SLOTS = ["upi", "bank", "url", "qr"]

LLM_TIMEOUT = 10  # seconds

