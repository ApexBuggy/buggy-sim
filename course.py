def slope(p0, p1):
    return (p1[1] - p0[1]) / (p1[0] - p0[0])

# Representation of the buggy course
class Course:
    points = None # [(x0,y0), (x1,y1), ...]

    # Initialized by a series of points (x,y)
    # TODO: support a 3D course
    # REQUIRES: points is sorted by x-coordinate and has no points with the same
    #           x-coordinate
    def __init__(self, points):
        assert(len(points) >= 2)
        self.points = points

    # Returns the slope at a given x-coordinate
    # At a point, the slope of the preceding line segment is used,
    # except for at the first point, where it is the slope of the following line
    def slope_at(self, x):
        # TODO: optimize
        if(x < self.points[0][0] or x > self.points[-1][0]):
            print("Invalid x to get_slope:", x)
            return None
        elif(x == self.points[0][0]): # Float == ok, only for exact cases anyway
            return slope(self.points[0], self.points[1])
        else:
            idx = 0
            while(idx + 1 < len(self.points) and self.points[idx][0] < x):
                idx += 1
            return slope(self.points[idx - 1], self.points[idx])
