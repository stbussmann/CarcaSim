import numpy as np
import shapely.geometry as sh
import shapely.affinity as sha
import matplotlib.pyplot as plt

class Map:

    # a Carcassonnemap is a n times m matrix

    def __init__(self, map_height, map_width, cell_side_length, outradius, inradius, RDS):

        self.RDS = RDS
        self.cell_side_length = cell_side_length

        #store measurements so that the BooleanModel can access them from map
        self.width = map_width
        self.height = map_height
        self.area = map_height * map_width

        self.n = map_height // cell_side_length
        self.m = map_width // cell_side_length

        if map_height % cell_side_length != 0:
            self.n += 1
        if map_width % cell_side_length != 0:
            self.m += 1

        self.carc_map = []

        for i in range(int(self.n)):
            self.carc_map.append([])
            for j in range(int(self.m)):
                self.carc_map[i].append(self._make_shape(inradius, outradius))

    def _make_shape(self, inradius, outradius):

        # 32 segments with radian 1/32 * 2pi
        segment = np.pi / 16.0

        points = []

        for i in range(32):

            angle = self.RDS.uniform(i * segment, (i + 1) * segment)
            distance = self.RDS.uniform(inradius, outradius)

            points.append([distance * np.cos(angle), distance * np.sin(angle)])

        return sh.Polygon(points)

    def get_shape(self, x, y):

        return self.carc_map[int(x // self.cell_side_length)][int(y // self.cell_side_length)]


class BooleanModel:

    def __init__(self, _set_of_nodes, _map):

        self.number_of_nodes = len(_set_of_nodes)
        self.set_of_nodes = _set_of_nodes

        self.map = _map
        self.model = []

        for point in self.set_of_nodes:
            x = point[0]
            y = point[1]
            self.model.append(sha.translate(_map.get_shape(x, y), x, y))

    def volume(self):

        _set = self.model[0]

        for set in self.model:
            _set = _set.union(set)

        vol = _set.area

        return vol

    def isolated_nodes(self):
        iso = 0
        for i in range(len(self.model)):
            is_isolated = True

            for j in range(i + 1, len(self.model)):
                if self.model[i].intersects(self.model[j]):
                    is_isolated = False

            if is_isolated:
                iso += 1

        return iso

    def number_of_components(self):

        #create graph

        V = self.set_of_nodes
        E = []

        for i in range(0, len(V)):
            for j in range(i+1, len(V)):

                # x = sh.Point(V[i][0], V[i][1])
                # y = sh.Point(V[j][0], V[j][1])

                #if(x.within(self.model[j]) and y.within(self.model[j])):
                #    E.append([i,j])
                if self.map.get_shape(V[i][0], V[i][1]).intersects(self.map.get_shape(V[j][0], V[j][1])):
                    E.append([i, j])

        # compute connected components
        if len(E)==0:
            return self.number_of_nodes

        else:

            M = np.zeros((len(V), len(E)))

            i = 0
            for edge in E:
                M[edge[0] - 1][i] = -1
                M[edge[1] - 1][i] = 1
                i += 1

            if len(E) != 0:
                _number_of_components = len(V) - np.linalg.matrix_rank(M)
            else:
                _number_of_components = len(V)

            return _number_of_components

    def draw(self):

        # plot grid
        grid_ticks_x = []
        grid_ticks_y = []

        for i in range(1, int(self.map.n)):
            grid_ticks_y.append(i * self.map.cell_side_length)
        for j in range(1, int(self.map.m)):
            grid_ticks_x.append(j * self.map.cell_side_length)

        plt.hlines(grid_ticks_y, 0, self.map.height, linestyles='dotted', colors='grey')
        plt.vlines(grid_ticks_x, 0, self.map.width, linestyles='dotted', colors='grey')

        # plot nodes
        x_nodes = []
        y_nodes = []

        for point in self.set_of_nodes:
            x_nodes.append(point[0])
            y_nodes.append(point[1])

        plt.plot(x_nodes, y_nodes, 'ro', markersize=1)

        # plot shapes
        for polygon in self.model:
            plt.plot(*polygon.exterior.xy, 'black', linewidth=0.75)

        plt.show()
