#!/usr/bin/env python3

import time, sys
from course import Course
from geoparse import GeoParse

# Filename with course data
course_file = "course.dat"

gp = GeoParse(course_file)
c = Course(gp.get_points())

c.init_plot(show_course = False)
c.add_curve(gp.get_points(), "course")

# gp.smooth(23)
# c.add_curve(gp.get_points(), "smoothed")

# gp.only_extremes()
# c.add_curve(gp.get_points(), "extremes")

input("Press enter to close")
