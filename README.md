# IYPT_or_CUPT2023

Simulation codes for several problems from the 2023 International Young
Physicists' Tournament (IYPT) and the Chinese Undergraduate Physics
Tournament (CUPT). These scripts are kept for reference.


## Setup

Install Python 3 with `pip` and fetch the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

The scripts are pure Python and do not require compilation.

## Main folder

`read.py`
A tracker built on OpenCV's CSRT algorithm. It outputs an Excel file and a
PNG figure with the tracked positions versus time. The number of tracked
objects is limited only by your hardware.
Run `python read.py` and follow the prompts to select regions of interest
in a video. The tracker saves a spreadsheet and plot in the current
directory.

`magnetic.py`
Helper functions for calculating magnetic fields and forces used in multiple
problems. Import these utilities from your own scripts instead of executing
the file directly.


## Euler's Pendulum

Numerical simulation of Euler's pendulum following the equations in R. I.
Leine, *Experimental and theoretical investigation of the energy
dissipation of a rolling disk during its final stage of motion* (2008).
Core functions are defined in `magnetic.py` and `numerical.py`. Run

`python run.py` inside the folder to start a simulation. The program
asks for basic parameters (simulation time, length and initial velocity)
and then writes the results to an Excel sheet and a PNG plot.


## Arrester Bed

Implements Wong–Reece's algorithm for a cylinder moving through a sand bed.

The implementation resides in `numerical.py`. Execute it directly with
`python numerical.py` to print the drawbar force, torque and other values
for the default parameters. Alternatively import the module and call the
`balance()` and `friction()` functions to use the model in your own code.


## Pancake Rotation

`plot_fft.py` analyses the Excel output from `read.py` (or a file with the
same format). It performs a Fourier transform of the coordinates and

highlights dominant frequencies. Invoke `python plot_fft.py` and provide the
path to your Excel file when prompted.

