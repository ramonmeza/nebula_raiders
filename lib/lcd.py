# type: ignore

from machine import I2C, Pin
from utime import sleep_ms, sleep_us


class PCF8574:
    def __init__(self) -> None:
        self.RegisterSelect: bool = False
        self.ReadWrite: bool = False
        self.Enable: bool = False
        self.BacklightControl: bool = True
        self.Data4: bool = False
        self.Data5: bool = False
        self.Data6: bool = False
        self.Data7: bool = False

    def set_data(self, nibble: int) -> None:
        data: int = nibble & 0xF
        self.Data7 = bool(data & 0b1000)  # MSB of nibble
        self.Data6 = bool(data & 0b0100)
        self.Data5 = bool(data & 0b0010)
        self.Data4 = bool(data & 0b0001)  # LSB of nibble
        print(f"Data set: {str(self)}")

    def __int__(self) -> int:
        value: int = (
            (self.Data7 << 7)  # pin 7 (MSB) on PCF8574
            | (self.Data6 << 6)  # pin 6
            | (self.Data5 << 5)  # pin 5
            | (self.Data4 << 4)  # pin 4
            | (self.BacklightControl << 3)  # pin 3
            | (self.Enable << 2)  # pin 2
            | (self.ReadWrite << 1)  # pin 1
            | (self.RegisterSelect << 0)  # pin 0
        )
        return value

    def __str__(self) -> str:
        return f"PCF8574(value={hex(int(self))}, RS={int(self.RegisterSelect)}, RW={int(self.ReadWrite)}, EN={int(self.Enable)}, BL={int(self.BacklightControl)}, D7={self.Data7}, D6={self.Data6}, D5={self.Data5}, D4={self.Data4})"


class I2CDriver:
    def __init__(self, sda: int, scl: int) -> None:
        self._i2c = I2C(sda=Pin(sda), scl=Pin(scl))
        self._addr = 0x27
        self._pcf8574 = PCF8574()
        self._initialize()
        self._row_offsets = [0x00, 0x40]

    def _write_to_chip(self) -> None:
        data: bytes = int(self._pcf8574).to_bytes(1, "big")
        self._i2c.writeto(self._addr, data)

    def pulse_enable(self) -> None:
        self._pcf8574.Enable = True
        self._write_to_chip()
        sleep_us(2)
        self._pcf8574.Enable = False
        self._write_to_chip()
        sleep_us(53)

    def write_command(self, command: int) -> None:
        self._pcf8574.RegisterSelect = 0
        self._write_byte(command)

    def write_char(self, char: str) -> None:
        self._pcf8574.RegisterSelect = 1
        self._write_byte(ord(char))

    def _initialize(self) -> None:
        sleep_ms(150)
        self._init_4bit_mode()
        self.function_set()
        self.display_switch()
        self.screen_clear()
        self.input_set()
        self.display_switch(D=1)

    def _init_4bit_mode(self) -> None:
        print("Initialize 4-bit Mode...")
        self._pcf8574.RegisterSelect = 0
        self._pcf8574.ReadWrite = 0
        self._write_nibble(0x3)
        print("Wait 5ms")
        sleep_ms(5)

        self._pcf8574.RegisterSelect = 0
        self._pcf8574.ReadWrite = 0
        self._write_nibble(0x3)
        print("Wait 100us")
        sleep_us(100)

        self._pcf8574.RegisterSelect = 0
        self._pcf8574.ReadWrite = 0
        self._write_nibble(0x3)
        print("Wait 100us")
        sleep_us(100)

        self._pcf8574.RegisterSelect = 0
        self._pcf8574.ReadWrite = 0
        self._write_nibble(0x2)
        print("Wait 100us")
        sleep_us(100)

    def function_set(self, N: int = 1, F: int = 0) -> None:
        cmd: int = 0b00100000 | (N << 3) | (F << 2)
        print(f"function_set({hex(cmd)})")
        self.write_command(cmd)

    def display_switch(self, D: int = 0, C: int = 0, B: int = 0) -> None:
        cmd: int = 0b00001000 | (D << 2) | (C << 1) | B
        print(f"display_switch({hex(cmd)})")
        self.write_command(cmd)

    def input_set(self, id: int = 1, s: int = 0) -> None:
        cmd: int = 0b00000100 | (id << 1) | s
        print(f"input_set({hex(cmd)})")
        self.write_command(cmd)

    def set_cursor(self, row: int, col: int) -> None:
        addr: int = self._row_offsets[row] + col
        cmd: int = 0x80 | addr
        print(f"set_cursor({hex(cmd)})")
        self.write_command(cmd)

    def screen_clear(self) -> None:
        cmd: int = 0x01
        print(f"screen_clear({hex(cmd)})")
        self.write_command(cmd)
        sleep_ms(2)

    def _write_nibble(self, nibble: int) -> None:
        self._pcf8574.set_data(nibble)
        self._write_to_chip()
        self.pulse_enable()

    def _write_byte(self, byte: int) -> None:
        hi_nibble: int = (byte & 0xF0) >> 4
        lo_nibble: int = byte & 0x0F
        print(
            f"Write byte: {hex(byte)} -> High Nibble: {hex(hi_nibble)}, Low Nibble: {hex(lo_nibble)}"
        )
        self._write_nibble(hi_nibble)
        self._write_nibble(lo_nibble)

    @property
    def backlight(self) -> bool:
        return self._pcf8574.BacklightControl

    @backlight.setter
    def backlight(self, value: bool) -> None:
        self._pcf8574.BacklightControl = value
        self._write_to_chip()


class LCD:
    def __init__(self) -> None:
        self._driver = I2CDriver(sda=0, scl=1)

    def set_cursor(self, row: int, col: int) -> None:
        self._driver.set_cursor(row, col)

    def clear(self) -> None:
        self._driver.screen_clear()
        self.set_cursor(0, 0)

    def write_string(self, text: str) -> None:
        for c in text:
            self._driver.write_char(c)

    def print(self, text: str) -> None:
        self.clear()
        self.write_string(text)

    def set_display(self, value: bool) -> None:
        self._driver.display_switch(D=1 if value else 0)

    def set_backlight(self, value: bool) -> None:
        self._driver.backlight = value
