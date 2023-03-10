from machine import Pin
import utime


class StepMotorController:
    """ core class to control the stepper motor"""
    # The total number of steps of your stepper motor (check the specs)
    TOTAL_STEP = 2048

    # Sleeping time between each step. e.g.
    # The maximum rotation speed will be MIN_SLEEP * TOTAL_STEP (about 4 seconds / full rotation)
    MIN_SLEEP = 0.002
    # The minimum rotation speed will be MAX_SLEEP * TOTAL_STEP (about 102 seconds / full rotation)
    MAX_SLEEP = 0.05

    def __init__(self, in_1: int, in_2: int, in_3: int, in_4):
        """
        init function
        :param in_1: GPIO number where the IN1 is plugged
        :param in_2: GPIO number where the IN2 is plugged
        :param in_3: GPIO number where the IN3 is plugged
        :param in_4: GPIO number where the IN4 is plugged
        """
        self._pins = [
            Pin(in_1, Pin.OUT),
            Pin(in_2, Pin.OUT),
            Pin(in_3, Pin.OUT),
            Pin(in_4, Pin.OUT)
        ]

        self._motor_count = 0

        self._one_step_sequence = [[1, 0, 0, 0],
                                   [0, 1, 0, 0],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]]

        self.reset()

    def rotate(self, angle: int, direction: str, speed: float) -> None:
        """
        function used to rotate the step motor
        :param angle: angle in degree we want to rotate the step motor from its current position
        :param direction: clockwise (c), counter clockwise (cc)
        :param speed: between 0 and 1 with 1 is the higher speed
        """
        num_steps = int(angle * self.TOTAL_STEP / 360)
        sleep_time = self.MAX_SLEEP - (self.MAX_SLEEP - self.MIN_SLEEP) * speed

        for step in range(num_steps):
            if direction == "c":
                self._motor_count = (self._motor_count - 1) % 4
            elif direction == "cc":
                self._motor_count = (self._motor_count + 1) % 4

            for ind, pin in enumerate(self._pins):
                pin.value(self._one_step_sequence[self._motor_count][ind])
            utime.sleep(sleep_time)

    def reset(self):
        """ reset the GPIO """
        for pin in self._pins:
            pin.value(0)
