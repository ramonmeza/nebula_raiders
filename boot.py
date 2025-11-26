# type: ignore
from secrets import WIFI_SSID, WIFI_PASSWORD

import machine
import network
import utime

from lib.ntp import get_server_time

# turn on built-in LED
power_led: machine.Pin = machine.Pin("LED", machine.Pin.OUT)
power_led.on()


# configure network
def initialize_wifi() -> network.WLAN:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        utime.sleep_ms(100)
    return wlan


# set RTC
def setup_rtc() -> machine.RTC:
    unix_time = get_server_time("pool.ntp.org")
    tm = utime.localtime(unix_time)
    rtc = machine.RTC()
    rtc.datetime((tm[0], tm[1], tm[2], tm[6], tm[3], tm[4], tm[5], 0))
    return rtc
