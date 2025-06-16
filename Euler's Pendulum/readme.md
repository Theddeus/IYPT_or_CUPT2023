This directory contains a numerical model of Euler's pendulum. The equations of
motion follow R. I. Leine, *Experimental and theoretical investigation of the
energy dissipation of a rolling disk during its final stage of motion* (2008).
The magnetic field of the neodymium magnet is approximated as a single loop
current, and the magnetic force on the rod is obtained by integrating the forces
acting on its magnetic poles.

Run the simulation with:

```bash
python run.py
```

The script will ask for parameters such as the total simulation time,
pendulum length and initial velocity. Once finished it creates an Excel
file and a PNG plot with the calculated trajectory. You can also import
`numerical.py` in your own code and call `simulation()` directly.
