# type: ignore

from machine import Pin
from utime import sleep, sleep_ms


class SlideSwitch:
    def __init__(self, on_pin: int, off_pin: int) -> None:
        self._on_pin = Pin(on_pin, Pin.IN, Pin.PULL_DOWN)
        self._off_pin = Pin(off_pin, Pin.IN, Pin.PULL_DOWN)

    def is_on(self) -> bool:
        # there seems to be a bug when switching on and off too fast
        # once signal boosted (green LED), then switch off, sometimes goes to yellow LED
        # fix seems to be sleeping, which fixes the bug mentioned above
        sleep_ms(5)
        return self._on_pin.value() > 0 and self._off_pin.value() == 0


class SignalBooster:
    def __init__(
        self,
        sw_on_pin: int,
        sw_off_pin: int,
        led_red_pin: int,
        led_yellow_pin: int,
        led_green_pin: int,
    ) -> None:
        self._slide_sw = SlideSwitch(sw_on_pin, sw_off_pin)
        self._led_red = Pin(led_red_pin, Pin.OUT)
        self._led_yellow = Pin(led_yellow_pin, Pin.OUT)
        self._led_green = Pin(led_green_pin, Pin.OUT)

    def set_leds(
        self, red: bool = False, yellow: bool = False, green: bool = False
    ) -> None:
        self._led_red.value(red)
        self._led_yellow.value(yellow)
        self._led_green.value(green)

    def boost_signal(self) -> None:
        self.set_leds(yellow=True)
        sleep(1)
        self.set_leds(green=True)
        while self._slide_sw.is_on():
            pass

    def run(self) -> None:
        while True:
            try:
                self.set_leds(red=True)
                if self._slide_sw.is_on():
                    self.boost_signal()

            except KeyboardInterrupt:
                break
            finally:
                self.set_leds(False, False, False)


def main() -> None:
    sb = SignalBooster(17, 16, 15, 14, 13)
    sb.run()


if __name__ == "__main__":
    main()
