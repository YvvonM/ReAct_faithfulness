from tools.calculator import Calculator
from tools.wikipedia import Wikipedia

calc = Calculator()
print(calc.run("52400 * 0.90 * 1.10"))
print(calc.run("(2 * 0.30 - 1 * 0.30) / 2"))
print(calc.run("60/((30/10) + (30/30))"))
print(calc.run("(200 * 0.70 * 0.80) - (200 * 0.50)"))
print(calc.run("(4/11) * (3/10)"))
print(calc.run("what is the speed of light"))

wiki = Wikipedia()
print(wiki.run("Mombasa Nairobi SGR opening date"))
print(wiki.run("Hyperinflation in Zimbabwe"))
