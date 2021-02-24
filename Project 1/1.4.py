# Python simulation of simple planar pendulum with real time animation

# import matplotlib
# matplotlib.use('TKAgg')
from matplotlib import animation
from pylab import *

# Global constants
G = 9.8                     # gravitational acceleration

class Oscillator:
    """Class for an general, simple oscillator"""
    gamma = 1
    m = 1                   # mass of the pendulum bob
    c = 4                   # c=g/L=4
    L = G / c               # string length
    t = 0                   # the time
    theta = np.pi / 2       # the position/angle
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


class DampedPendulum(BaseSystem):
    def force(self, osc):
        return -(osc.m * osc.c * np.sin(osc.theta)) - (osc.m * osc.gamma * osc.dtheta)


class BaseIntegrator:
    dt = 0.01  # time step

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


class VerletIntegrator(BaseIntegrator):
    def timestep(self, simsystem, osc, obs):
        osc.t += self.dt

        accel = simsystem.force(osc) / osc.m

        # TODO: Implement the integration here, updating osc.theta and osc.dtheta
        osc.theta = osc.theta + osc.dtheta*self.dt + 0.5*accel*(self.dt**2)
        osc.dtheta = osc.dtheta + 0.5*(simsystem.force(osc)/osc.m + accel)*self.dt


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
            tmax=30.,               # final time
            stepsperframe=5,        # how many integration steps between visualising frames
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
        # plt.waitforbuttonpress(30)
        
        plt.clf()
        plt.title("DampedPendulum-Verlet")
        plt.plot(obs.vel, obs.pos, label="PhaseDiagram")
        plt.xlabel('position')
        plt.ylabel('velocity')
        plt.legend()
        #plt.savefig(title + ".pdf")
        plt.show()

simulation = Simulation()

simulation.run(simsystem=DampedPendulum(), integrator=VerletIntegrator(), title="DampedPendulum-V")