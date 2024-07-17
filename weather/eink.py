from PIL import Image, ImageDraw, ImageFont, ImageColor
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)
tmpdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'temp_image')

import logging
from waveshare_epd import epd4in01f
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.INFO)

def convert_color(image):

    palette_7c = []
    palette_7c.extend((0, 0, 0))        # BLACK
    palette_7c.extend((255, 255, 255))  # WHITE
    palette_7c.extend((0, 128, 0))      # GREEN
    palette_7c.extend((31, 119, 180))   # BLUE
    palette_7c.extend((213, 39, 40))    # RED
    palette_7c.extend((255, 255, 0))    # YELLOW
    palette_7c.extend((255, 165, 0))    # ORANGE

    original = Image.open(image)
    original.convert('P')
    pal_image = Image.new("P", (1, 1))
    pal_image.putpalette(palette_7c)
    quantized = original.quantize(palette=pal_image)
    quantized.convert('P')
    quantized.save(tmpdir + '/quantized.bmp')
    # quantized.show()

    epd = epd4in01f.EPD()
    epd_palette = []
    epd_palette.extend((0x00, 0x00, 0x00))  # epd.BLACK
    epd_palette.extend((0xff, 0xff, 0xff))  # epd.WHITE
    epd_palette.extend((0x00, 0xff, 0x00))  # epd.GREEN
    epd_palette.extend((0x00, 0x00, 0xff))  # epd.BLUE
    epd_palette.extend((0xff, 0x00, 0x00))  # epd.RED
    epd_palette.extend((0xff, 0xff, 0x00))  # epd.YELLOW
    epd_palette.extend((0xff, 0x80, 0x00))  # epd.ORANGE

    epd_image = Image.new("P", (1, 1))
    epd_image.putpalette(epd_palette)
    quantized.convert('RGB')
    # quantized.show()

    converted = Image.new('P', (original.size[0], original.size[1]))

    for i in range(quantized.size[0]):
        for j in range(quantized.size[1]):
            c = quantized.getpixel((i, j))
            converted.putpixel((i, j),
                               (epd_palette[0 + c*3], epd_palette[1 + c*3], epd_palette[2 + c*3]))
    # converted.show()

    converted.save(tmpdir + '/converted.png')
    return tmpdir + '/converted.png'


def show(image):
    epd = epd4in01f.EPD()

    logging.info("epd4in01f init")
    epd.init()

    logging.info(image)
    himage = Image.open(image)
    himage = himage.rotate(180)
    epd.display(epd.getbuffer(himage))
    time.sleep(3)

    logging.info("Goto Sleep...")
    epd.sleep()

    return 0

def clear():
    epd = epd4in01f.EPD()

    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(3)

    logging.info("Goto Sleep...")
    epd.sleep()

    return 0

