"""
 Copyright (c) 2021 Alan Yorinks All rights reserved.

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,f
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

 DHT support courtesy of Martyn Wheeler
 Based on the DHTNew library - https://github.com/RobTillaart/DHTNew
"""

import sys
import time

from telemetrix_rpi_pico import telemetrix_rpi_pico

"""
Monitor the Pico internal temperature sensor (ADC 4) and return raw values.
"""

# Setup a pin for analog input and monitor its changes
ADC = 4  # temperature sensor ADC

# Callback data indices
CB_PIN_MODE = 0
CB_PIN = 1
CB_VALUE = 2
CB_TIME = 3


def the_callback(data):
    """
    A callback function to report data changes.
    This will print the pin number, its reported value and
    the date and time when the differential is exceeded
    :param data: [report_type, ADC#, current reported value, timestamp]
    """
    date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data[CB_TIME]))
    # value =
    print(f'ADC Report Type: {data[CB_PIN_MODE]} ADC: {data[CB_PIN]} '
          f'Value: {data[CB_VALUE]} Time Stamp: {date}')


def analog_in(my_board, adc):
    """
     This function establishes the pin as an
     analog input. Any changes on this pin will
     be reported through the call back function.

     :param my_board: a pymata4 instance
     :param adc: ADC number
     """

    # set the pin mode
    my_board.set_pin_mode_analog_input(adc, differential=10, callback=the_callback)

    print('Enter Control-C to quit.')
    # enable neopixel support on the Pico
    my_board.set_pin_mode_neopixel()

    # set some values and the show them
    my_board.neo_pixel_set_value(0, 64, 0, 0)
    my_board.neo_pixel_set_value(1, 0, 64, 0)
    my_board.neo_pixel_set_value(7, 0, 0, 64)
    my_board.neopixel_show()

    time.sleep(1)

    # clear the NeoPixels
    my_board.neopixel_clear()

    time.sleep(1)

    # fill the NeoPixels
    my_board.neopixel_fill(50, 0, 120)

    time.sleep(1)

    # set pixel value and update immediately
    my_board.neo_pixel_set_value(3, 0, 65, 64, True)
    time.sleep(1)

    my_board.neopixel_clear()
    try:
        while True:
            for pixel in range(8):
                my_board.neo_pixel_set_value(pixel, 0, 0, 64, True)
                # time.sleep(.5)
                my_board.neopixel_clear()
                # time.sleep(.2)
    except KeyboardInterrupt:
        board.shutdown()
        sys.exit(0)


board = telemetrix_rpi_pico.TelemetrixRpiPico()

try:
    analog_in(board, ADC)
except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
