#! /usr/bin/env python

# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel
# Backlight: Enhanced by TOMDENKT - backlight control (on/off)
# Backlight: lcd_backlight(1) = ON, lcd_backlight(0) = OFF
# Backlight: Usage, if lcddriver is set to "display" (like example below)
# Backlight: display.lcd_backlight(0) # Turn backlight off
# Backlight: display.lcd_backlight(1) # Turn backlight on

# If drivers/i2c_dev.py is NOT in same folder with your scripts,
# uncomment below and set path to i2c_dev, e.g. "/home/pi/lcd"
# import sys
# sys.path.append("/home/pi/lcd")

# Import necessary libraries for communication and display use
from lcd_16x2 import drivers
from time import sleep

import sys

if sys.platform != "linux" or "raspberry" not in sys.platform:
    print("Warning: This script uses 'smbus', which is specific to Raspberry Pi.")
    print("You are on a different system (Windows, macOS, etc.). The demo will not function as expected.")
    print("Please try running this script on a Raspberry Pi for full functionality or use demo_emulator.py instead.")
    sys.exit(1)


# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first
display = drivers.Lcd()

# Main body of code
try:
    print("Press CTRL + C to quit program")
    while True:
        # Remember that your sentences can only be 16 characters long!
        print("Loop: Writing to display and toggle backlight...")
        display.lcd_backlight(1)                          # Make sure backlight is on / turn on
        sleep(0.5)                                        # Waiting for backlight toggle
        display.lcd_backlight(0)                          # Turn backlight off
        sleep(0.5)                                        # Waiting for turning backlight on again
        display.lcd_backlight(1)                          # Turn backlight on again
        sleep(1)                                          # Waiting for text
        display.lcd_display_string("Demo Backlight", 1)   # Write line of text to first line of display
        display.lcd_display_string("Control ON/OFF", 2)   # Write line of text to second line of display
        sleep(2)                                          # Waiting for backlight toggle
        display.lcd_backlight(0)                          # Turn backlight off
        sleep(0.5)                                        # Waiting for turning backlight on again
        display.lcd_backlight(1)                          # Turn backlight on again
        sleep(0.5)                                        # Waiting for turning backlight off again
        display.lcd_backlight(0)                          # Turn backlight off
        sleep(0.5)                                        # Waiting for turning backlight on again
        display.lcd_backlight(1)                          # Turn backlight on again
        sleep(2)                                          # Give time for the message to be read
        display.lcd_display_string("I am a display! ", 1) # Refresh the first line of display with a different message
        display.lcd_display_string("Demo Backlight", 2)   # Refresh the second line of display with a different message
        sleep(2)                                          # Give time for the message to be read
        display.lcd_clear()                               # Clear the display of any data
        sleep(1)                                          # Give time for the message to be read
        display.lcd_backlight(0)                          # Turn backlight off
        sleep(1.5)                                        # Waiting until restart
except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press CTRL + C), exit the program and cleanup
    print("Exit and cleaning up!")
    display.lcd_clear()
    # Make sure backlight is on / turn on by leaving
    display.lcd_backlight(1)
