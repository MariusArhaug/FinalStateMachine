""" RULES """
class Rule:
    """
    Class for rules to be used for states, signals and actions
    """
    def __init__(self, state1, state2, signal, action):
        self.state1 = state1
        self.state2 = state2
        self.signal = signal
        self.action = action

    def match(self, fsm_state, signal):
        """
        if signal_is_digit(signal):
            return self.state1 == fsm_state and self.signal == int(signal)
        return self.state1 == fsm_state and self.signal == signal
        """
        return self.state1 == fsm_state and self.__check_signal(signal)

    def __check_signal(self, signal):
        """
        checks signal type
        """
        if self.signal == "all_signals":
            return True
        elif self.signal == "all_digits":
            return signal_is_digit(signal)
        return self.signal == signal

def signal_is_digit(signal):
    """
    if signal is digit
    """
    return 48 <= ord(signal) <= 57
