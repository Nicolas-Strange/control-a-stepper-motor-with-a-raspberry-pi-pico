import json

import utime
from machine import ADC, Pin


class JoystickReader:
    """ core class to read the Joystick values """

    def __init__(self, vr_x: int, vr_y: int, vr_z: int):
        """
        init function
        :param vr_x: GPIO number where the VRX is plugged
        :param vr_y: GPIO number where the VRY is plugged
        :param vr_z: GPIO number where the VRZ is plugged
        """
        self._analog_x = ADC(Pin(vr_x))
        self._analog_y = ADC(Pin(vr_y))
        self._analog_z = Pin(vr_z, Pin.IN, Pin.PULL_UP)

        with open("./calibration.json") as infile:
            self._cal_conf = json.load(infile)

        self._min_x = self._cal_conf["min_x"]
        self._min_y = self._cal_conf["min_y"]
        self._max_x = self._cal_conf["max_x"]
        self._max_y = self._cal_conf["max_y"]
        self._middle_x = self._cal_conf["middle_x"]
        self._middle_y = self._cal_conf["middle_y"]

        self._std_middle = self._cal_conf["std_middle"]

    def calibrate(self) -> None:
        """
        Calibrate the joystick.
        Sequence: left, right, up, down, then press z
        Sequence: middle, then press z
        """
        print("Calibration x, y: slowly rotate the joystick in all the directions then press z")
        x_values, y_values = self._calibration()
        self._min_x = min(x_values)
        self._max_x = max(x_values)

        self._min_y = min(y_values)
        self._max_y = max(y_values)

        utime.sleep(1)

        print("Calibration middle: don't touch the joystick, wait few seconds, then press z")
        x_values, y_values = self._calibration()

        self._middle_x = int(sum(x_values) / len(x_values))
        self._middle_y = int(sum(y_values) / len(y_values))

        values = x_values + y_values
        self._std_middle = 2 * int((sum((x-(sum(values) / len(values)))**2 for x in values) / (len(values)-1))**0.5)

        self._cal_conf["min_x"] = self._min_x
        self._cal_conf["min_y"] = self._min_y
        self._cal_conf["max_x"] = self._max_x
        self._cal_conf["max_y"] = self._max_y
        self._cal_conf["middle_x"] = self._middle_x
        self._cal_conf["middle_y"] = self._middle_y
        self._cal_conf["std_middle"] = self._std_middle

        print(f'min_x: {self._cal_conf["min_x"]}')
        print(f'min_y: {self._cal_conf["min_y"]}')
        print(f'max_x: {self._cal_conf["max_x"]}')
        print(f'max_y: {self._cal_conf["max_y"]}')
        print(f'middle_x: {self._cal_conf["middle_x"]}')
        print(f'middle_y: {self._cal_conf["middle_y"]}')
        print(f'std_middle: {self._cal_conf["std_middle"]}')

        with open("./calibration.json", "w") as outfile:
            outfile.write(json.dumps(self._cal_conf))

    def _calibration(self) -> tuple:
        """ hidden function for the calibration """
        list_x_values = []
        list_y_values = []

        while self._analog_z.value() == 1:
            list_x_values.append(self._analog_x.read_u16())
            list_y_values.append(self._analog_y.read_u16())
            utime.sleep(0.1)

        return list_x_values, list_y_values

    def read(self) -> tuple:
        """
        read the analog values and return a tuple with x, y, and z values
        """
        # normalize the values
        val_x = self._analog_x.read_u16()
        val_y = self._analog_y.read_u16()
        val_z = self._analog_z.value()

        # normalization of x
        if val_x > self._middle_x + self._std_middle:
            min_x = self._middle_x + self._std_middle
            val_x = (val_x - min_x) / (self._max_x - min_x) * 100
        elif val_x < self._middle_x - self._std_middle:
            max_x = self._middle_x - self._std_middle
            val_x = -(100 - ((val_x - self._min_x) / (max_x - self._min_x) * 100))
        else:
            val_x = 0

        if val_y > self._middle_y + self._std_middle:
            min_y = self._middle_y + self._std_middle
            val_y = -(val_y - min_y) / (self._max_y - min_y) * 100
        elif val_y < self._middle_y - self._std_middle:
            max_y = self._middle_y - self._std_middle
            val_y = 100 - ((val_y - self._min_y) / (max_y - self._min_y) * 100)
        else:
            val_y = 0

        return val_x, val_y, val_z
