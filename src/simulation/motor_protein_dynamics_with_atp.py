# File: src/simulation/motor_protein_dynamics_with_atp.py

import numpy as np
import random
import matplotlib.pyplot as plt

class MotorProtein:
    def __init__(self, name, speed, step_size, force, atp_consumption):
        self.name = name
        self.speed = speed  # nm/s
        self.step_size = step_size  # nm/step
        self.force = force  # pN
        self.atp_consumption = atp_consumption  # ATP per step
        self.bound = False
        self.total_atp_used = 0  # Track total ATP consumed

    def bind_to_track(self, probability):
        """Motor binds to a track with a given probability."""
        self.bound = random.random() < probability

    def step(self):
        """Simulate one step of motor movement if bound."""
        if self.bound:
            return self.step_size
        return 0

    def consume_atp(self):
        """Simulate ATP consumption for each step."""
        if self.bound:
            self.total_atp_used += self.atp_consumption
        return self.atp_consumption if self.bound else 0

# Define cytoskeletal track (simple 1D for now)
class CytoskeletalTrack:
    def __init__(self, length):
        self.length = length
        self.positions = np.zeros(length)

    def update_position(self, motor, position, direction):
        """Update motor position on the track."""
        if 0 <= position < self.length:
            self.positions[position] += motor.step() * direction

# Simulation
def intracellular_transport_simulation(motor1, motor2, steps, track_length):
    track = CytoskeletalTrack(track_length)
    position = track_length // 2  # Start in the middle of the track
    direction = 1  # Start by moving in one direction

    motor1_atp_consumed = []
    motor2_atp_consumed = []

    for step in range(steps):
        motor1.bind_to_track(0.8)  # 80% chance to bind
        motor2.bind_to_track(0.8)

        # Tug-of-war dynamics: each motor pulls in opposite directions
        if motor1.bound:
            direction = 1
        elif motor2.bound:
            direction = -1

        track.update_position(motor1, position, direction)
        track.update_position(motor2, position, -direction)

        # Simulate ATP consumption
        atp_used_motor1 = motor1.consume_atp()
        atp_used_motor2 = motor2.consume_atp()

        motor1_atp_consumed.append(motor1.total_atp_used)
        motor2_atp_consumed.append(motor2.total_atp_used)

        print(f"Step {step + 1}: Motor 1 ATP: {atp_used_motor1}, Motor 2 ATP: {atp_used_motor2}")
        print(f"Motor 1 bound: {motor1.bound}, Motor 2 bound: {motor2.bound}")
        print(f"Position: {position}, Direction: {direction}")

    # Plotting ATP consumption over time
    plt.plot(motor1_atp_consumed, label='Motor 1 ATP Consumption (Kinesin)')
    plt.plot(motor2_atp_consumed, label='Motor 2 ATP Consumption (Dynein)')
    plt.xlabel('Simulation Steps')
    plt.ylabel('Total ATP Consumed')
    plt.title('ATP Consumption by Motor Proteins Over Time')
    plt.legend()
    plt.show()

# Create motor proteins
kinesin = MotorProtein("Kinesin", 800, 8, 6, 1)
dynein = MotorProtein("Dynein", 600, 8, 6, 1)

# Run the simulation
intracellular_transport_simulation(kinesin, dynein, steps=50, track_length=100)

