import adafruit_bus_device.i2c_device as i2c_device
from micropython import const

_MA_ADDR = const(0xB8)
_MA_STEP = const(0xF8)
_MA_RST = const(0xFD)
_MA_PGRM_CH = const(0xC0)
_MA_OFF = const(0x80)
_MA_ON = const(0x90)
_MA_UPD_COLROW = const(0xB0)  # Used to update either a row or column
_MA_MEM = const(0xA0)
_MA_GET_COLROW = const(0xF5)


class Matrixarchate:
    """
    """

    _BUFFER = bytearray(5)

    def __init__(self, i2c, address=_MA_ADDR):
        self._device = i2c_device.I2CDevice(i2c, address)

    def off(self, point, program=0xFF):
        self._BUFFER[0] = _MA_OFF & 0xFF
        self._BUFFER[1] = point & 0xFF
        self._BUFFER[2] = program & 0xFF

        with self._device as d:
            d.write(self._BUFFER, end=3)

    def on(self, point, program=0xFF):
        self._BUFFER[0] = _MA_ON & 0xFF
        self._BUFFER[1] = point & 0xFF
        self._BUFFER[2] = program & 0xFF

        with self._device as d:
            d.write(self._BUFFER, end=3)

    def updatecol(self, col, lval, hval, program=0xFF):
        self._BUFFER[0] = _MA_UPD_COLROW & 0xFF
        self._BUFFER[1] = (~0x80 & col) & 0xFF
        self._BUFFER[2] = program & 0xFF
        self._BUFFER[3] = lval & 0xFF
        self._BUFFER[4] = hval & 0xFF

        with self._device as d:
            d.write(self._BUFFER, end=5)

    def updaterow(self, row, val, program=0xFF):
        self._BUFFER[0] = _MA_UPD_COLROW & 0xFF
        self._BUFFER[1] = (0x80 | row) & 0xFF
        self._BUFFER[2] = program & 0xFF
        self._BUFFER[3] = val & 0xFF

        with self._device as d:
            d.write(self._BUFFER, end=4)

    def pgrmch(self, prog):
        self._BUFFER[0] = _MA_PGRM_CH & 0xFF
        self._BUFFER[1] = prog

        with self._device as d:
            d.write(self._BUFFER, end=2)

    def raw(self, buf):
        with self._device as d:
            d.write(buf)
