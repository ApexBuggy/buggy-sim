# Script for parsing data scraped from Caltopo into
# longitude, latitude, and altitude (m)
# To get this data, open map on Caltopo and draw path. Open the browser
# developer tools (Ctrl+shift+c or F12, usually) and look at Network.
# Right-click on path and select profile. A network request called "pointstats"
# will be generated. Select that and copy the results field within.
import re

class GeoParse:
    def __init__(self, file_name):
        # Point : (long, lat, elev)
        self.points = []

        # Matches entries of the form
        # 1: [-79.94166075723936, 40.44156124125338, 289.3372409255437
        pt_match = re.compile(r'\d+:\s*\[([-.\d]+),\s*([-.\d]+),\s*([-.\d]+)')

        with open(file_name, "r") as f:
            for l in f:
                m = pt_match.match(l)
                self.points.append((float(m.group(1)),
                                    float(m.group(2)),
                                    float(m.group(3))))

    # Smooth the data
    # Window is the number of data points in averaging window
    def smooth(self, window = 5):
        self.smooth_range(range(len(self.points)), window)

    # Smooth the data in a range
    # Window is the number of data points in averaging window,
    # idx_range is the range of indices to smooth (incl. low, excl. high)
    def smooth_range(self, idx_range, window):
        assert len(idx_range) > window, \
            "Range must be at least as large as window"
        assert window % 2 == 1, \
            "window must be odd"

        # Array of smoothed points, temp storage before in-place replacement
        new_pts = []

        # New point is the average of the window points surrounding that index
        # If that window would go outside of idx_range, clip the window on
        #   both ends (to prevent discontinuities when two ranges join)

        # Example
        # Window 5, range [3, 10)
        #       3 4 5
        #     3 4 5 6 7
        #   3 4 5 6 7 8 9
        #     5 6 7 8 9
        #       7 8 9
        #
        # / 1 3 5 5 5 3 1

        # Smooth the opening of the window
        for i in range(window // 2):
            new_pt = [0,0,0] # Sum of points in window
            count = 2 * i + 1

            for p in self.points[idx_range.start:idx_range.start + 2 * i + 1]:
                for component in range(len(p)):
                    new_pt[component] += p[component]

            new_pts.append((new_pt[0]/count, new_pt[1]/count, new_pt[2]/count))

        # Smooth the middle
        for i in range(idx_range.start + window // 2,
                       idx_range.stop - window // 2):
            new_pt = [0,0,0] # Sum of points in window
            count = window

            for p in self.points[i - window // 2:i + window // 2 + 1]:
                for component in range(len(p)):
                    new_pt[component] += p[component]

            new_pts.append((new_pt[0]/count, new_pt[1]/count, new_pt[2]/count))

        # Smooth the closing of the window
        for i in reversed(range(window // 2)):
            new_pt = [0,0,0] # Sum of points in window
            count = 2 * i + 1

            for p in self.points[idx_range.stop - 2*i - 1:idx_range.stop]:
                for component in range(len(p)):
                    new_pt[component] += p[component]

            new_pts.append((new_pt[0]/count, new_pt[1]/count, new_pt[2]/count))

        # We should create exactly as many points as are in the range
        assert(len(new_pts) == len(idx_range))
        for i in range(len(new_pts)):
            self.points[idx_range.start + i] = new_pts[i]

    # Remove everything but local minima and maxima
    def only_extremes(self):
        new_pts = []

        for i in range(len(self.points)):
            # Only uses altitude
            alt = self.points[i][2]

            if i == 0 or i + 1 == len(self.points):
                # Always keep endpoints
                new_pts.append(self.points[i])

            elif ((self.points[i-1][2] <= alt > self.points[i+1][2]) or
                  (self.points[i-1][2] >= alt < self.points[i+1][2])):
                # Also maxima/minima. Only use the last point when duplicated
                new_pts.append(self.points[i])

        original_idxs = [self.points.index(p) for p in new_pts]

        self.points = new_pts
        print("{} extremes at indices {}".format(len(self.points), original_idxs))

    def get_points(self):
        return self.points
