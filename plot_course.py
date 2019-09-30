#!/usr/bin/env python3

import time, sys
from course import Course
from geoparse import GeoParse

# Filename with course data
course_file = "course.dat"

gp = GeoParse(course_file)
c = Course(gp.get_points())

c.init_plot()

gp.smooth()
c.add_curve(gp.get_points())

input("Press enter to close")
