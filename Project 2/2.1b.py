# A 2D random walk with single steps along x or y
# Use random generator r[i]=(a*r[n-1] + c)

import pylab, numpy, math

def direction(m, r0, a, c, steps):
    # Arrays with the same size as the number of steps
    x = numpy.zeros(steps)
    y = numpy.zeros(steps)
    r = r0
    
    def random_generator():
        nonlocal r0                              # r0 is a local variable, throws UnboundLocalError otherwises
        r0 = (a*r0 + c) % m
        return r0 / (m-1)                        # divided by (m-1) because 

    # Random-walk generator
    for i in range(steps):
        n = math.floor(random_generator() * 4)   # math.floor(x) returns the integer not larger than x
        if n == 0:  
            x[i] = x[i-1] + 1
            y[i] = y[i-1] 

        elif n == 1:
            x[i] = x[i-1] - 1
            y[i] = y[i-1] 

        elif n == 2: 
            x[i] = x[i-1] 
            y[i] = y[i-1] + 1

        elif n == 3:
            x[i] = x[i-1] 
            y[i] = y[i-1] - 1

    pylab.figure()
    pylab.title("Random walk with "+str(steps)+" steps | m={m}, r0={r0}, a={a}, c={c}".format(m=m, r0=r, a=a, c=c))
    pylab.plot(x, y, 'b-')
    pylab.xlabel("x")
    pylab.ylabel("y")
    pylab.show()


steps = [10, 100, 1000]
m = [128, 129, 130]
r0 = [1, 5, 10]
a = [3, 5, 20]
c = [4, 4, 20]

for i in range(len(m)):
    direction(128, r0[i], a[i], c[i], steps[i])
