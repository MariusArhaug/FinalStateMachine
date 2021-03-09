""" FINAL STATE MACHINE """
import time

from rule import Rule
from kpc import KPC


class FSM:
    """
    Final state machine that circulates between different states
    gathered from rules in self.rules
    """
    def __init__(self, agent, list_of_rules, initial_state):
        """
        initialization
        """
        self.kpc = agent
        self.rules = list_of_rules
        self.initial_state = initial_state
        self.current_state = initial_state
        self.final_state = self.rules[-1].state2

    def fire(self, rule):
        """
        a) set next state of FSM
        b) call the appropriate agent action method (in rule)
        """
        self.current_state = rule.state2
        rule.action()

    def add_rule(self, rule):
        """
        add rule to fsm
        """
        self.rules.append(rule)

    def get_next_signal(self):
        """
        gets next signal, may be bad method
        """
        signal = self.kpc.get_next_signal()
        return signal

    def run(self):
        """
        run fsm machine while state is not end_state
        """
        while self.current_state != self.final_state:
            # Get next signal, typically from keypad
            signal = self.kpc.get_next_signal()
            # 9098432*print(signal)
            if signal is None:
                continue
            # Rule-Loop
            for rule in self.rules:
                if rule.match(self.current_state, signal):
                    # self.current_state = rule.state2
                    self.fire(rule)
                    break

def main():
    """
    main method for running the program
    """
    print("Welcome! Press any key to start!")
    agent = KPC()
    rule1 = Rule("S-init", "S-Read", "all_signals", agent.start)
    rule2 = Rule("S-Read", "S-Read", "all_digits", agent.append_next_password_digit)
    rule3 = Rule("S-Read", "S-Verify", "*", agent.verify_password)
    rule4 = Rule("S-Read", "S-init", "all_signals", agent.reset_agent)
    rule5 = Rule("S-Verify", "S-Active","Y", agent.fully_activate_agent)
    rule5_2 = Rule("S-Verify", "S-Read", "N", agent.reset_agent)
    #rule6 = Rule(state1="S-Verify", signal="all_signals", state2="S-init", action=KPC.reset_agent())
    rule6 = Rule("S-Active", "S-delete_password", "*", agent.confirm_reset)
    rule6_2 = Rule("S-delete_password", "S-reset", "*", agent.reset_password_accumulator)
    rule6_3 = Rule("S-delete_password", "S-Active", "#", agent.fully_activate_agent)
    rule6_4 = Rule("S-reset", "S-reset", "all_digits", agent.append_new_password)
    rule6_5 = Rule("S-reset", "S-Verify", "*", agent.verify_new_password)
    rule6_6 = Rule("S-Verify", "S-reset", "F", agent.append_new_password)
    rule7 = Rule("S-Active", "S_led", "all_digits", agent.append_led)
    #rule8 = Rule(state1="S_led", signal="all_digits", state2="S_led", action=KPC.append_led)
    rule9 = Rule("S_led", "S_time", "*", agent.append_led)
    rule10 = Rule("S_time", "S_time", "all_digits", agent.append_time)
    rule11 = Rule("S_time", "S_Active", "*", agent.set_time)
    rule12 = Rule("S_Active", "S_logout", "#", agent.begin_logout)
    rule13 = Rule("S_logout", "S_end", "#", agent.stop_system)
    rules = [rule1, rule2, rule3, rule4, rule5, rule5_2, rule6, rule6_2, rule6_3, rule6_4, rule6_5, rule6_6, rule7, rule9, rule10, rule11, rule12, rule13]
    fsm = FSM(list_of_rules=rules, initial_state="S-init", agent=agent)
    fsm.run()

if __name__ == '__main__':
    main()
