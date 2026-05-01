# Ceiling fan model placeholder
class CeilingFan:
    def __init__(self):
        # --- Parameters ---
        self.max_power_watt = 75.0  # Power at Speed 5
        self.current_speed = 0       # 0 (Off) to 5 (Max)
        
        # Power levels for speeds 1-5 (Watts)
        self.speed_map = {0: 0, 1: 15, 2: 30, 3: 45, 4: 60, 5: 75}
        
        # Tracking
        self.energy_used_wh = 0
        self.activity_log = []

    def set_speed(self, speed):
        """Sets the fan speed (0-5)"""
        if 0 <= speed <= 5:
            self.current_speed = speed

    def simulate_step(self, dt_minutes=1):
        # 1. Get current power based on speed
        current_power = self.speed_map[self.current_speed]
        
        # 2. Energy Calculation
        self.energy_used_wh += (current_power * (dt_minutes / 60))
        
        # 3. 'Activity' Tracking (Ref 1 Requirement)
        # Even though a fan is low power, it runs for long hours, 
        # so its 'Cumulative Activity' is high.
        self.activity_log.append(current_power)
        
        return current_power


def calculate_daily(data):
    return (data['watts'] * data['qty'] * data['hours'] * data.get('speed', 1)) / 1000