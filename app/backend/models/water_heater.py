# Water heater model placeholder
class WaterHeater:
    def __init__(self, capacity_liters=25, power_watt=3000):
        # --- Parameters ---
        self.capacity = capacity_liters # e.g., 15L, 25L
        self.power_watt = power_watt    # 3.0 kW Geyser
        self.t_set = 60.0               # Target hot water temp
        self.t_deadband = 2.0           # Hysteresis margin
        
        # Physics Constants
        self.temp_water = 25.0          # Starting water temp
        self.temp_ambient = 25.0        # Room temp
        self.insulation_k = 0.001       # Heat loss coefficient
        self.specific_heat_water = 4186 # Joules/kg·°C
        
        # Tracking
        self.is_heating = False
        self.energy_used_wh = 0
        self.activity_log = []

    def use_hot_water(self, liters):
        """Simulates a shower: replaces hot water with cold 25°C water"""
        fraction_replaced = min(liters / self.capacity, 1.0)
        self.temp_water = (self.temp_water * (1 - fraction_replaced)) + (25.0 * fraction_replaced)

    def simulate_step(self, hour, minute, dt_seconds=60):
        # 1. User Behavior: "The Shower Event"
        # Logic: Someone takes a 15L shower at 8:00 AM
        if hour == 8 and minute == 0:
            self.use_hot_water(15)

        # 2. Thermostatic Control Logic
        if self.temp_water < (self.t_set - self.t_deadband):
            self.is_heating = True
        elif self.temp_water >= self.t_set:
            self.is_heating = False
            
        # 3. Physics Equations (Modelica style)
        # Heat gain from element (Joules)
        q_in = (self.power_watt * dt_seconds) if self.is_heating else 0
        # Heat loss to room (Joules)
        q_loss = self.insulation_k * (self.temp_water - self.temp_ambient) * dt_seconds
        
        # Temperature Change: dT = Q / (mass * specific_heat)
        mass = self.capacity # 1 Liter water = 1 kg
        self.temp_water += (q_in - q_loss) / (mass * self.specific_heat_water)
        
        # 4. Energy & Activity (Ref 1)
        current_power = self.power_watt if self.is_heating else 0
        self.energy_used_wh += (current_power * (dt_seconds / 3600))
        self.activity_log.append(current_power)
        
        return current_power


def calculate_daily(data):
    return (data['watts'] * data['qty'] * data['hours']) / 1000