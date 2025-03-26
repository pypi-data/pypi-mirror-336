import sys
import time

from tmx_nano2040_wifi import tmx_nano2040_wifi

"""
Monitor a digital input pin with pullup enabled
"""

# The callback data is provided as a list.
# These are the indices into the list for the reported data.

# This is an index to the pin mode.
CB_PIN_MODE = 0
# This is an index to the reporting pin number
CB_PIN = 1
# This is an index to the reported data change
CB_VALUE = 2
# This is an index to the raw time-stamp the change occurred
CB_TIME = 3


def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the change occurred

    :param data: [pin mode, pin, current reported value,
                  pin_mode, timestamp]
    """

    # convert the raw time stamp into human readable format
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
    print(f'Report Type: {data[CB_PIN_MODE]} Pin: {data[CB_PIN]} '
          f'Value: {data[CB_VALUE]} Time Stamp: {date}')


# Instantiate the telemetrix class providing the IP address
# of the Nano RP2040.

board = tmx_nano2040_wifi.TmxNano2040Wifi(ip_address='192.168.2.246')

# Set the pin mode for pin 11 and establish the callback.
board.set_pin_mode_digital_input_pullup(11, the_callback)

try:
    # wait forever reporting all data changes.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # perform an orderly shutdown
    board.shutdown()
    sys.exit(0)