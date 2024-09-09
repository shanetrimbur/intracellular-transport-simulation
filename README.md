# Intracellular Transport Simulation

## Overview
This project simulates the intracellular transport mechanisms of motor proteins like kinesin, dynein, and myosin. These motor proteins travel along cytoskeletal tracks (microtubules for kinesin/dynein and actin filaments for myosin) to transport cargo within cells. The program models the dynamics of these motor proteins, including their ATP consumption, movement, and interactions with cytoplasmic obstacles (crowding).

## Key Features
- **Motor Proteins**: Simulates kinesin, dynein, and myosin motors.
- **Multiple Tracks**: Kinesin/dynein operate on microtubules, while myosin moves along actin filaments.
- **ATP Consumption**: Tracks energy usage for each motor during the simulation.
- **Cytoplasmic Crowding**: Introduces obstacles that motors must navigate, simulating the crowded environment inside cells.
- **Collision Detection**: Models how motor proteins respond when encountering obstacles on the track.

## Requirements
- Python 3.x
- NumPy
- Matplotlib

To install required libraries:
```bash
pip install numpy matplotlib

