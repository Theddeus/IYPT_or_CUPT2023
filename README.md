# IYPT_or_CUPT2023
The simulations of problems of IYPT or CUPT 2023 (legacy files)
# Main folder
read.py --- a Tracker based on opencv CSRT algorithm, the output is a excel and a figure, both containing position and time.
It is able to track unlimited number of targets. (as long as python and your computer can handle)
# Euler's Pendulum
The files of this problem is created by defining the key functions in magnetic.py and numerical.py. You can run simulation using 
run.py which is the default runner of functions defined in numerical.py and magnetic.py. Specific information is seen in the Euler's pendulum
folder.
# Arrester Bed
The files are written in the similar manner as Euler's Pendulum. The numerical.py contains functions based on Wong-Reece's algorithm.
# Pancake Rotation
plot.py -- a plotting and peak finding python script that can be used to process the excel created by read.py or any other excel formated similarly 
with read.py
