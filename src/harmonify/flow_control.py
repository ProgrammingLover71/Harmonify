# Continue executing original & postfix
CONTINUE_EXEC = "continue"
# Continue executing original, but not postfix
CONTINUE_WITHOUT_POSTFIX = "continue_npf"
# Don't execute anything else
STOP_EXEC = "stop"


class FlowControlError(Exception):
    def __init__(self, state):
        super.__init__(f"Flow control state is not valid: {state}")