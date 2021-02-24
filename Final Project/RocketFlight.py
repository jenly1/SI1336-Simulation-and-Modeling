# Simulates a rocket flight

import numpy as np
from scipy.integrate import odeint
from RocketStage import *                           

class Flight:
    def __init__(self, dt, stage, Y0, x=[], v=[], t=None):
        """
        Create a rocket flight object.

        dt:         Time step
        stage:      Rocket stage 
        Y0:         Initial condition vector on the form [position, velocity]
        x:          Position vector
        v:          Velocity vector
        t:          Time interval 
        m:          Mass storage
        """
        self.dt = dt
        self.stage = stage
        self.Y0 = Y0
        if t is None and x==[] and v==[]: # If first stage
            self.t = np.arange(0, self.stage.burnTime(), self.dt)
            self.x = []
            self.v = []
        else:                               
            self.t = t
            self.x = x
            self.v = v
    
    def rho(self, x):
        """
        Exponential approximation of air density change with height on Earth

        x:          Current position

        Return:     Air density 
        """
        return 1.225 * np.exp(-x/10400)   
 
    def RK4(self, Ycurr, t):
        """
        Chosen numerical integrator, Runge-Kutta of fourth order (RK4).
        
        Ycurr:      Current vector 
        t:          Current timestep

        Return:     Updated vector Y
        """
        # Current values
        x = Ycurr[0]
        v = Ycurr[1]
        t0 = self.t[0]

        def dv(x,v,t):
            """
            Calculates the ODE (Newtons 2nd law of motion in the vertical axis of the rocket)

            x:      Current position
            v:      Current velocity
            t:      Current timestep

            Return: ODE value
            """
            m = self.stage.massCurr(t-t0)
            D = self.stage.dragForce(self.rho(x), self.stage.Cd, self.stage.dragArea(), v)
            T = self.stage.T
            return (1/m) * (T - m*g0 - D)

        # RK4
        dt = self.dt

        a1 = dt * dv(x,v,t)
        b1 = dt * v

        a2 = dt * dv(x+b1/2, v+a1/2, t+dt/2)
        b2 = dt * (v+a1/2)

        a3 = dt * dv(x+b2/2, v+a2/2, t+dt/2)
        b3 = dt * (v+a2/2)

        a4 = dt * dv(x+b3, v+a3, t+dt)
        b4 = dt * (v+a3)

        xnew = x + (1/6) * (b1 + 2*b2 + 2*b3 + b4)
        vnew = v + (1/6) * (a1 + 2*a2 + 2*a3 + a4)

        # New vector
        Y = [xnew, vnew]

        return Y

    def Euler(self, Ycurr, t):
        # Current values
        x = Ycurr[0]
        v = Ycurr[1]
        t0 = self.t[0]

        def dv(x,v,t):
            m = self.stage.massCurr(t-t0)
            D = self.stage.dragForce(self.rho(x), self.stage.Cd, self.stage.dragArea(), v)
            T = self.stage.T
            return (1/m) * (T - m*g0 - D)

        # Explicit Euler method
        dt = self.dt

        xnew = x + v * dt
        vnew = v + dv(x,v,t) * dt

        # New vector
        Y = [xnew, vnew]

        return Y

    def solveRK4(self, Y0):
        """
        Solves the ODE in given time interval
        
        Y0:         Initial vector
        """
        for t in self.t:
            if t == self.t[0]:
                Y = self.RK4(Y0, t)       # Change this depending on what integrator you want to use
                self.x.append(Y[0])
                self.v.append(Y[1])
            else:
                Y = self.RK4(Y, t)        # ^
                self.x.append(Y[0])
                self.v.append(Y[1])

    def liftoffRK4(self):
        """
        Calculates the altitude and velocity for different stages. 

        Return:     Total burn time, altitude and velocity
        """
        # First stage liftoff
        self.solveRK4(self.Y0)

        # Burn-out values RK4
        tb = self.t[-1] - self.t[0]
        xb = self.x[-1]
        vb = self.v[-1]

        # New initial condition for next stage
        Y0next = [xb, vb]
        
        # Next stage liftoff
        if isinstance(self.stage.payload, Stage): # isinstance returns True if rocket payload is an instance of the Stage class, i.e. if payload exists, i.e. if next stage exists
            nextStage = self.stage.payload
            nextTime = np.arange(tb, tb+nextStage.burnTime(), self.dt)
            nextPos = self.x
            nextVel = self.v

            # Initiate next flight
            nextStageFlight = Flight(self.dt, nextStage, Y0next, x = nextPos, v = nextVel, t = nextTime)
            nextStageFlight.solveRK4(Y0next)

            # Total time
            self.t = np.concatenate((self.t, nextTime))

        return self.t, self.x, self.v


# Below code is redundant if one can figure out how to call the solve function correctly so that the input is the desired numerical integrator. 


    def solveEuler(self, Y0):
        """
        Solves the ODE in given time interval
        
        Y0:         Initial vector
        """
        for t in self.t:
            if t == self.t[0]:
                Y = self.Euler(Y0, t)       # Change this depending on what integrator you want to use
                self.x.append(Y[0])
                self.v.append(Y[1])
            else:
                Y = self.Euler(Y, t)        # ^
                self.x.append(Y[0])
                self.v.append(Y[1])

    def liftoffEuler(self):
        """
        Calculates the altitude and velocity for different stages. 

        Return:     Total burn time, altitude and velocity
        """
        # First stage liftoff
        self.solveEuler(self.Y0)

        # Burn-out values RK4
        tb = self.t[-1] - self.t[0]
        xb = self.x[-1]
        vb = self.v[-1]

        # New initial condition for next stage
        Y0next = [xb, vb]
        
        # Next stage liftoff
        if isinstance(self.stage.payload, Stage): # isinstance returns True if rocket payload is an instance of the Stage class, i.e. if payload exists, i.e. if next stage exists
            nextStage = self.stage.payload
            nextTime = np.arange(tb, tb+nextStage.burnTime(), self.dt)
            nextPos = self.x
            nextVel = self.v

            # Initiate next flight
            nextStageFlight = Flight(self.dt, nextStage, Y0next, x = nextPos, v = nextVel, t = nextTime)
            nextStageFlight.solveEuler(Y0next)

            # Total time
            self.t = np.concatenate((self.t, nextTime))

        return self.t, self.x, self.v