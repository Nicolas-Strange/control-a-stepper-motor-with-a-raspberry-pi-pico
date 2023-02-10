from joystick import JoystickReader
from stepper_motor import StepMotorController


class Main:
    """ main class that will handle the loop """

    def __init__(self):
        """
        init function
        """
        self._stepper = StepMotorController()
        self._joystick = JoystickReader()

    def run(self) -> None:
        """
        core function to iterate
        For each iteration the joystick value will be read and the stepper motor will be updated
        """
        self._joystick.calibrate()  # comment here if your joystick is correctly calibrated
        while True:
            x, y, z = self._joystick.read()
            if x > 0:
                self._stepper.rotate(angle=1, direction="c", speed=x / 100)
            elif x < 0:
                self._stepper.rotate(angle=1, direction="cc", speed=-x / 100)
            else:
                self._stepper.reset()


if __name__ == '__main__':
    run = Main()
    run.run()
