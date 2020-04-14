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

# Parse the course file into a 3D course
# Not config but this needs to be here for the next few lines
gp = GeoParse(course_file)

# What parts of the course to smooth, and by how much
# Format: (range(lo_idx, hi_idx), smoothing_factor)
#         lo_idx = starting index in course.dat, inclusive
#         hi_idx = ending index in course.dat, exclusive
#         smoothing_factor = how many data points to sample when smoothing
#                            more points -> smoother but further from true data
#                            NB: must be odd
course_smooths = [
    # Hill 1 to a little way down the steepest part of the free roll,
    # less smoothed so the top of the hill doesn't lower (and because
    # the data at the beginning of the course is more smooth)
    (range(0, 56), 7),

    # Slight overlap with previous to smooth the boundary (which is
    # sketchy because smoothing is not associative). Smooth until the
    # end. Pulls the chute turn in a little bit more than is probably
    # realistic (turn is more gradual than it should be), and doesn't
    # quite smooth the end of hill 5. This part of the data is much
    # noisier, so more smoothing is required
    (range(48, len(gp.points)), 17)
]

###################
# SIMULATION CODE #
###################

# Smooth the course data
for (r, sf) in course_smooths:
    gp.smooth_range(r, sf)

# Instantiate a Course with the smoothed points
c = Course(gp.get_points())

# Declare a force due to gravity
Fg = buggy.Gravity_Force()

# Instantiate a Buggy
# mass = 55 kg ~ 120 lbs
# velocity = 0 for now
# angular mass (moment of inertia) = 0 for now
# wheel radius = 0 for now
# distance = 180m is a little past hill 2, for testing
b = buggy.Buggy(mass = 55, velocity = 0,
                angular_mass = 0.015, wheel_radius = 0.1, distance = 180)

# Assign the buggy force due to gravity
b.add_force(Fg)

# Initialize the plot
c.init_plot()

# Timing variables
t = 0                    # Simulation time
start_time = time.time() # Wall clock time of simulation start
last_disp_time = 0       # Last simulation time that was displayed

# Simulation loop (bounded at 150s)
while(t < 150):
    # Increase time by small delta
    t += DT

    # Update the buggy (position, speed, etc) given that DT seconds have
    # passed since the last call to update, and given the slope of the
    # course at the specific point where the buggy is currently
    b.update(DT, c.slope_at(b.dist))

    # Check if simulation time has reached the time at which we are supposed
    # to display again
    if(t >= last_disp_time + disp_tick):
        # Wall time when the next display should occur
        next_disp = start_time + last_disp_time + disp_tick
        # Update last display time
        last_disp_time += disp_tick
        # Don't use real time (simulation time or wall clock time) in these
        # calculations, then you'll get "drift". As is, we can have some
        # error but it won't accumulate. Take embedded :-P

        # Wait until enough wall clock time has passed that it's time
        # for the next display (i.e. wait for wall clock time to catch
        # up to simulation time)
        if(time.time() > next_disp):
            print("[WARNING] Running slower than real-time", file = sys.stderr)
        else:
            # Sleep until next display is expected
            time.sleep(next_disp - time.time())

        # Print the simulation time and info about the buggy to console
        print("[{:.2f}s]: {}".format(t,b))

        # Update the plot with the buggy's new position
        c.update_plot(b)
