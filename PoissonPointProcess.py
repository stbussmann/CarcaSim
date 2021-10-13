#########################################################
#### Poisson Point Process Object                    ####
#### by Stephan Bussmann, University of Osnabrueck   ####
#########################################################


import numpy as np
from scipy.integrate import dblquad
import matplotlib.pyplot as plt

class PoissonPointProcess:

    def __init__(self, window_width, window_height, intensityfunction, number_of_cells_x_axis, number_of_cells_y_axis):

        self.SET = []

        cell_width = window_width/number_of_cells_x_axis
        cell_height = window_height/number_of_cells_y_axis

        for i in range(number_of_cells_x_axis):
            for j in range(number_of_cells_y_axis):

                int, error = dblquad(intensityfunction, i*cell_width, (i+1)*cell_width, lambda x: j*cell_height, lambda x: (j+1)*cell_height)

                points_in_cell = np.random.poisson(int)

                for k in range(points_in_cell):
                    self.SET.append([np.random.uniform(i*cell_width, (i+1)*cell_width), np.random.uniform(j*cell_height, (j+1)*cell_height)])
