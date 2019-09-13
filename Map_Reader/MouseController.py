import ctypes

#https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa

class MouseController():
    def setSpeed(self, speed):
        #   1 - slow
        #   10 - standard
        #   20 - fast
        set_mouse_speed = 113   # 0x0071 for SPI_SETMOUSESPEED
        ctypes.windll.user32.SystemParametersInfoA(set_mouse_speed, 0, speed, 0)

    def getSpeed(self):
        get_mouse_speed = 112   # 0x0070 for SPI_GETMOUSESPEED
        speed = ctypes.c_int()
        ctypes.windll.user32.SystemParametersInfoA(get_mouse_speed, 0, ctypes.byref(speed), 0)

        return speed.value 

    def toggleAcceleration(self, b):
        arr = [0, 0, int(b)]
        mouse_params = (ctypes.c_int * len(arr))(*arr)
        set_mouse = 4   # 0x0004 for SPI_SETMOUSE
        ctypes.windll.user32.SystemParametersInfoA(set_mouse, 0, mouse_params, 0)