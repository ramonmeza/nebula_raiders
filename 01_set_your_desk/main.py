from utime import sleep

from lib.lcd import LCD


def main() -> None:
    lcd: LCD = LCD()
    try:
        messages: list[str] = [
            "Nebula Raider",
            "Comm System OK",
            "Incoming Msg",
            "Awaiting Command",
        ]

        while True:
            for message in messages:
                lcd.print(message)
                sleep(3)

    except KeyboardInterrupt:
        pass

    finally:
        lcd.set_display(False)
        lcd.set_backlight(False)


if __name__ == "__main__":
    main()
