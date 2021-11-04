# CarcaSim

Provides objects necessary to reproduce the results presented in the addendum to my doctoral thesis.

# carcassonne.py

Required Packages: NumPy (https://numpy.org/), Shapely (https://github.com/Toblerity/Shapely) and Matplotlib (https://matplotlib.org/).

Contains classes for our random map generator and the creation of a Boolean model on this map. 

class Map: Expects (in that order) height and width of the map to be created, side length of a cell, outradius, inradius and a numpy.random.RandomState object. This is needed to ensure randomness when using multiple threads.

class BooleanModel: Expects (in that order) a set of nodes (that is a list of lists each containing a x and y coordinate) and a Map object. The user should ensure that the coordinates of the nodes are contained within the limits of the given map. A BooleanModel object admits the following functions:

   - volume() returns the covered volume of the Boolean model.

   - isolated_nodes() returns the number of isolated nodes in the Boolean model.

   - draw() visualizes the model using Matplotlib.

# poissonpointprocess.py

Required Packages: NumPy (https://numpy.org/) and SciPy (https://scipy.org/).

Contains the class needed to simulate a Poisson point process as laid out in the thesis.

class PoissonPointProcess: Expects (in that order) height and width of the observation window, the intensity function (given in a form that can be handled by scipy.integrate.dblquad), number of cells on the x-axis and number of cells on the y-axis. Has the attribute SET, which gives a list of the created coordinates.

# booleanmodel.py

Required Packages: NumPy (https://numpy.org/), Shapely (https://github.com/Toblerity/Shapely) and Matplotlib (https://matplotlib.org/).

Contains classes for the creation of a spherical Boolean model with fixed communication radius on a stationary Poisson point process. A BooleanModel object admits the following functions:

class BooleanModel: Expects (in that order) height and width of the observation window, intensity of the process and the radius. A BooleanModel object admits the following functions:

   - percolates() returns True if the created model contains a left-right crossing component. False otherwise.
   - draw() visualizes the model using Matplotlib.
