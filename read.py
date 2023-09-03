import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import fft
import time
import pandas as pd
import cv2 as cv
import numpy as np
cap = cv.VideoCapture(input("Input absolute directory of the video to be tracked: "))	

n = int(input('How many balls are there? '))

#Set parameters
params = cv.TrackerCSRT_Params()
#params.use_scale_adaptation = False
params.psr_threshold = 0.075
#params.use_rgb = True
#params.scale_lr = 1
params.scale_sigma_factor = 1

#Create Trackers
for i in range(n):
	setting = "tracker{} = cv.TrackerCSRT_create(params)".format(i)
	exec(setting)

def mcall(event,x,y,flags,param):
	if event == cv.EVENT_LBUTTONDOWN:
		coordinate.append(x)
		coordinate.append(y)
		print(x,' ',y)
		#cv.imshow('frame',f1)
def boxing(x):
	boxes = []
	for i in range(x):
		bbox = cv.selectROI("Boxing", frame, False)
		boxes.append(bbox)
		print(bbox)
		cv.destroyAllWindows()
	return boxes	

scale = input("The scale you are about to draw(in cm): ")
scale = int(scale)
fps = input("The frame per second of input video: ")
fps = float(fps)

it_count = 0 #count iteration

while True:
	it_count += 1
	ret, frame, = cap.read()
	if not ret:
		cv.imwrite('last_frame.jpg',a)
		break	
	if it_count == 1:#First frame
		f1 = frame.copy()
		cv.imshow("Select scale",f1)
		coordinate = []
		cv.setMouseCallback('Select scale',mcall)
		cv.waitKey(0)
		#cv.setMouseCallback('frame',mcall)
		#cv.waitKey(0)
			#if len(coordinate) == 2:
			#	break
		#while True:
		#	cv.setMouseCallback('frame',mcall)
			#time.sleep(100)
		#	if len(coordinate) == 4:
		#		break

		
		#cv.waitKey(0)
		#print(cor1)
		#cor2 = cv.setMouseCallback('frame',mcall)
		#print(cor2)
		#print(type(cor2))
		#print("Press any key to continue.")
		#cv.waitKey(0)
		cv.line(f1,(coordinate[0],coordinate[1]),(coordinate[2],coordinate[3]),(255,0,0),10)
		cv.imshow("Result",f1)
		print("Press any key to continue.")
		cv.waitKey(0)
		cv.destroyAllWindows()
		#yn = input("Do you need to calculate angular velocity? (Y/N) ")
		yn = "N"
		if yn == "Y" or yn == "y":
			cv.imshow("Select center",f1)
			cv.setMouseCallback('Select center',mcall)
			cv.waitKey(0)
			cv.circle(f1, (coordinate[4],coordinate[5]), 10, (255,0,0), -1)
			cv.imshow("Result",f1)
			print("Press any key to continue.")
			cv.waitKey(0)
			cv.destroyAllWindows()
		else:
			pass
		boxes = boxing(n)
		for i in range(n):
			assin = "bbox{} = boxes[{}]".format(i,i)
			exec(assin)
			begin = "ok{} = tracker{}.init(frame,bbox{})".format(i,i,i)
			exec(begin)
			result = "result{} = []".format(i)
			exec(result)
			append = "result{}.append(bbox{})".format(i,i)
			eval(append)
			append = "result{}.append(it_count)".format(i)
			eval(append)
#			if ok:
#				p1 = (int(box[0]),int(box[1])
#				p2 = (int(box[0]+box[2]),int(box[1]+box[3]))
	else:
		a = frame.copy()
		for i in range(n):
			track = "ok{}, bbox{} = tracker{}.update(frame)".format(i,i,i)
			exec(track)
			append = "result{}.append(bbox{})".format(i,i) 
			eval(append)
			timer = cv.getTickCount()
			append = "result{}.append(it_count)".format(i)
			eval (append)
			draw = "box = bbox{}".format(i)
			exec(draw)
			if box:
				p1 = (int(box[0]),int(box[1]))
				p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
				cv.rectangle(a, p1, p2, (255,0,0), 2, 1)
		cv.imshow("Tracking",a)
	#if it_count == 2400:
	#	break
	

	if cv.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv.destroyAllWindows()
