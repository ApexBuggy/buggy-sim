import geopy.distance
import matplotlib.pyplot as plt

# This import registers the 3D projection, but is otherwise unused.
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

# Returns the slope (altitude / d) between points of the form (d,lat,long,alt)
def slope(p0, p1):
    return (p1[3] - p0[3]) / (p1[0] - p0[0])

# Representation of the buggy course
class Course:
    # points is formatted as [(d0,lat0,long0,alt0), (d1,lat1,long1,alt1), ...]
    # dN represents distance from the start along the course, like t in a
    # parameterized curve.
    points = None

    # Initialized by a series of points (latitude, longitude, altitude (m))
    # REQUIRES: points is in course order and has no points with the same
    #           coordinates
    def __init__(self, points):
        assert(len(points) >= 2)
        self.points = []

        # Cumulative distance
        d = 0.
        last_p = points[0]
        for p in points:
            d += geopy.distance.distance(p, last_p).m
            self.points.append((d, p[0], p[1], p[2]))
            last_p = p

        print("Total course distance (m): ", d)

        # Index of the last point accessed, used for optimization
        self.last_idx = 0

    # Returns the point at a given distance along the course
    def point_at(self, d):
        if(d < self.points[0][0] or d > self.points[-1][0]):
            print("Invalid d to get_point:", d)
            return None
        else:
            # Search for the index of the first point with distance > d
            idx = 0

            # Optimize by checking last-used point first.
            # TODO: Optimize further, e.g. check next point as well
            if(self.last_idx > 0 and
               self.points[self.last_idx - 1][0] < d and
               self.points[self.last_idx][0] >= d):
                idx = self.last_idx
            else:
                # TODO: binary search
                while(idx + 1 < len(self.points) and self.points[idx][0] <= d):
                    idx += 1

                self.last_idx = idx

            # assert(self.points[idx][0] > d or idx == len(self.points) - 1)
            # assert(self.points[idx-1][0] <= d)

            weight = ((d - self.points[idx - 1][0]) /
                      (self.points[idx][0] - self.points[idx - 1][0]))
            # assert(0 <= weight <= 1)

            return tuple([(1 - weight) * self.points[idx - 1][i] +
                          weight * self.points[idx][i] for i in range(4)])

    # Returns the slope at a given distance along the course
    # At a point, the slope of the preceding line segment is used,
    # except for at the first point, where it is the slope of the following line
    def slope_at(self, d):
        if(d < self.points[0][0] or d > self.points[-1][0]):
            print("Invalid d to get_slope:", d)
            return None
        elif(d == self.points[0][0]): # Float == ok, only for exact cases anyway
            return slope(self.points[0], self.points[1])
        else:
            idx = 0

            # Optimize by checking last-used point first.
            # TODO: Optimize further, e.g. check next point as well
            if(self.last_idx > 0 and
               self.points[self.last_idx - 1][0] < d and
               self.points[self.last_idx][0] >= d):
                idx = self.last_idx
            else:
                # TODO: binary search
                while(idx + 1 < len(self.points) and self.points[idx][0] < d):
                    idx += 1
                self.last_idx = idx

            # assert(self.points[idx][0] > d or idx == len(self.points) - 1)
            # assert(self.points[idx-1][0] <= d)

            return slope(self.points[idx - 1], self.points[idx])

    # Initialize the visualization plot and graph the course
    def init_plot(self):
        plt.rcParams['legend.fontsize'] = 10
        self.axes = plt.figure().gca(projection='3d')

        x = [(pt[1]) for pt in self.points] # Latitude
        y = [(pt[2]) for pt in self.points] # Altitude
        z = [(pt[3]) for pt in self.points] # Longitude

        self.axes.plot(x, y, z, label='parametric curve')
        self.axes.legend()

    # Plot the new position of the buggy on the visualization
    def update_plot(self, buggy):
        # Remove the old buggy marker
        if(len(self.axes.lines) == 2): # One for course, one for buggy
            l = self.axes.lines.pop(1)
            del l

        # Plot a new buggy marker
        buggy_pt = self.point_at(buggy.dist)
        self.axes.plot([buggy_pt[1]],[buggy_pt[2]],[buggy_pt[3]], color="orange", marker="o")

        plt.draw()
        plt.pause(0.001)
