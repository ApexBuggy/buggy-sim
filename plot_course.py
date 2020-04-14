#!/usr/bin/env python3

# Standalone script for visualizing the course
# I created this for testing GeoParse and messing around with
# specific course parameters. Hack away!

import time, sys
from course import Course
from geoparse import GeoParse

# Filename with course data
course_file = "course.dat"

gp = GeoParse(course_file)
c = Course(gp.get_points())
c.init_plot(show_course = False)

# Show the un-smoothed course
c.add_curve(gp.get_points(), "raw")

# Hill 1 to a little way down the steepest part of the free roll,
# less smoothed so the top of the hill doesn't lower (and because
# the data at the beginning of the course is more smooth)
gp.smooth_range(range(0, 56), 7)

# Slight overlap with previous to smooth the boundary (which is
# sketchy because smoothing is not associative). Smooth until the
# end. Pulls the chute turn in a little bit more than is probably
# realistic (turn is more gradual than it should be), and doesn't
# quite smooth the end of hill 5. This part of the data is much
# noisier, so more smoothing is required
gp.smooth_range(range(48, len(gp.points)), 17)

# Show the smoothed course
c.add_curve(gp.get_points(), "smoothed")

# A good way to figure out if the course is smoothed enough it to
# only view the local extremes - points that are local maxima or
# minima
gp.only_extremes()
c.add_curve(gp.get_points(), "extremes")

input("Press enter to close")
