# File: src/simulation/motor_protein_dynamics_with_energy_constraints.py

class EnergyModule:
    def __init__(self, initial_atp):
        self.atp_level = initial_atp

    def consume_atp(self, amount):
        self.atp_level = max(0, self.atp_level - amount)

    def is_atp_depleted(self):
        return self.atp_level <= 0

def intracellular_transport_with_energy(motor1, motor2, steps, track_length, initial_atp):
    energy = EnergyModule(initial_atp)

    for step in range(steps):
        if not energy.is_atp_depleted():
            motor1.bind_to_track(0.8)
            motor2.bind_to_track(0.8)
            
            atp_consumed = motor1.consume_atp() + motor2.consume_atp()
            energy.consume_atp(atp_consumed)

            print(f"Step {step + 1}: ATP level: {energy.atp_level}")
        else:
            print("ATP depleted! Motors stop.")

# Simulate with energy constraints
intracellular_transport_with_energy(kinesin, dynein, steps=50, track_length=100, initial_atp=200)

