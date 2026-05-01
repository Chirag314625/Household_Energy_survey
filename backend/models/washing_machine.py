# Washing machine model placeholder
class Washing_Machine:
    def __init__(self):
        # Define the "Program" states (Duration in minutes, Power in Watts)
        # Wash uses heater (high power), Spin uses motor (medium power)
        self.program = [
            {"state": "WASH", "duration": 30, "power": 2000}, 
            {"state": "RINSE", "duration": 15, "power": 300},
            {"state": "SPIN", "duration": 10, "power": 800}
        ]
        
        self.current_minute = 0
        self.total_energy_wh = 0
        self.activity_log = []

    def simulate_cycle(self):
        print("Starting Laundry Cycle...")
        
        for stage in self.program:
            state_name = stage["state"]
            duration = stage["duration"]
            power_level = stage["power"]
            
            for m in range(duration):
                # Calculate Energy: (Power * time_in_hours)
                minute_energy = power_level * (1/60)
                self.total_energy_wh += minute_energy
                
                # Tracking "Activity" (Reference 1 requirement)
                self.activity_log.append(power_level)
                self.current_minute += 1
                


def calculate_daily(data):
    return (data['watts'] * (data['duration'] / 60) * data['cycles'] * data['temp_factor']) / 1000