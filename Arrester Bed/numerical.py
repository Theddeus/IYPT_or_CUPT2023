#!/usr/bin/python3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#default parameters
phi = np.pi/6 # Internal friction angle
c = 5 #Cohesion force
K = 1.5 # Shear modulus
k1 = np.exp(10.62) # Sand para1
k2 = 69000 #Sand para2
n = 0.63 #Sand para3
s_proper_default = [phi,c,K,k1,k2,n]
r = 0.015 # Radius of cylinder
b = 0.06 # Length of cylinder
m = 0.064 # Mass of cylinder
g = 9.794 # Gravitational constant
W = m*g
w_proper_default = [r,b,W]
c1 =0.42
c2 = 0.32
slip = 0.05
relative_c_def = [c1,c2,slip]

def sigma1(theta,s_property=s_proper_default,w_property=w_proper_default,theta1=np.pi/6):
    _,_,_,k1,k2,n = s_property
    r,b,_ = w_property
    return (k1+k2*b)*(r/b)**(n)*(np.cos(theta)-np.cos(theta1))

def sigma2(theta,s_property=s_proper_default,w_property=w_proper_default,relative_c=relative_c_def,theta1=np.pi/6):
    _,_,_,k1,k2,n = s_property
    r,b,_ = w_property
    c1,c2,slip = relative_c
    sig = (k1+k2*b)*(r/b)**(n)*(np.cos(theta1-theta*((1-(c1+c2*slip))/(c1+c2*slip)))-np.cos(theta1))**(n)
    return sig

def tau1(theta,s_property=s_proper_default,w_property=w_proper_default,relative_c=relative_c_def,theta1=np.pi/6):
    phi,c,K,_,_,_ = s_property
    r,_,_ = w_property
    _,_,slip = relative_c
    j = r*((theta1-theta)-(1-slip)*(np.sin(theta1)-np.sin(theta)))
    tau = (c+sigma1(theta)*np.tan(phi))*(1-np.exp(-j/K))
    return tau

def tau2(theta,s_property=s_proper_default,w_property=w_proper_default,relative_c=relative_c_def,theta1=np.pi/6):
    phi,c,K,_,_,_ = s_property
    r,_,_ = w_property
    _,_,slip = relative_c
    j = r*((theta1-theta)-(1-slip)*(np.sin(theta1)-np.sin(theta)))
    tau = (c+sigma2(theta)*np.tan(phi))*(1-np.exp(-j/K))
    return tau

def sum(ran,fun,tri,para):
    t = 0.001
    total = int((ran[1]-ran[0])//t)
    integrant = 0
    for i in range(total):
        if tri == "c":
            integrant +=fun(theta=i*t+ran[0],theta1 = para)*np.cos(i*t+ran[0])*t
        if tri =="s":
            integrant +=fun(theta=i*t+ran[0],theta1 = para)*np.sin(i*t+ran[0])*t
        if tri == "const":
            integrant +=fun(theta=i*t+ran[0],theta1 = para)*t

    return integrant

def balance(w_property=w_proper_default,relative_c=relative_c_def):
    r,b,W = w_property
    c1,c2,slip = relative_c
    re_slip = c1+c2*slip
    for theta1 in np.linspace(0,np.pi/2,1000):
            
        Wc = r*b*(sum([theta1*re_slip,theta1],sigma1,tri="c",para=theta1)+sum([0,theta1*re_slip],sigma2,tri="c",para=theta1)+sum([theta1*re_slip,theta1],tau1,tri="s",para=theta1)+sum([0,theta1*re_slip],tau2,para=theta1,tri="s"))
        print("Theta = ",theta1)
        print("W = ",Wc)
        if abs(Wc-W)<0.01*W:
            the = theta1
            break
        elif Wc >W and abs(Wc-W)>0.01*W :
            the = theta1
            break
        else:
            the=[]
            pass
    if the:
        print("Successed :) !")
        return the,slip
    else:
        print("Failed :(")
        return 0,0
def friction(theta1,w_property=w_proper_default,relative_c=relative_c_def):
    #phi,c,K,k1,k2,n = s_property
    r,b,_ = w_property
    c1,c2,slip = relative_c
    re_slip = c1+c2*slip
    Db = r*b*((sum([re_slip*theta1,theta1],tau1,"c",para=theta1)+sum([0,re_slip*theta1],tau2,"c",para=theta1))-(sum([re_slip*theta1,theta1],sigma1,"s",para=theta1)+sum([0,re_slip*theta1],sigma2,"s",para=theta1)))
    Tor = r**2*b*(sum([re_slip*theta1,theta1],tau1,"const",para=theta1)+sum([0,re_slip*theta1],tau2,"const",para=theta1))
    return Db,Tor
if __name__ =="__main__":
    theta,slip = balance()
    Db,Tor = friction(theta)
    print("Contact angle = ",theta)
    print("Slip = ",slip)
    print("Drawbar = ",Db)
    print("Torque = ",Tor)