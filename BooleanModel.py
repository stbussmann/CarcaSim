#################################################
#### percolation test program                ####
#### by Stephan Bussmann                     ####
####                                         ####
#### Contains a Boolean model object realized####
#### by using Shapely and offers methods for #### 
#### its analysis                            ####
#################################################

import numpy as np
import matplotlib.pyplot as plt

from shapely.geometry import Point as shPoint
from shapely.geometry import LineString


class Point:

    def __init__(self, x, y, index):

        self.x = x
        self.y = y
        self.index = index

    def distance_to(self, other_point):

        distance = np.sqrt((self.x - other_point.x)**2 + (self.y - other_point.y)**2)
        return distance


class BooleanModel:

    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, POINT_INTENSITY, COMM_RADIUS):

        self.number_of_points = int(POINT_INTENSITY * WINDOW_WIDTH * WINDOW_HEIGHT)

        self.x_min = -WINDOW_WIDTH/2.0
        self.x_max = WINDOW_WIDTH/2.0

        self.y_min = -WINDOW_HEIGHT/2.0
        self.y_max = WINDOW_HEIGHT/2.0

        self.radius = COMM_RADIUS

        #The following two represent vertices and edges in the graph structure.
        #Edges are encoded by the indices of points.
        self.set_of_points = []
        self.set_of_connections = []

        for index in range(self.number_of_points):

            this_point = Point(np.random.uniform(self.x_min, self.x_max), np.random.uniform(self.y_min, self.y_max), index)
            self.set_of_points.append(this_point)

            for other_point in self.set_of_points:

                if this_point.distance_to(other_point) <= 2*COMM_RADIUS:
                    self.set_of_connections.append([this_point.index, other_point.index])

    def shape_components(self):

        Z = shPoint(self.set_of_points[0].x, self.set_of_points[0].y).buffer(self.radius)

        for index in range(1, len(self.set_of_points)):

            Z = Z.union(shPoint(self.set_of_points[index].x, self.set_of_points[index].y).buffer(self.radius))


        return Z

    def number_of_components(self):

        M = np.zeros((len(self.set_of_points), len(self.set_of_connections)))
        i = 0
        for edge in self.set_of_connections:
            M[edge[0] - 1][i] = -1
            M[edge[1] - 1][i] = 1
            i += 1

        if len(self.set_of_connections) != 0:
            number_of_components = len(self.set_of_points) - np.linalg.matrix_rank(M)
        else:
            number_of_components = len(self.set_of_points)

        return number_of_components

    def percolates(self):

        percolates = False

        left_border = LineString([(self.x_min,self.y_min),(self.x_min,self.y_max)])
        right_border = LineString([(self.x_max,self.y_min),(self.x_max,self.y_max)])

        Z = self.shape_components()

        if Z.geom_type == 'MultiPolygon':
            for component in Z:
                if left_border.intersects(component) and right_border.intersects(component):
                    percolates = True
                    break;
        else:
            if left_border.intersects(Z) and right_border.intersects(Z):
                percolates = True

        return percolates

    def draw(self):

        Z = self.shape_components()

        for point in self.set_of_points:
            plt.scatter(point.x, point.y, color='black')

        if Z.geom_type == 'MultiPolygon':
            for component in Z:
                plt.plot(*component.exterior.xy, color='blue')
        else:
            plt.plot(*Z.exterior.xy, color='blue')

        for edge in self.set_of_connections:
            p1 = self.set_of_points[edge[0]]
            p2 = self.set_of_points[edge[1]]
            plt.plot((p1.x, p2.x), (p1.y, p2.y), color='red')

        plt.xlim(self.x_min, self.x_max)
        plt.ylim(self.y_min, self.y_max)
        plt.show()
