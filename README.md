# IYPT_or_CUPT2023

Simulation codes for several problems from the 2023 International Young
Physicists' Tournament (IYPT) and the Chinese Undergraduate Physics
Tournament (CUPT). These scripts are kept for reference.

## Main folder

`read.py`  
A tracker built on OpenCV's CSRT algorithm. It outputs an Excel file and a
PNG figure with the tracked positions versus time. The number of tracked
objects is limited only by your hardware.

`magnetic.py`  
Helper functions for calculating magnetic fields and forces used in multiple
problems.

## Euler's Pendulum

Numerical simulation of Euler's pendulum following the equations in R. I.
Leine, *Experimental and theoretical investigation of the energy
dissipation of a rolling disk during its final stage of motion* (2008).
Core functions are defined in `magnetic.py` and `numerical.py`. Run
`python run.py` inside the folder to start a simulation.

## Arrester Bed

Implements Wong–Reece's algorithm for a cylinder moving through a sand bed.
The implementation resides in `numerical.py`.

## Pancake Rotation

`plot_fft.py` analyses the Excel output from `read.py` (or a file with the
same format). It performs a Fourier transform of the coordinates and
highlights dominant frequencies.
