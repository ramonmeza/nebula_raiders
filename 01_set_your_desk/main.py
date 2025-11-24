# type: ignore
from machine import Pin
from utime import sleep


def main():
    led_green: Pin = Pin(15, Pin.OUT)
    led_red: Pin = Pin(14, Pin.OUT)
    led_blue: Pin = Pin(13, Pin.OUT)

    try:
        while True:
            led_green.on()
            sleep(1)
            led_green.off()

            led_red.on()
            sleep(1)
            led_red.off()

            led_blue.on()
            sleep(1)
            led_blue.off()

    except KeyboardInterrupt:
        pass

    finally:
        led_green.off()
        led_red.off()
        led_blue.off()


if __name__ == "__main__":
    main()
