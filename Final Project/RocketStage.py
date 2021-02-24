# Simulates a stage in a rocket

import numpy as np

# Global constants 
g0 = 9.80665        # Gravitation at sea level [m/s^2]

class Stage:
    def __init__(self, name, ms, mp, ml, T, Isp, Cd, d, payload=None):
        """
        Create a rocket stage object. When creating a multi-stage rocket, create the stages in flipped order, 
        i.e. start with final stage and end with first stage.

        name:       Name of stage 
        ms:         Structural mass [kg]
        mp:         Propellant mass [kg]
        ml:         Payload mass [kg]
        T:          Thrust [N]
        Isp:        Specific impulse [s]
        Cd:         Drag coefficient 
        d:          Diameter [m]
        payload:    Previous stage
        """
        self.name = name        
        self.ms = ms
        self.mp = mp
        self.ml = ml
        self.T = T
        self.Isp = Isp
        self.Cd = Cd
        self.d = d
        self.payload = payload

    def dragArea(self):
        """Calculates cross-sectional area of rocket stage"""
        return np.pi * (self.d/2)**2

    def dragForce(self, rho, Cd, A, v):
        """Calculates the drag force operating on the rocket stage"""
        return 0.5 * rho * Cd * A * v**2

    @property
    def m0(self):
        """Calculates initial total mass, including propellant, also known as wet mass."""
        return self.mf + self.mp

    @property
    def mf(self):
        """Calculates final total mass, without propellant, also known as dry mass."""
        return self.ml + self.ms

    def massFlow(self):
        """Calculates massflow"""
        return self.T / (g0 * self.Isp)

    def massCurr(self, t):
        """Calculates current mass at timestep t"""
        return self.m0 - self.massFlow() * t

    def burnTime(self):
        """Calculates the burn time, i.e. when the rocket stage used up all its propellant"""
        return (self.m0 - self.mf) / self.massFlow()

    def __str__(self):
        """For printing out information about the stage"""
        ret = "Rocket stage: " + self.name + "\n"
        ret += "mp = {:0,g}\n".format(self.mp)
        ret += "ms = {:0,g}\n".format(self.mp)
        ret += "ml = {:0,g}\n".format(self.ml)
        ret += "T = {:0,g}\n".format(self.T)
        ret += "Isp = {:0,g}\n".format(self.Isp)
        ret += "Cd = {}\n".format(self.Cd)
        ret += "Payload = {}".format(repr(self.payload))
        return ret







