import termplotlib as tpl
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(6*x) * 55
fig = tpl.figure()
fig.plot(x, y, width=60, height=20)
fig.show()