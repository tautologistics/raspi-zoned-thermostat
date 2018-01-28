import os
import time
import sys
from PIL import ImageFont

from luma.core import cmdline, error
from luma.core.render import canvas

class Display(object):

  device = None
  line_height = None
  font = None

  def __init__(self):
    self.line_height = 16
    self.font = ImageFont.truetype(
      os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts', 'C&C Red Alert [INET].ttf')),
      self.line_height,
    )
    self.load_device()
    self.write_lines([
      'Line 1',
      'Line 2',
      'Line 3',
      'Line 4',
    ])

  def __enter__(self):
    pass

  def __exit__(self, type, value, traceback):
    self.close()

  def load_device(self):
    self.close()

    parser = cmdline.create_parser(description='default')
    args = parser.parse_args([])
    try:
        self.device = cmdline.create_device(args)
    except error.Error as e:
        print('ERROR: ', parser.error(e))

  def write_lines(self, lines):
    with canvas(self.device) as draw:
      line = 0
      draw.text((0, line), lines[0], font=self.font, fill='white')
      line += self.line_height
      draw.text((0, line), lines[1], font=self.font, fill='white')
      line += self.line_height
      draw.text((0, line), lines[2], font=self.font, fill='white')
      line += self.line_height
      draw.text((0, line), lines[3], font=self.font, fill='white')
      line += self.line_height

  def close(self):
    if self.device:
      self.device.clear()
      self.device = None
