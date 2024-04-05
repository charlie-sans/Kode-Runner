import termplotlib as tpl
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(5*x) * x+3
fig = tpl.figure()
fig.plot(x, y, width=200, height=70)
fig.show()