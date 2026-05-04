# Refrigerator model placeholder

class Refrigerator:
    def __init__(self):
        # Parameters
        self.t_set = 4.0  # Target temp
        self.hysteresis = 1.0  # Buffer
        self.power_watt = 150  # Compressor power
        self.temp_inside = 10.0
        self.temp_ambient = 25.0
        self.insulation_k = 0.02

        # Data tracking
        self.energy_used = 0
        self.activity_log = []

    def simulate_step(self, dt_minutes=1):
        # 1. Control Logic (The "Brain")
        is_on = self.temp_inside > (self.t_set + self.hysteresis)

        # 2. Physics Logic (The "Body")
        heat_leak = self.insulation_k * (self.temp_ambient - self.temp_inside)
        cooling = 0.5 if is_on else 0  # Simple cooling factor

        self.temp_inside += (heat_leak - cooling)

        # 3. Energy Calculation
        current_power = self.power_watt if is_on else 0
        self.energy_used += (current_power * (dt_minutes / 60))

        # This is the "Activity" from your Reference 1!
        self.activity_log.append(abs(current_power))


def calculate_daily(data):
    return (data['watts'] * 24 * data['duty'] * data['qty']) / 1000