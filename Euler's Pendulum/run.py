#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sci
import numerical
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
    X,Y,Z,T,Alp,Bet,Wx = numerical.simulation(l=l,v0=v0,Theta = The,m = m,time = time)
    figure1,axs = plt.subplots(2,2,figsize = (16,9),layout = "constrained")
    axs[0,0].plot(T,X)
    axs[0,0].set_xlabel("Time (s)")
    axs[0,0].set_ylabel("X (m)")
    axs[0,1].plot(T,Y)
    axs[0,1].set_xlabel("Time (s)")
    axs[0,1].set_ylabel("Y (m)")
    axs[1,0].plot(T,Z)
    axs[1,0].set_xlabel("Time (s)")
    axs[1,0].set_ylabel("Z (m)")
    axs[1,1].plot(X[:],Y[:])
    axs[1,1].set_xlabel("X (m)")
    axs[1,1].set_ylabel("Y (m)")
    for i in range(4):
        for spine in axs[i//2,i%2].spines.values():
            spine.set_linewidth(4)
    plt.savefig(f"Simulation{round(The,2)}.png",dpi = 1000)
    data = pd.DataFrame({"x":X,"y":Y,"z":Z,"t":T,"alpha":Alp,"beta":Bet,"wx":Wx})
    The = 1
    data.to_excel(f"Simulation{The}.xlsx",index=False)
    print("Totally Finished !!!")
