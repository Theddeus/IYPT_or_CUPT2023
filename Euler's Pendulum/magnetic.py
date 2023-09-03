#/usr/bin/python3
import numpy as np
#import multiprocessing
sigma = 500 # dencity of magnetic pole strength (Could be a function of space.)

def magfield(theta,r,a=0.02,I1=5259.95 ):
    miu0 = 1.2566e-6
    Br = (miu0*I1*a**2*np.cos(theta))/(2*(a**2+r**2)**(3/2))*(1+(15*a**2*r**2*np.sin(theta)**2)/(4*(a**2+r**2)**(2)))
    Bsita = (-miu0*I1*a**(2)*np.sin(theta)/(4*(a**2+r**2)**(5/2))*(2*a**2-r**2+(15*a**2*r**2*np.sin(theta)**2*(4*a**(2)-3*r**(2)))/(8*(a**2+r**2)**(2))))
    return Br,Bsita

def magforce(x,y,z,s,sigma = 2*0.37/1.2566e-6):
    r = np.sqrt(x**2+y**2+z**2)
    theta = np.arccos(z/r)
    phisin = np.arcsin(y/np.sqrt(x**2+y**2))
    phicos = np.arccos(x/np.sqrt(x**2+y**2))
    Br,Bsita = magfield(theta,r)
    m = sigma*s
    Bt = theta+np.arctan(Bsita/Br)# theta angle of B with Br
    B = np.sqrt(Br**2+Bsita**2)*np.array([np.sin(Bt)*np.cos(phicos),np.sin(Bt)*np.sin(phisin),np.cos(Bt)])
    return -m*B



def calculate_force( Sita, h=0.013,rdisk = 0.005,res = 0.0001,l = 0.1982):
    xnum = 2*rdisk//res
    F = np.array([0.0,0.0,0.0],dtype='float64')
    for i in range(int(xnum)):
        x = i*res
        y = (2*x*rdisk-x**2)**(1/2)
        ynum = int(2*y//res)
        for j in range(int(ynum)):
            xcor = i*res*np.cos(Sita)-rdisk
            ycor = j*res
            zcor = -x*np.sin(Sita)-h
            xcorf = xcor-l*np.sin(Sita)
            ycorf = ycor
            zcorf = zcor-l*np.cos(Sita)
            F1 = magforce(xcor,ycor,zcor,res**2)
            F2 = -magforce(xcorf,ycorf,zcorf,res**2)
            F += F1+F2
    return F


def magtorque(Sita,h=0.0134,rdisk = 0.005,res = 0.0001,l = 0.1982):
    # Split the circle of the top of the pendulum
    xnum = 2*rdisk//res
    M = 0


    """with multiprocessing.Pool() as p:
        results = p.map(calculate_force, [(i, Sita, h, rdisk, res) for i in range(int(xnum))])"""
    
    #print(results[1])
    
    #M = np.sum(results,axis = 0)
    for i in range(int(xnum)):
        x = i*res
        y = (2*x*rdisk-x**2)**(1/2)
        ynum = int(y//res)
        #args = []
        
        for j in range(int(ynum)):
            xcor = i*res*np.cos(Sita)-rdisk
            ycor = j*res
            zcor = -x*np.sin(Sita)-h
            xcorf = xcor-l*np.sin(Sita)
            ycorf = ycor
            zcorf = zcor-l*np.cos(Sita)
            F = magforce(xcor,ycor,zcor,res**2)
            r = np.array([xcor,ycor,zcor])-np.array([-rdisk,0,-h])
            Ff = -magforce(xcorf,ycorf,zcorf,res**2)
            rf = np.array([xcorf,ycorf,zcorf])-np.array([-rdisk,0,-h])
            M += np.cross(r,F)+np.cross(rf,Ff)
            #M += np.cross(rf,Ff)
            #M += np.cross(r,F)
    
    return -2*M[1],-2*M

if __name__ == "__main__":
    print("Field test = ",np.array(magfield(np.pi*(5/6),0.01)))
    print("Force test = ",magforce(2,2,-4,0.02))
    print("Torque test =",magtorque(np.pi/3,h=0.01)[0])
    print("Integrated force test = ",calculate_force(0.001,h = 0.0134))
    """Mm = []
    for i in np.linspace(0,np.pi/2,100):
        Mm.append([i,magtorque(abs(i))[0]])
    Mm = np.array(Mm)
    print(Mm[0,:])
    print(Mm[5,1])"""
    #magtorque(np.pi/12)