import subprocess
from PIL import ImageGrab
import Quartz

image = ImageGrab.grab(include_layered_windows=True)
position = Quartz.NSEvent.mouseLocation()
pX = int(position.x * 2)
pY = int(image.height - position.y * 2)
pixels = image.load()
color = pixels[pX, pY]
subprocess.run("pbcopy", universal_newlines=True, input='#%02x%02x%02x' % (color[0], color[1], color[2]))
