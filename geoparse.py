# Script for parsing data scraped from Caltopo into
# longitude, latitude, and altitude (m)
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
        total = [0,0,0] # Running sum of data
        count = 0       # Number of data points in total

        new_pts = []

        # Begin with the first half of the window
        for i in range(window//2 + 1):
            p = self.points[i]
            total[0] += p[0]
            total[1] += p[1]
            total[2] += p[2]
            count += 1

        for i in range(len(self.points)):
            if i - window//2 >= 0:
                # Remove a point
                p = self.points[i - window//2]
                total[0] -= p[0]
                total[1] -= p[1]
                total[2] -= p[2]
                count -= 1
            if i + window//2 < len(self.points):
                p = self.points[i + window//2]
                total[0] += p[0]
                total[1] += p[1]
                total[2] += p[2]
                count += 1

            new_pts.append((total[0]/count, total[1]/count, total[2]/count))

        self.points = new_pts

    def get_points(self):
        return self.points
