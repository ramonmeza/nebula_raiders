# type: ignore
from machine import Pin
from utime import sleep_ms


def main() -> None:
    pir_sensor = Pin(2, Pin.IN)
    led = Pin(3, Pin.OUT)

    try:
        while True:
            if pir_sensor.value():
                led.on()
            else:
                led.off()
            sleep_ms(10)

    finally:
        led.off()


if __name__ == "__main__":
    main()
