# CarcaSim

Provides objects necessary to reproduce the results presented in the addendum to my doctoral thesis.

# carcassonne.py

Required Packages: NumPy (https://numpy.org/), Shapely (https://github.com/Toblerity/Shapely) and Matplotlib (https://matplotlib.org/).

Contains classes for our random map generator and the creation of a Boolean model on this map. 

class Map: Expects (in that order) height and width of the map to be created, side length of a cell, outradius, inradius and a numpy.random.RandomState object. This is needed to ensure randomness when using multiple threads.

class BooleanModel: Expects a set of nodes (that is a list of lists each containing a x and y coordinate) and a Map object. The user should ensure that the coordinates of the nodes are contained within the limits of the given map. A BooleanModel object admits the following functions:

volume() returns the covered volume of the Boolean model.

isolated_nodes() returns the number of isolated nodes in the Boolean model.

draw() visualizes the model using Matplotlib.
