
import random

class SVGWriter:
  def __init__(self, filename):
    self.f = open(filename, "w")
    self.f.write("<svg  xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n")

  def drawRec(self, x, y, width, height, text):
    print("gene " + text)
    if (width < 0 or height < 0):
      print("Warning: trying to draw a svg rectangle with negative width or height")
      return
    
    self.f.write("  <svg x=\"" + str(x) + "\" y=\"" + str(y) + "\" ")
    self.f.write("height=\"" + str(height) + "\" width=\"" + str(width) + "\" >\n")
    
    color = hex(random.randrange(0, 16777216))[2:]
    self.f.write("    <rect x=\"0%\" y=\"0%\" height=\"100%\" width=\"100%\" style=\"fill: #")
    self.f.write(color + "\"/>\n")

    self.f.write("   <text x=\"50%\" y=\"50%\" alignment-baseline=\"middle\" text-anchor=\"middle\">")
    self.f.write(text)
    self.f.write("</text>\n" )

    self.f.write("  </svg>\n")
    
    pass


  def close(self):
    self.f.write("</svg>\n")


#plop = SVGWriter("results/dataexample/multi-raxml.svg")
#plop.drawRec(0, 0, 100, 100)
#plop.drawRec(100, 0, 100, 100)
#plop.drawRec(0, 100, 200, 100)
#plop.close()
