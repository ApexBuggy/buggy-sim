from course import Course
import buggy

DT = 10**(-1)

c = Course([(0,1),(1,0)])

Fg = buggy.Gravity_Force()

# 55 kg ~ 120 lbs
b = buggy.Buggy(m=55, v=0)
b.add_force(Fg)

while(b.xpos < 1.0):
    b.update(DT, c.slope_at(b.xpos))
    print(b)
