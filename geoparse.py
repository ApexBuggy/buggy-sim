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

    def get_points(self):
        return self.points
