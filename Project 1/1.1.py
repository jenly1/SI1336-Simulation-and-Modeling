# Python simulation of simple planar pendulum with real time animation

# import matplotlib
# matplotlib.use('TKAgg')
from matplotlib import animation
from pylab import *

matplotlib.rcParams.update({'font.size': 15})

# Global constants
G = 9.8                     # gravitational acceleration

class Oscillator:
    """Class for an general, simple oscillator"""
    m = 1                   # mass of the pendulum bob
    c = 4                   # c=g/L=4
    L = G / c               # string length
    t = 0                   # the time
    theta = np.pi * 0.5     # the position/angle
    dtheta = 0              # the velocity

# Class for storing observables for an oscillator
class Observables:
    def __init__(self):
        self.time = []      # list to store time
        self.pos = []       # list to store positions
        self.vel = []       # list to store velocities
        self.energy = []    # list to store energy


class BaseSystem:
    def force(self, osc):
        """ Implemented by the childclasses  """
        pass


class Harmonic(BaseSystem):
    def force(self, osc):
        return -osc.m * osc.c * osc.theta


class Pendulum(BaseSystem):
    def force(self, osc):
        return -osc.m * osc.c * np.sin(osc.theta)


class BaseIntegrator:
    dt = 0.001  # time step

    def integrate(self, simsystem, osc, obs):
        """ Perform a single integration step """
        self.timestep(simsystem, osc, obs)

        # Append observables to their lists
        obs.time.append(osc.t)
        obs.pos.append(osc.theta)
        obs.vel.append(osc.dtheta)
        obs.energy.append(0.5 * osc.m * osc.L ** 2 * osc.dtheta ** 2 + 0.5 * osc.m * G * osc.L * osc.theta ** 2)  # harmonic oscillator        

    def timestep(self, simsystem, osc, obs):
        """ Implemented by the childclasses """
        pass

class EulerIntegrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        osc.t += self.dt

        #accel = simsystem.force(osc) / osc.m
        
        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        theta = osc.theta                              # temporarily storing the value of theta at time t
        osc.theta += osc.dtheta * self.dt
        osc.dtheta -= (G/osc.L) * theta * self.dt

class EulerCromerIntegrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        osc.t += self.dt                            

        #accel = simsystem.force(osc) / osc.m

        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        osc.dtheta -= (G/osc.L) * osc.theta * self.dt # updating dtheta
        osc.theta += osc.dtheta * self.dt             # updating theta

class VerletIntegrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        osc.t += self.dt

        accel = simsystem.force(osc) / osc.m

        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        osc.theta = osc.theta + osc.dtheta*self.dt + 0.5*accel*(self.dt**2)
        osc.dtheta = osc.dtheta + 0.5*(simsystem.force(osc)/osc.m + accel)*self.dt

class RK4Integrator(BaseIntegrator):
    def timestep(self,simsystem,osc,obs):
        osc.t += self.dt

        def accel(theta, dtheta, t):
            return -osc.c * np.sin(theta)

        a1 = accel(osc.theta, osc.dtheta, osc.t) * self.dt
        b1 = osc.dtheta * self.dt

        a2 = (accel(osc.theta + b1/2, osc.dtheta + a1/2, osc.t + self.dt/2) * self.dt)
        b2 = (osc.dtheta + a1/2) * self.dt

        a3 = (accel(osc.theta + b2/2, osc.dtheta + a2/2, osc.t + self.dt/2) * self.dt)
        b3 = (osc.dtheta + a2/2) * self.dt

        a4 = accel(osc.theta + b3, osc.dtheta + a3, osc.t + self.dt) * self.dt
        b4 = (osc.dtheta + a3) * self.dt

        osc.dtheta += (1/6) * (a1 + 2 * a2 + 2 * a3 + a4)
        osc.theta += (1/6) * (b1 + 2 * b2 + 2 * b3 + b4)

        print(osc.dtheta,osc.theta)
        
        # theta = osc.theta

        # osc.t += self.dt
        # accel1 = simsystem.force(osc) / osc.m
        # a1 = accel1*self.dt
        # b1 = osc.dtheta*self.dt

        # osc.theta = theta + 0.5* b1
        # accel2 = simsystem.force(osc) / osc.m
        # a2 = (accel2)*self.dt
        # b2 = (osc.dtheta + 0.5*a1)*self.dt

        # osc.theta = theta + 0.5* b2
        # accel3 = simsystem.force(osc)/osc.m
        # a3 = (accel3)*self.dt
        # b3 = (osc.dtheta + 0.5*a2)*self.dt

        # osc.theta = theta + b3
        # accel4 =simsystem.force(osc)/osc.m
        # a4 = (accel4)*self.dt
        # b4 = (osc.dtheta+b3)*self.dt

        # osc.dtheta = osc.dtheta + (1/6)*(a1 + 2*a2 + 2*a3 + a4)
        # osc.theta = theta       + (1/6)*(b1 + 2*b2 + 2*b3 + b4)

