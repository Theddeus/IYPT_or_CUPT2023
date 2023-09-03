#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy as sci
import magnetic
plt.rcParams['lines.linewidth'] = 4
    # Set default font size for titles 
plt.rcParams['axes.titlesize'] = 16

    # Set default font size for labels on x-axis and y-axis
plt.rcParams['axes.labelsize'] = 23

plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

    # Set default size of markers
plt.rcParams['lines.markersize'] = 10
# Define Parameter
def simulation(l = 19.82,Theta = 42,m = 0.118,time = 60,v0 = 200 ):
     # Length of the pedulum (cm)
    l = l/100
    
    h = l/2
    g = 9.794 # gravitational acceleration (N/kg)
    #k = 40000*1.8*10**(-5)/(2*l) 
    k = 1.4
    Theta = np.pi*Theta/180
    #Initial Velocity of release (cm/s)
    v0 = v0/100
     # Mass of magnetic rod (kg)
    radp = 0.005 # Radius of the pendulum
    D = 2*radp
    # Inertial Tensor
    I1 = 1/4*m*(radp)**2+1/12*m*(h)**2
    I3 = 1/2*m*radp**2

    """
    ex = np.array([1,0,0])
    ey = np.array([0,1,0])
    ez = np.array([0,0,1])
    """
    # Things the simulation tries to record

    T = []
    X = []
    Y = []
    Z = []
    Bet = []
    Alp = []
    We = []
    angbai =[]

    # Formal simulation

    #Set up the simulation
    daldt = v0/l


    alpha = 0.00
    beta = np.pi/2-Theta
    gamma = 0.00
    Mm =[]

    #Get the value of magtorqe to speed up the calculation
    num = 0
    for i in np.linspace(0.0000001,np.pi/2,100):
        Mm.append([i,magnetic.magtorque(abs(i),l=l)[0]])
        print("Calculating Magnetic Torque!",f"{num}%","Fighting!!!!!")
        num+=1
    Mm = np.array(Mm)
    Fc = []
    num = 0
    for i in np.linspace(0.0000001,np.pi/2,100):
        Fc.append([i,magnetic.calculate_force(abs(i),l=l)[2]])
        print("Calculating Magnetic Force!",f"{num}%","Fighting!!!!!")
        num+=1
    Fc = np.array(Fc)


    #Initial angular velocity in K frame
    wx = 0.00 
    #wy = 0.00
    wy = daldt*np.sin(beta)+daldt
    #wz = 0.00
    wz = daldt*np.cos(beta)


    k1 = I1/(m*(radp)**2)
    k2 = I3/(m*(radp)**2)
    epsilon = h/radp
    gbar = g/radp
    wnew = np.array([wx,wy,wz])
    #print(wnew)

    # Total time to simulate
    t = 0.0001# Time step
    total = int(time//t)
    mucount = 0.3
    # Start simulation
    for i in range(total):
        
        wx,wy,wz = wnew
        #print(wnew)
        alpha += wz*(1/np.cos(beta))*t
        beta += wx*t
        gamma += (wy-wz*np.tan(beta))*t
        
        idx = (np.abs(np.pi/2-beta-Mm[:,0])).argmin()
        magtorque = Mm[idx,1]
        Magforce = Fc[idx,1]
        #print(magtorque)
        wnew[0] = wx + ((magtorque/(m*radp**(2))-(k*(l**3)*D*wx/3)/(m*radp**(2))-((k1+epsilon**(2))*np.tan(beta)+epsilon)*wz**2-gbar*(np.sin(beta)-epsilon*np.cos(beta))+wy*wz*(k2+1+epsilon*np.tan(beta)))/(k1+1+epsilon**2))*t
        """print(wx)
        print((k*l**3*D*wx/3)/(m*radp**(2)))
        #print(magnetic.magtorque(abs(np.pi/2-beta),l=l)[0]/(m*radp**(2)))
        print(wnew)"""
        fdissz = -(k*l**3*D*(wz*(1/np.cos(beta)))/3)/(m*radp**(2))+radp*mucount*(Magforce-m*g)*np.sign(wy-wz*np.tan(beta))*np.tan(beta)/(m*radp**(2))
        fdissy = -mucount*radp*(Magforce-m*g)*np.sign(wy-wz*np.tan(beta))/(m*radp**(2))
        dwzdt = ((-(1+epsilon*np.tan(beta))*wx*wz*epsilon/(k2+1)-k2*wx*wy+wx*wz*((k1+epsilon**2)*np.tan(beta)+epsilon)+fdissz+epsilon*fdissy/(k2+1))/(k1+epsilon**2-(epsilon**2/(k2+1))))
        wnew[2] = wz + dwzdt*t
        wnew[1] = wy + ((epsilon*dwzdt-(1+np.tan(beta)*epsilon)*wx*wz+fdissy)/(k2+1))*t
        T.append(t*i)
        X.append(l*np.cos(alpha)*np.cos(beta))
        Y.append(l*np.sin(alpha)*np.cos(beta))
        Z.append(-l*np.sin(beta))
        angbai.append(np.pi/2-beta)
        Bet.append(beta)
        Alp.append(alpha)
        We.append(wnew[0])
        #-mucount*gbar*np.tan(beta)
        #+mucount*gbar
        if beta+wx*t > 1.57:
            angbai = angbai*-1
            alpha += np.pi
            wnew[0] = wnew[0]*(-1)*(1-(2*radp**(2))/(h**2+radp**(2)))
            wnew[2] = wnew[2]*(-1)
            print("Triggered!",wnew)
            print("beta",beta)
        if beta < 0.0001 :
            wnew[0] = abs(wnew[0])
            beta = 0
        if alpha > np.pi*2:
            alpha-=2*np.pi
        else: 
            pass
        
        
        

        print("Finished:",f"{np.round(i*100/total,2)}% ","Fighting !!!!!")
    return X,Y,Z,T,Alp,Bet,angbai,We
if __name__ =="__main__":
    X,Y,Z,T,Alp,Bet,W = simulation()
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
    plt.savefig("Simulation.png",dpi = 300)
    data = pd.DataFrame({"x":X,"y":Y,"z":Z,"t":T,"alpha":Alp,"beta":Bet,"w":W})
    data.to_excel("Simulation2.xlsx",index=False)
    print("Totally Finished !!!")