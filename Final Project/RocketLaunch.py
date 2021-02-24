# Simulates a rocket launch (test)

import matplotlib
import pylab as plt
import numpy as np
from RocketFlight import * 

# Makes sure that the labels on the plots have a readable size 
matplotlib.rcParams.update({'font.size': 20})

# Lists
dtList = [0.1, 0.05, 0.01, 0.005, 0.001, 0.0001]
mList = np.arange(2e3, 40e3, 10)
MList = np.arange(10e3, 15e3, 1e3)
colors = ["yellow", "orange", "red", "lawngreen", "cyan", "b"]

# Results RK4 
tList, xList, vList = [], [], []

# Results Euler 
ttList, xxList, vvList = [], [], []

# Results error
errorx, errorv = [], []


for dt in dtList:
    # for M in MList:       # Try mass limit
    # for m in mList:       # Try mass distribution between the stages
        # m1 = 0.9 * m
        # m2 = m - m1
        m1 = 8352
        m2 = 2088

        # Test vehicle 
        R2 = Stage("Stage 2", 1e3, m2, 2e3, 200e3, 380, 0.75, 0.2)
        R1 = Stage("Stage 1", 3e3, m1, 6e3, 200e3, 340, 0.75, 0.2, payload=R2)
        rocket = R1

        R22 = Stage("Stage 2", 1e3, m2, 2e3, 200e3, 380, 0.75, 0.2)
        R11 = Stage("Stage 1", 3e3, m1, 6e3, 200e3, 340, 0.75, 0.2, payload=R22)
        rockett = R11

        # Initial condition
        Y0 = [0, 0]     

        # Initiate flight
        rocketFlight = Flight(dt, rocket, Y0)
        t, x, v = rocketFlight.liftoffRK4()

        rocketFlightt = Flight(dt, rockett, Y0)
        tt, xx, vv = rocketFlightt.liftoffEuler()

        # # If altitude of 100 km (Karman's line) is achieved
        # if xx[-1] >= 100e3:
        tList.append(t)
        xList.append(x)
        vList.append(v)
        ttList.append(tt)
        xxList.append(xx)
        vvList.append(vv)
        # errorx.append(np.subtract(x, xx))
        # errorv.append(np.subtract(v, vv))

        print("\nRK4")
        print("Maximume altitude for dt", dt, "is:", x[-1])
        print("Maximume velocity for dt", dt, "is:", v[-1])  

        print("\nEuler")
        print("Maximume altitude for dt", dt, "is:", xx[-1])
        print("Maximume velocity for dt", dt, "is:", vv[-1])  

        print("Needed mass is m1:", m1, "and m2:", m2)
        print("Total mass:", m1+m2)
            # break

# Plots ------------------------------------------------------------------------------------------------------------------------------------------------------

# # Time vs altitude RK4
# plt.figure(1)
# #plt.title("Altitude vs. time for RK4")
# for x, t, dt, c in zip(xList, tList, dtList, colors):
#     plt.plot(t, x, color = c, label = "dt = "+str(dt))
# plt.plot(t,[100000+i*0 for i in t], "k")
# plt.plot(t,[i*0 for i in t], "k")
# plt.legend(loc = "upper left")
# plt.xlabel("Time [s]")
# plt.ylabel("Altitude [m]")
# plt.ticklabel_format(style='sci', axis='y', scilimits=(3,3))

# # Time vs velocity RK4
# plt.figure(2)
# #plt.title("Velocity vs. time for RK4")
# for v, t, dt, c in zip(vList, tList, dtList, colors):
#     plt.plot(t, v, color = c, label = "dt = "+str(dt))
# plt.legend(loc = "upper left")
# plt.xlabel("Time [s]")
# plt.ylabel("Velocity [m/s]")

# # Time vs altitude Euler
# plt.figure(3)
# #plt.title("Altitude vs. time for Explicit Euler")
# for x, t, dt, c in zip(xxList, ttList, dtList, colors):
#     plt.plot(t, x, color = c, label = "dt = "+str(dt))
# plt.plot(t,[100000+i*0 for i in t], "k")
# plt.plot(t,[i*0 for i in t], "k")
# plt.legend(loc = "upper left")
# plt.xlabel("Time [s]")
# plt.ylabel("Altitude [m]")
# # plt.ticklabel_format(style='sci', axis='y', scilimits=(3,3))

# # Time vs velocity Euler
# plt.figure(4)
# #plt.title("Velocity vs. time for Explicit Euler")
# for v, t, dt, c in zip(vvList, tList, dtList, colors):
#     plt.plot(t, v, color = c, label = "dt = "+str(dt))
# plt.legend(loc = "upper left")
# plt.xlabel("Time [s]")
# plt.ylabel("Velocity [m/s]")

# # Altitude error
# plt.figure(5)
# #plt.title("Altitude error vs. time")
# for e, t, dt, c in zip(errorx, tList, dtList, colors):
#     plt.plot(t, e, color = c, label = "dt = "+str(dt))
# plt.legend(loc = "upper left")
# plt.xlabel("Time [s]")
# plt.ylabel("Altitude [m]")

# # Velocity error
# plt.figure(6)
# #plt.title("Velocity error vs. time")
# for e, t, dt, c in zip(errorv, tList, dtList, colors):
#     plt.plot(t, e, color = c, label = "dt = "+str(dt))
# plt.legend(loc = "upper left")
# # plt.xlabel("Time [s]")
# # plt.ylabel("Velocity [m/s]")

# # Mass dependence altitude RK4
# plt.figure(7)
# for x, t, M, c in zip(xList, tList, MList, colors):
#     plt.plot(t, x, color = c, label = "m1 = " + str(M))
# plt.plot(t,[100000+i*0 for i in t], "k")
# plt.plot(t,[i*0 for i in t], "k")
# plt.legend(loc = "upper left")
# # plt.xlabel("Time [s]")
# # plt.ylabel("Altitude [m]")
# plt.ticklabel_format(style='sci', axis='y', scilimits=(3,3))

# # Mass dependence velocity RK4
# plt.figure(8)
# for v, t, M, c in zip(vList, tList, MList, colors):
#     plt.plot(t, v, color = c, label = "m1 = " + str(M))
# plt.plot(t,[i*0 for i in t], "k")
# plt.legend(loc = "upper left")
# # plt.xlabel("Time [s]")
# # plt.ylabel("Velocity [m/s]")

plt.show()







