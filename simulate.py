#!/usr/bin/env python3

import time, sys
from course import Course
from geoparse import GeoParse
import buggy

#####################
# SIMULATION CONFIG #
#####################

# Delta Time used by simulation
DT = 2**(-12)

# Time between updating the plot
disp_tick = 0.2

# Filename with course data
course_file = "course.dat"

###################
# SIMULATION CODE #
###################

gp = GeoParse(course_file)
c = Course(gp.get_points())

Fg = buggy.Gravity_Force()

# 55 kg ~ 120 lbs
b = buggy.Buggy(mass = 55, velocity = 0, distance = 180)
b.add_force(Fg)

c.init_plot()

t = 0                    # Simulation time
start_time = time.time() # Clock time of simulation start
last_t = 0               # Last simulation time that was displayed

while(t < 150):
    b.update(DT, c.slope_at(b.dist))
    t += DT
    if(t >= last_t + disp_tick):
        # Time when the next display should occur
        next_disp = start_time + last_t + disp_tick

        if(time.time() > next_disp):
            print("[WARNING] Running slower than real-time", file = sys.stderr)
        else:
            # Sleep until next display is expected
            time.sleep(next_disp - time.time())

        # Don't use real time in this calculation, then you'll get drift.
        # This can have some error but it won't accumulate. Take embedded.
        last_t += disp_tick

        print("[{:.2f}s]: {}".format(t,b))
        c.update_plot(b)
