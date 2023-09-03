#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sci
import numerical
import imageio
plt.rcParams['lines.linewidth'] = 4
    # Set default font size for titles 
plt.rcParams['axes.titlesize'] = 16

    # Set default font size for labels on x-axis and y-axis
plt.rcParams['axes.labelsize'] = 23

plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

    # Set default size of markers
plt.rcParams['lines.markersize'] = 10
if __name__ =="__main__":
    #The = eval(input("What is the initial angle? (degree)"))
    time = eval(input("How long to simulate? "))
    l = eval(input("What is the length? "))
    amp = float(input("What is the amplitude? "))
    v0 = eval(input("Initial velocity? "))
    The = np.arcsin(amp/l)*180/np.pi
    m = (0.118/19.82)*l
    #tim = eval(input("What is the initial angle? (s)"))
    X,Y,Z,T,Alp,Bet,angbai,Wx = numerical.simulation(l=l,v0=v0,Theta = The,m = m,time = time)
    plotset =[]
    Bet = np.array(Bet)
    Wx = np.array(Wx)
    for i in range(int(int(np.max(T))/0.01)):
        plt.figure(layout = "constrained")
        plt.plot(Bet[:i*100],Wx[:i*100])
        plt.xlim(0.2,np.pi/2)
        plt.ylim(-30,30)
        axs = plt.gca()
        for spine in axs.spines.values():
            spine.set_linewidth(4)
        plt.xlabel(r"$\beta$(rad)")
        plt.ylabel(r"$\omega_x$(rad/s)")
        plt.savefig(f"Simulation.png")
        plotset.append(imageio.imread("Simulation.png"))
    imageio.mimsave('phase.gif', plotset, duration=0.01)

    print("Totally Finished !!!")
