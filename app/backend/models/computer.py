# Computer model placeholder
class ComputingLoad:
    def __init__(self, type="Laptop"):
        self.type = type
        # Power profiles (Watts)
        if type == "Desktop":
            self.states = {"Sleep": 5, "Idle": 80, "High_Work": 250}
        else: # Laptop
            self.states = {"Sleep": 1, "Idle": 15, "High_Work": 65}
            
        self.current_state = "Idle"
        self.energy_used_wh = 0
        self.activity_log = []

    def simulate_step(self, hour, minute):
        # 1. Behavior Logic (Typical Student Schedule)
        if (9 <= hour <= 17) or (20 <= hour <= 23):
            self.current_state = "High_Work" # Coding/Studying
        elif (0 <= hour <= 8):
            self.current_state = "Sleep"
        else:
            self.current_state = "Idle"

        # 2. Power Calculation
        current_power = self.states[self.current_state]
        
        # 3. Energy & Activity (Ref 1)
        self.energy_used_wh += (current_power * (1 / 60))
        self.activity_log.append(current_power)
        
        return current_power


def calculate_daily(data):
    return ((data['watts'] + data['monitor']) * data['hours'] * data.get('qty', 1) + data['router'] * 24) / 1000

class ConnectivityLoad:
    def __init__(self):
        # Routers/Modems are basically constant 24/7
        self.power_watt = 12.0 # Standard Dual-band Router
        self.energy_used_wh = 0
        self.activity_log = []

    def simulate_step(self):
        # No complex logic, just constant draw
        current_power = self.power_watt
        self.energy_used_wh += (current_power * (1 / 60))
        self.activity_log.append(current_power)
        return current_power