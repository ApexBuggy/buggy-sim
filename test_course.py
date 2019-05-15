from course import Course

points = [(0,1), (1,0), (2.0, 0.0), (2.1, 1.0), (3.1, 4.0)]
c = Course(points)

test_x = [-0.1,
          0.0,
          0.5,
          1.0,
          1 + 1/3,
          2.0,
          2.000000000001,
          2.1,
          3,
          3.1,
          3.2]

expected_slopes = [None,
                   -1.0,
                   -1.0,
                   -1.0,
                   0.0,
                   0.0,
                   10.0,
                   10.0,
                   3.0,
                   3.0,
                   None]

for i in range(len(test_x)):
    if(c.slope_at(test_x[i]) != expected_slopes[i]):
        print("Test",i,"failed: ",
              c.slope_at(test_x[i]),"!=",expected_slopes[i])
    else:
        print("Test",i,"passed")
