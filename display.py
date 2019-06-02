import time
import os
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0
PADDING = -2
TOP = PADDING

# Load default font.
FONT = ImageFont.load_default()

# Move left to right keeping track of the current x position for drawing shapes.
X = 0
height, width = 0, 0


class Display:

    def __init__(self):
        self.disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)
        self.height = self.disp.height
        self.width = self.disp.width
        self.image = Image.new('1', (self.width, self.height))

        # Initialize library.
        self.disp.begin()

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def clear(self):
        self.disp.clear()
        self.disp.display()

    def draw_text(self, text):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Write two lines of text.
        self.draw.text((X, TOP), text, font=FONT, fill=255)
        self.disp.image(self.image)
        self.disp.display()


if __name__ == '__main__':
    # Test the display module
    pioled = Display()
    pioled.draw_text('Hello world!')
    os.system("pause")
