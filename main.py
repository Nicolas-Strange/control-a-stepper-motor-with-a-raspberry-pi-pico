from joystick import JoystickReader
from stepper_motor import StepMotorController


class Main:
    """ main class that will handle the loop """

    def __init__(self):
        """
        init function
        """
        self._stepper = StepMotorController(in_1=0, in_2=1, in_3=2, in_4=3)
        self._joystick = JoystickReader(vr_x=26, vr_y=27, vr_z=28)

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
