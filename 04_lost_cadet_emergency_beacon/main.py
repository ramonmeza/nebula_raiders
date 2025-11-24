# type: ignore
from machine import Pin
from utime import sleep_ms


DELAYS: list[int] = [500, 500, 150, 150, 150, 150]


def main() -> None:
    btn: Pin = Pin(2, Pin.IN, Pin.PULL_DOWN)
    led: Pin = Pin(3, Pin.OUT)
    buzzer: Pin = Pin(4, Pin.OUT)

    try:
        cur_delay: int = 0
        while True:
            if bool(btn.value()):
                led.on()
                buzzer.on()
                sleep_ms(DELAYS[cur_delay])

                led.off()
                buzzer.off()
                sleep_ms(DELAYS[cur_delay])
                cur_delay = (cur_delay + 1) % len(DELAYS)
            else:
                cur_delay = 0
    finally:
        led.off()
        buzzer.off()


if __name__ == "__main__":
    main()
