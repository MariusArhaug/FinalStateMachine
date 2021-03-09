"""Interface object between agent and charlieplexer"""
from GPIOSimulator_v5 import *
import time

GPIO = GPIOSimulator()


class CharliePlex:
    """
    class for controlling the lights
    """
    def __init__(self):
        self.GPIO = GPIO

    def light_led(self, led, debug=True):
        """
        Turn on one of the 6 LEDs,
        by making the appropriate combination of input
        and output declarations and then making appropriate HIGH/LOW settings12344*
        """
        valid_led = [0, 1, 2, 3, 4, 5]
        if led not in valid_led:
            print("Not a valid LED; you must choose between an LED with number 0-5")
            return

        if led == 0:
            self.GPIO.setup(PIN_CHARLIEPLEXING_0, GPIO.OUT, state=GPIO.HIGH)
            self.GPIO.setup(PIN_CHARLIEPLEXING_1, GPIO.OUT, state=GPIO.HIGH)
            self.GPIO.setup(PIN_CHARLIEPLEXING_2, GPIO.IN, state=GPIO.LOW)
            self.GPIO.output(PIN_CHARLIEPLEXING_0, state=GPIO.HIGH)
            self.GPIO.output(PIN_CHARLIEPLEXING_1, state=GPIO.LOW)
        elif led == 1:
            self.GPIO.setup(PIN_CHARLIEPLEXING_0, GPIO.OUT, state=GPIO.HIGH)
            self.GPIO.setup(PIN_CHARLIEPLEXING_1, GPIO.OUT, state=GPIO.HIGH)
            self.GPIO.setup(PIN_CHARLIEPLEXING_2, GPIO.IN, state=GPIO.HIGH)
            self.GPIO.output(PIN_CHARLIEPLEXING_0, state=GPIO.LOW)
            self.GPIO.output(PIN_CHARLIEPLEXING_1, state=GPIO.HIGH)
            # print("LED 1 is active")
        elif led == 2:
            self.GPIO.setup(PIN_CHARLIEPLEXING_0, GPIO.IN, state=GPIO.HIGH)
            self.GPIO.setup(PIN_CHARLIEPLEXING_1, GPIO.OUT, state=GPIO.LOW)
            self.GPIO.setup(PIN_CHARLIEPLEXING_2, GPIO.OUT, state=GPIO.LOW)
            self.GPIO.output(PIN_CHARLIEPLEXING_1, state=GPIO.HIGH)
            self.GPIO.output(PIN_CHARLIEPLEXING_2, state=GPIO.LOW)
        elif led == 3:
            self.GPIO.setup(PIN_CHARLIEPLEXING_0, GPIO.IN, state=GPIO.LOW)
            self.GPIO.setup(PIN_CHARLIEPLEXING_1, GPIO.OUT, state=GPIO.LOW)
            self.GPIO.setup(PIN_CHARLIEPLEXING_2, GPIO.OUT, state=GPIO.HIGH)
            self.GPIO.output(PIN_CHARLIEPLEXING_1, state=GPIO.LOW)
            self.GPIO.output(PIN_CHARLIEPLEXING_2, state=GPIO.HIGH)
        elif led == 4:
            self.GPIO.setup(PIN_CHARLIEPLEXING_0, GPIO.OUT, state=GPIO.LOW)
            self.GPIO.setup(PIN_CHARLIEPLEXING_1, GPIO.IN, state=GPIO.HIGH)
            self.GPIO.setup(PIN_CHARLIEPLEXING_2, GPIO.OUT, state=GPIO.HIGH)
            self.GPIO.output(PIN_CHARLIEPLEXING_0, state=GPIO.HIGH)
            self.GPIO.output(PIN_CHARLIEPLEXING_2, state=GPIO.LOW)
        elif led == 5:
            self.GPIO.setup(PIN_CHARLIEPLEXING_0, GPIO.OUT, state=GPIO.LOW)
            self.GPIO.setup(PIN_CHARLIEPLEXING_1, GPIO.IN, state=GPIO.LOW)
            self.GPIO.setup(PIN_CHARLIEPLEXING_2, GPIO.OUT, state=GPIO.HIGH)
            self.GPIO.output(PIN_CHARLIEPLEXING_0, state=GPIO.LOW)
            self.GPIO.output(PIN_CHARLIEPLEXING_2, state=GPIO.HIGH)
        if debug:
            print(f'LED #{led} ON')
        time.sleep(0.1)
        self.GPIO.cleanup()
        print(f'LED #{led} OFF')

    def flash_all_leds(self, k):
        """
        Flash all 6 LEDs on and off for k seconds,
        since we can only light up one LED at the time,
        we can make the duration between LEDs short thus indicating all flashing
        """
        time_end = time.time() + k
        while time.time() < time_end:
            for i in range(0, 6):
                self.light_led(i)
                time.sleep(0.01)

    def twinkle_all_leds(self, k):
        """
        Turn all LEDs of and off in sequence for k seconds
        """
        time_end = time.time() + k
        while time.time() < time_end:
            for i in range(0, 6):
                self.light_led(i)
                time.sleep(1)

    def flash_power_on(self):
        """
        Flash LEDs when powering on
        """
        time_end = time.time() + 1.5
        while time.time() < time_end:
            for i in range(0, 6):
                self.light_led(i)
                self.light_led((i + 1) % 6)
                self.light_led((i + 2) % 6)
                time.sleep(1)

    def flash_power_off(self):
        """
        Flash LEDs when powering off
        """
        time_end = time.time() + 1.5
        while time.time() < time_end:
            self.light_led(0)
            time.sleep(0.5)

    def light_led_for_time(self, led, k):
        """
        Flash one led for k number of secs
        """
        time_end = time.time() + k
        while time.time() < time_end:
            self.light_led(led)


def main():
    """
    main method to test the class
    """
    # Tests
    charlie = CharliePlex()
    # charlie.flash_all_leds(2)
    charlie.twinkle_all_leds(2)
    charlie.GPIO.show_leds_states()
    time.sleep(2)
    charlie.GPIO.show_leds_states()
    charlie.flash_power_off()
    charlie.flash_power_on()


if __name__ == '__main__':
    main()