# Animation function which integrates a few steps and return a line for the pendulum
def animate(framenr, simsystem, oscillator, obs, integrator, pendulum_line, stepsperframe):
    for it in range(stepsperframe):
        integrator.integrate(simsystem, oscillator, obs)

    x = np.array([0, np.sin(oscillator.theta)])
    y = np.array([0, -np.cos(oscillator.theta)])
    pendulum_line.set_data(x, y)
    return pendulum_line,


class Simulation:
    def run(self,
            simsystem,
            integrator,
            tmax=300.,               # final time
            stepsperframe=250,        # how many integration steps between visualising frames
            title="simulation",     # name of output file and title shown at the top
            ):
        oscillator = Oscillator()
        obs = Observables()

        numframes = int(tmax / (stepsperframe * integrator.dt))

        plt.clf()
        # fig = plt.figure()
        ax = plt.subplot(xlim=(-1.2, 1.2), ylim=(-1.2, 1.2))
        plt.axhline(y=0)            # draw a default hline at y=1 that spans the xrange
        plt.axvline(x=0)            # draw a default vline at x=1 that spans the yrange
        pendulum_line, = ax.plot([], [], lw=5)
        plt.title(title)
        # Call the animator, blit=True means only re-draw parts that have changed
        anim = animation.FuncAnimation(plt.gcf(), animate,  # init_func=init,
                                       fargs=[simsystem, oscillator, obs, integrator, pendulum_line, stepsperframe],
                                       frames=numframes, interval=25, blit=True, repeat=False)
        plt.show()

        # If you experience problems visualizing the animation and/or
        # the following figures comment out the next line 
        #plt.waitforbuttonpress(30)
        
        plt.clf()
        plt.title("HarmonicOscillator-RK4 | theta(0) = pi*0.5, dt = 0.01")
        plt.plot(obs.time, obs.energy, label="Energy")
        #plt.plot(obs.time, obs.pos, label="Position")
        #plt.plot(obs.time, obs.vel, label="Velocity")
        plt.xlabel('time')
        plt.ylabel('energy')
        plt.legend()
        plt.show()

# Comparing the different methods with each other 
simulation = Simulation()

#simulation.run(simsystem=Harmonic(), integrator=EulerCromerIntegrator(), title="Harmonic-EulerCromer")
#simulation.run(simsystem=Harmonics(), integrator=VerletIntegrator(), title="Harmonic-Verlet")
simulation.run(simsystem=Harmonic(), integrator=RK4Integrator(), title="Harmonic-RK4")

# simulation.run(simsystem=Pendulum(), integrator=EulerCromerIntegrator(), title="Pendulum-EulerCromer")
#simulation.run(simsystem=Pendulum(), integrator=VerletIntegrator(), title="Pendulum-Verlet")
# simulation.run(simsystem=Pendulum(), integrator=RK4Integrator(), title="Pendulum-RK4")

