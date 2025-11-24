# type: ignore
import machine
import utime


def main():
    led: machine.Pin = machine.Pin("LED", machine.Pin.OUT)

    try:
        while True:
            led.value(True)
            utime.sleep(1)
            led.value(False)
            utime.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        led.value(False)


if __name__ == "__main__":
    main()