distance = ((coordinate[0]-coordinate[2])**2+(coordinate[1]-coordinate[3])**2)**(1/2)
scalar = (scale)/distance
data = pd.DataFrame()
for i in range(n):
	exec("result = result{}".format(i))
	x=[]
	y=[]
	T = []
	length = len(result)//2
	for psi in range(length):
		xprime = (result[2*psi][0] + (result[2*psi][2] * (1/2)))* scalar
		x.append(xprime)
		yprime = 1 * (result[2*psi][1] + (result[2*psi][3] * (1/2)) ) * scalar
		y.append(yprime)
		time = result[2*psi+1]/fps
		T.append(time)
	fori_x = np.array(x)
	x = fori_x
	fori_y = np.array(y)
	y = fori_y
	fori_T = np.array(T)
	T = fori_T
	ftt_series = fft.fft(fori_x)
	ftt_x = fft.fftfreq(fori_T.size,1/fps)
	if yn == "Y" or yn == "y":
		velocity_x = (x[4:] - x[:-4])/(4/fps)
		velocity_y = (y[4:] - y[:-4])/(4/fps)
		T_v = T[2:-2]
		x_v = x[2:-2] - (coordinate[4]*scalar)
		y_v = y[2:-2] - (coordinate[5]*scalar)
		r = np.sqrt(x_v**2 + y_v**2)
		v = np.stack((velocity_x, velocity_y), axis=-1) 
		r_hat = np.stack((x_v, y_v), axis=-1) / r[..., np.newaxis]
		v_r = np.sum(v * r_hat, axis=-1)
		omega = np.cross(v, r_hat) / r
		data_o = pd.DataFrame({"Angular_velocity":omega,"Velocity_r":v_r})
		data_o.to_excel(f"Omega{i+1}.xlsx",index=False)
		figure, ax = plt.subplots(1,2,figsize = (10,5),layout="constrained")
		ax[0].plot(T_v,omega)
		ax[0].set_xlabel("Time (s)", fontsize = 16)
		ax[0].set_ylabel("Angular velocity (rad/s)", fontsize = 16)
		ax[1].set_xlabel("Time (s)", fontsize = 16)
		ax[1].plot(T_v,v_r)
		ax[1].set_ylabel("Radius velocity (cm/s)", fontsize = 16)
		plt.savefig(f"Angular{i+1}.png",dpi = 1000)

	ploting = "fig{}, axs = plt.subplots(3,1,layout='constrained')".format(i)
	exec(ploting)
	#axis = "ax{}.plot(T,x)".format(i)
	#eval(axis)
	#axis = "ax{}.set_xlabel('Time (s)')".format(i)
	#eval(axis)
	#axis = "ax{}.set_ylabel('X position(cm)')".format(i)
	#eval(axis)
	axs[0].plot(T,x)
	axs[0].set_xlabel('Time (s)')
	axs[0].set_ylabel("X position (cm)")
	axs[0].grid()
	axs[1].plot(T,y)
	axs[1].set_xlabel('Time (s)')
	axs[1].set_ylabel("Y position (cm)")
	axs[1].grid()
	axs[2].plot(ftt_x,np.abs(ftt_series))
	axs[2].set_xlabel('Frequency (Hz)')
	axs[2].set_ylabel("Amplitude")	
	axs[2].set_yscale('log')
	#axs[2].set_yticks([20,40,60,80,100])
	axs[2].set_xticks([*range(-10,11)])
	axs[2].set_xlim(xmin=-5,xmax=5)
	axs[2].grid()
	plt.savefig("{}numbers_of_ball.png".format(i),dpi=1200)
	data[f"x{i+1}"] = x
	data[f"t{i+1}"] = T
	data[f"y{i+1}"] = y
data.to_excel(f"data{n}.xlsx",index=False)