"""Keypad acts as an interface between keypad controller agent and simulated keypad"""
from GPIOSimulator_v5 import GPIOSimulator, keypad_row_pins, keypad_col_pins
import time

# Global GPIO
GPIO = GPIOSimulator()

KEYPAD_VALUES = {(3, 7): '1',
                 (3, 8): '2',
                 (3, 9): '3',
                 (4, 7): '4',
                 (4, 8): '5',
                 (4, 9): '6',
                 (5, 7): '7',
                 (5, 8): '8',
                 (5, 9): '9',
                 (6, 7): '*',
                 (6, 8): '0',
                 (6, 9): '#'}

class Keypad:
    """
    Class for Keypad
    """
    def __init__(self):
        self.GPIO = GPIOSimulator()
        self.setup()

    def setup(self):
        """ For each row pin do:"""
        for rp in keypad_row_pins:
            self.GPIO.setup(rp, GPIO.OUT)

        # For each column pin do:
        for cp in keypad_col_pins:
            self.GPIO.setup(cp, GPIO.IN, state=GPIO.LOW)

    def do_polling(self):
        """Poll key presses"""
        for rp in keypad_row_pins:
            self.GPIO.output(rp, state=GPIO.HIGH)
            for cp in keypad_col_pins:
                if self.GPIO.input(cp) == GPIO.HIGH:
                    # Button pressed = key
                    key = (rp, cp)
                    # print(key)
                    return key
            self.GPIO.output(rp, state=GPIO.LOW)
        return None

    def get_next_signal(self):
        """
        gets next signal from keypad
        """
        fixed_time = 0.25
        while True:
            signal_key = self.do_polling()
            # print(signal_key)
            time.sleep(fixed_time)
            if signal_key is not None:
                return translate_signal_key(signal_key)


def translate_signal_key(key):
    """
    translates the signal to right value
    """
    if key in KEYPAD_VALUES:
        return KEYPAD_VALUES[key]
    else:
        return "Not valid signal"

def main():
    """
    main method to test the class
    """
    keypad = Keypad()
    print(keypad.get_next_signal())

if __name__ == '__main__':
    main()
