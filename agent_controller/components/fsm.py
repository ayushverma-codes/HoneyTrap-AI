from constants import FSM_STATES, MAX_TURNS


class FSM:

    def transition(self, prev_state, scam_score, slots, turn):
        """
        Decide next FSM state.

        Args:
            prev_state: str
            scam_score: float
            slots: dict
            turn: int

        Returns:
            str (FSM state)
        """

        # Safety exit
        if turn >= MAX_TURNS:
            return "EXIT"

        # If any slot filled → extraction
        for v in slots.values():
            if v:
                return "EXTRACTION"

        # High confidence scam
        if scam_score >= 0.7:
            return "CONFIRMED_SCAM"

        # Medium suspicion
        if scam_score >= 0.4:
            return "SUSPICIOUS"

        # Default
        return "NORMAL_CHAT"
