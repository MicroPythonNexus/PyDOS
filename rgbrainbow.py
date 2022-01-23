# Rainbow algorithm adapted from
# https://learnembeddedsystems.co.uk/using-the-rgb-led-on-the-arduino-nano-rp2040-connect

import time
import sys
from pydos_ui import Pydos_ui

if sys.implementation.name.upper() == 'CIRCUITPYTHON':
    import neopixel
    import board

    if 'NEOPIXEL' not in dir(board):
        try:
            import cyt_mpp_board as board
            foundBoard = True
        except:
            foundBoard = False

        if not foundBoard:
            if board.board_id == "raspberry_pi_pico":
                try:
                    import kfw_pico_board as board
                except:
                    pass
            else:
                try:
                    import kfw_s2_board as board
                except:
                    pass

    pixels = neopixel.NeoPixel(board.NEOPIXEL, 1)

elif sys.implementation.name.upper() == 'MICROPYTHON':
    import machine
    from os import uname
    if uname().machine == 'TinyPICO with ESP32-PICO-D4':
        from micropython_dotstar import DotStar
        spi = machine.SPI(sck=machine.Pin(12), mosi=machine.Pin(13), miso=machine.Pin(18))
        pixels = DotStar(spi, 1)
    elif uname().machine == 'SparkFun Thing Plus RP2040 with RP2040':
        import neopixel
        pixels = neopixel.NeoPixel(machine.Pin(8), 1)
    elif uname().machine == 'Raspberry Pi Pico with RP2040':
        import neopixel
        pixels = neopixel.NeoPixel(machine.Pin(28), 1)


rgbValues = [255,0,0]
upIndex = 0
downIndex = 1
cmnd = ""

# Cycle colours.
print("listening... 'q' to quit")

while cmnd.upper() != "Q":

    if Pydos_ui.serial_bytes_available():
        cmnd = Pydos_ui.read_keyboard(1)

    rgbValues[upIndex] += 1
    rgbValues[downIndex] -= 1

    if rgbValues[upIndex] > 255:
        rgbValues[upIndex] = 255
        upIndex = (upIndex + 1) % 3

    if rgbValues[downIndex] < 0:
        rgbValues[downIndex] = 0
        downIndex = (downIndex + 1) % 3

    if cmnd.upper() == "Q":
        rgbValues[0] = 0
        rgbValues[1] = 0
        rgbValues[2] = 0

    if sys.implementation.name.upper() == 'CIRCUITPYTHON':
        pixels.fill((rgbValues[1], rgbValues[2], rgbValues[0]))
        time.sleep(0.005)
    elif sys.implementation.name.upper() == 'MICROPYTHON':
        if uname().machine == 'TinyPICO with ESP32-PICO-D4':
            pixels.fill((rgbValues[1], rgbValues[2], rgbValues[0]))
            time.sleep(0.005)
        else:
            pixels[0] = (rgbValues[1], rgbValues[2], rgbValues[0])
            pixels.write()
            time.sleep(0.005)

try:
    pixels.deinit()
except:
    pass
