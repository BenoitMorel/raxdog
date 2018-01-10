
import random

class SVGWriter:
  def __init__(self, filename):
    self.f = open(filename, "w")
    self.f.write("<svg  xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n")

  def drawRec(self, x, y, width, height):
    if (width < 0 or height < 0):
      print("Warning: trying to draw a svg rectangle with negative width or height")
      return
    color = hex(random.randrange(0, 16777216))[2:]
    self.f.write("  <rect x=\"" + str(x) + "\" y=\"" + str(y) + "\" ")
    self.f.write("height=\"" + str(height) + "\" width=\"" + str(width) + "\" ")
    self.f.write("style=\"fill: #"+ color + "\"/>\n")
    pass


  def close(self):
    self.f.write("</svg>\n")


#plop = SVGWriter("results/dataexample/multi-raxml.svg")
#plop.drawRec(0, 0, 100, 100)
#plop.drawRec(100, 0, 100, 100)
##plop.drawRec(0, 100, 200, 100)
#plop.close()
