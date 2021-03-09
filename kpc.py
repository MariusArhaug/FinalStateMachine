""" KPC agent """
import keypad as KP
import charlieplexer as CP


class KPC:
    """
    Class for agent
    """

    def __init__(self):
        self.keypad = KP.Keypad()
        self.filepath = "passwordfield.txt"
        self.charlieplexer = CP.CharliePlex()
        self.override_signal = ""
        self.cump = ""
        self.signal = ""
        self.led = ""
        self.time = ""
        self.new_password = ""

    def get_next_signal(self):
        """
        send next signal
        """
        if self.override_signal != "":
            self.signal = self.override_signal
            self.override_signal = ""
        else:
            self.signal = self.keypad.get_next_signal()
        return self.signal

    def confirm_reset(self):
        """
        confirm that user want to reset
        """
        print("Press * to confirm reset of password")
        print("Press # to cancel")

    def reset_password_accumulator(self):
        """
        delete current password
        """
        with open(self.filepath, "r+") as file:
            file.truncate(0)
        print("Enter your new password. At least 4 digits.")

    def append_new_password(self):
        """
        lets user type in new password
        """
        self.new_password += self.get_next_signal()
        print("Press next digit. Finish with *")

    def verify_new_password(self):
        """
        verifying new password
        """
        if len(self.new_password) >= 4:
            with open(self.filepath, "r+") as file:
                file.write(self.new_password)
            print("New password saved")
            self.new_password = ""
            self.twinkle_leds(2)
            self.override_signal = 'Y'
        else:
            print("Not successful, start over")
            self.light_one_led(2,1)
            self.new_password = ""
            self.override_signal = 'F'

    def append_next_password_digit(self):
        """
        Enter next digit of password.
        For login
        """
        self.cump += self.signal
        print(f"Current password {self.cump}")

    def verify_password(self):
        """"
        Verify password with corresponding signals
        """
        with open(self.filepath, "r") as file:
            if file.readline() == self.cump:
                self.twinkle_leds(0.2)
                self.override_signal = 'Y'

                print("Successful login")
            else:
                print("Unsuccessful login")
                self.light_one_led(2, 0.2)
                print("Try again")
                self.start_leds()
                self.cump = ""
                self.override_signal = 'N'

    def reset_agent(self):
        """
        reset to initial state
        """
        print("Failed login, try again! ")
        self.cump = ""

    def light_one_led(self, led, time):
        """
        lights one led
        """
        self.charlieplexer.light_led_for_time(led, time)

    def twinkle_leds(self, time):
        """
        twinkle leds
        """
        self.charlieplexer.twinkle_all_leds(time)

    def exit_action(self):
        """
        exit leds
        """
        self.charlieplexer.flash_power_off()

    def start_leds(self):
        """
        leds for starting
        """
        self.charlieplexer.flash_power_on()

    def fully_activate_agent(self):
        """
        ui for active state
        """
        print("Successful login! You have three options:")
        print("1. Press digit 1-5 to choose LED to light up. Finish with *.")
        print("2. Press * to reset password.")
        print("3. Press # to logout")

    def append_led(self):
        """
        choosing which led to light
        """
        print("Led chosen, press *")
        if self.signal != "*":
            self.led += str(self.signal)

    def append_time(self):
        """
        for choosing time for leds to light
        """
        print("Time set")
        self.time += str(self.signal)

    def set_time(self):
        """
        sets the time and start the led
        """
        print("lightning leds")
        self.light_one_led(int(self.led), int(self.time))

    def begin_logout(self):
        """
        for user to confirm logout
        """
        print("Press # to confirm logout")

    def stop_system(self):
        """
        exit lights and changes state
        """
        print("Goodbye!")
        self.exit_action()

    def start(self):
        """
        start leds and ui
        """
        self.start_leds()
        print("Enter password, finish with *")