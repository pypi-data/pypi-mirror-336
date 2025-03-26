import sys
import time
from telemetrix_rpi_pico import telemetrix_rpi_pico

# The GPIO pin number for the built-in LED
BOARD_LED = 25

# LED States
ON = 1
OFF = 0

# instantiate the library
board = telemetrix_rpi_pico.TelemetrixRpiPico()

# Set the DIGITAL_PIN as an output pin
board.set_pin_mode_digital_output(BOARD_LED)

try:
    while True:
        # turn led on
        board.digital_write(BOARD_LED, ON)
        time.sleep(1)
        # turn led off
        board.digital_write(BOARD_LED, OFF)
        time.sleep(1)

except KeyboardInterrupt:
    board.shutdown()
    sys.exit(0)
