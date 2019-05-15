import math

# Represented as a glorified function, but can be subclassed for forces
# of the same form (e.g. friction resistances)
class Force:
    # F : Buggy -> float
    # Returns the force (in N) on the input based on its mass, velocity, etc.
    # Positive axis is forward on the buggy, so rolling resistance e.g.
    # should not require trig, but gravity will.
    F = None

class Gravity_Force(Force):
    # Force directly down
    @staticmethod
    def F_down(buggy):
        return buggy.m * 9.80

    def F(self, buggy):
        return -1 * math.cos(math.pi/2 - buggy.angle) * self.F_down(buggy)

class Buggy:

    m      = 0.0 # mass (kg)

    angle  = 0.0 # angle between +x axis and buggy forward axis (rad)
    xpos   = 0.0 # x-position (m)
    v      = 0.0 # velocity (m/s)

    forces = [] # Forces on the buggy (N)

    def __init__(self, m, v):
        self.m = m
        self.v = v

    def add_force(self, F):
        self.forces.append(F)

    # Update everything given a delta-time dt and course information
    def update(self, dt, slope):
        self.angle = math.atan(slope)

        # Total force on buggy
        F = sum([f.F(self) for f in self.forces])

        # Acceleration
        a = F / self.m

        # New velocity
        # a = (v_new - v_old) / dt
        v_new = a * dt + self.v

        # Update state

        # Slightly more accurate distance calculation, I think
        # TODO: get someone better at approximations to look at this
        dist = dt * (v_new + self.v) / 2
        self.xpos += dist * math.cos(self.angle)

        self.v = v_new

    def __str__(self):
        return ("" + str(self.m) + "kg @ " +
                str(self.xpos) + "m < " + str(self.angle) + "rad, "
                + str(self.v) + "m/s")
