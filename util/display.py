import time
import os

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
PADDING = -2
TOP = PADDING
WIDTH = 128
HEIGHT = 32

# Load default font.
FONT = ImageFont.load_default()

# Move left to right keeping track of the current x position for drawing shapes.
X = 0
height, width = 0, 0


class Display:

    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
        self.height = self.disp.height
        self.width = self.disp.width
        self.image = Image.new('1', (self.width, self.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def clear(self):
        self.disp.clear()
        self.disp.display()

    def draw_text(self, lines):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        margin_top = TOP
        # Write two lines of text.
        for line in lines:
            self.draw.text((X, margin_top), line, font=FONT, fill=255)
            margin_top += 8

        self.disp.image(self.image)
        self.disp.show()


if __name__ == '__main__':
    # Test the display module
    pioled = Display()
    pioled.draw_text('Hello world!')
    os.system("pause")
