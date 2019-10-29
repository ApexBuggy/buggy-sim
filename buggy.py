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

    # This is a little janky because it isn't about one axis;
    # rather, it is the sum of the moments of inertia of the wheels,
    # each about their axes of rotation.
    I      = 0.0 # moment of inertia (kg * m^2)
    r_w    = 0.0 # Radius of each wheel (m)

    angle  = 0.0 # angle between ground plane and buggy forward axis (rad)
    dist   = 0.0 # distance along course (m)
    v      = 0.0 # velocity (m/s)

    forces = [] # Forces on the buggy (N)

    def __init__(self,
                 mass,             # Constant mass of buggy (kg)
                 velocity = 0,     # Initial velocity (m/s)
                 angular_mass = 0, # Constant moment of inertia (see I above)
                 wheel_radius = 0, # Constant wheel radius (m)
                 distance = 0):    # Initial distance along the course (m)
        self.m = mass
        self.v = velocity
        self.I = angular_mass
        self.r_w = wheel_radius
        self.dist = distance

    def add_force(self, F):
        self.forces.append(F)

    # Update everything given a delta time dt and course information
    def update(self, dt, slope):
        self.angle = math.atan(slope)

        # Compute the total force on buggy
        F = sum([f.F(self) for f in self.forces])

        # Acceleration
        a = F / self.m

        # New velocity
        # a = (v_new - v_old) / dt
        v_new = a * dt + self.v

        # Update state

        # Slightly more accurate distance calculation, I think
        # TODO: get someone better at approximations to look at this
        # Delta distance for this delta time
        dd = dt * (v_new + self.v) / 2
        self.dist += dd * math.cos(self.angle)

        self.v = v_new

    def __str__(self):
        return ("{:.1f}kg @ {:.3f}m ∠ {:.3f}rad, {:.3f}m/s"
                .format(self.m,self.dist,self.angle, self.v))
