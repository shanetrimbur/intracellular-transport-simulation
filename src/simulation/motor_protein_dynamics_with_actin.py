# File: src/simulation/motor_protein_dynamics_with_actin.py

import numpy as np
import random
import matplotlib.pyplot as plt

# Class definition for motor proteins (kinesin, dynein, and myosin)
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
        """Motor binds to the cytoskeletal track with a given probability."""
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

# Class for microtubule tracks (used by kinesin and dynein)
class MicrotubuleTrack:
    def __init__(self, length):
        self.length = length
        self.positions = np.zeros(length)  # 1D array to represent positions on the track

    def update_position(self, motor, position, direction):
        """Update motor position along the microtubule track."""
        if 0 <= position < self.length:
            self.positions[position] += motor.step() * direction

# Class for actin filaments (used by myosin)
class ActinTrack:
    def __init__(self, length):
        self.length = length
        self.positions = np.zeros(length)  # 1D array to represent positions on the track

    def update_position(self, motor, position, direction):
        """Update motor position along the actin track."""
        if 0 <= position < self.length:
            self.positions[position] += motor.step() * direction

# Class to simulate cytoplasmic crowding by adding random obstacles
class CytoplasmicCrowding:
    def __init__(self, track_length, obstacle_count):
        self.obstacles = np.random.choice(range(track_length), obstacle_count, replace=False)

    def check_collision(self, position):
        """Check if the motor encounters an obstacle."""
        return position in self.obstacles

# Simulation function with kinesin, dynein, and myosin motors on microtubule and actin tracks
def intracellular_transport_with_actin(motor1, motor2, motor3, steps, track_length, obstacle_count):
    mt_track = MicrotubuleTrack(track_length)  # Microtubule track for kinesin and dynein
    actin_track = ActinTrack(track_length)  # Actin track for myosin
    position_mt = track_length // 2  # Initial position on microtubule
    position_actin = track_length // 3  # Initial position on actin filament
    direction = 1  # Initial direction of movement
    crowding = CytoplasmicCrowding(track_length, obstacle_count)  # Introduce crowding

    motor1_atp_consumed = []  # ATP consumption for kinesin
    motor2_atp_consumed = []  # ATP consumption for dynein
    motor3_atp_consumed = []  # ATP consumption for myosin

    for step in range(steps):
        motor1.bind_to_track(0.8)  # 80% chance to bind (kinesin)
        motor2.bind_to_track(0.8)  # 80% chance to bind (dynein)
        motor3.bind_to_track(0.8)  # 80% chance to bind (myosin)

        # Check for collisions on the microtubule track
        if crowding.check_collision(position_mt):
            print(f"Step {step + 1}: Collision on microtubule at position {position_mt}, changing direction.")
            direction *= -1  # Reverse direction if a collision occurs on microtubule

        # Update positions on microtubule (kinesin and dynein)
        mt_track.update_position(motor1, position_mt, direction)
        mt_track.update_position(motor2, position_mt, -direction)  # Opposite direction for dynein

        # Check for collisions on the actin track
        if crowding.check_collision(position_actin):
            print(f"Step {step + 1}: Collision on actin at position {position_actin}, changing direction.")
            direction *= -1  # Reverse direction if a collision occurs on actin

        # Update position on actin track (myosin)
        actin_track.update_position(motor3, position_actin, direction)

        # Simulate ATP consumption for each motor
        atp_used_motor1 = motor1.consume_atp()
        atp_used_motor2 = motor2.consume_atp()
        atp_used_motor3 = motor3.consume_atp()

        motor1_atp_consumed.append(motor1.total_atp_used)
        motor2_atp_consumed.append(motor2.total_atp_used)
        motor3_atp_consumed.append(motor3.total_atp_used)

        print(f"Step {step + 1}: ATP consumed - Kinesin: {atp_used_motor1}, Dynein: {atp_used_motor2}, Myosin: {atp_used_motor3}")

    # Plot the ATP consumption of all motors over time
    plt.plot(motor1_atp_consumed, label='Kinesin ATP Consumption (Microtubule)')
    plt.plot(motor2_atp_consumed, label='Dynein ATP Consumption (Microtubule)')
    plt.plot(motor3_atp_consumed, label='Myosin ATP Consumption (Actin)')
    plt.xlabel('Simulation Steps')
    plt.ylabel('Total ATP Consumed')
    plt.title('ATP Consumption by Motor Proteins on Microtubule and Actin Filament')
    plt.legend()
    plt.show()

# Create motor proteins
kinesin = MotorProtein("Kinesin", 800, 8, 6, 1)  # Kinesin moves on microtubules
dynein = MotorProtein("Dynein", 600, 8, 6, 1)  # Dynein moves on microtubules
myosin = MotorProtein("Myosin", 500, 5, 5, 1)  # Myosin moves on actin filaments

# Run the simulation with microtubule (kinesin/dynein) and actin (myosin)
intracellular_transport_with_actin(kinesin, dynein, myosin, steps=50, track_length=100, obstacle_count=10)

