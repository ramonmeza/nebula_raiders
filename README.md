# Nebula Raiders

## Link to Course
https://craftingtable.com/a/members/9ba4ad0b-df9d-4b70-9d81-52bb443831f9/a47555bb-dc7a-4177-bfc1-8955f72c8cc9

## My Personal Goals
I want to learn more about embedded systems and embedded programming, specifically utilizing Python. I want to be confident in reading datasheets and implementing drivers for different components.

Based on these goals, I will be writing the drivers from scratch when I can. For example, the LCD class in `lib/lcd.py` is my own driver for the LCD1602 component that I've derived from many sources and the Waveshare and Hitachi datasheets.

## How-To
- `pdm run upload-lib` will upload all files in `lib/` directory to the connected microcontroller.
- `mpremote fs cp .\02_signal_booster\main.py :main.py` needs to be called to upload `main.py` from a specific source directory onto the microcontolller.
- `pdm run reset` will soft reset the microcontroller.

\* Certain components need to be hard reset by turning off power completely, like the LCD.
