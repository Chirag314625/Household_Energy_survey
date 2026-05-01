# Air conditioner model placeholder
class AirConditioner:
    def __init__(self):
        # --- Parameters (Change these for different 'Variants') ---
        self.t_set = 22.0       # Target Temperature (°C)
        self.hysteresis = 1.0   # 1°C margin before turning on/off
        self.power_watt = 2000  # 2.0 kW AC unit
        self.cooling_eff = 3.5  # COP (Coefficient of Performance)
        
        # Room Physics
        self.temp_room = 28.0   # Starting room temp
        self.temp_outside = 35.0 # Hot summer day
        self.insulation_k = 0.05 # How much heat leaks in through walls
        self.air_mass_const = 0.1 # Thermal mass of the air in the room
        
        # Tracking
        self.is_on = False
        self.energy_used_wh = 0
        self.activity_log = []

    def simulate_step(self, dt_minutes=1):
        # 1. Control Logic (The Thermostat)
        if self.temp_room > (self.t_set + self.hysteresis):
            self.is_on = True
        elif self.temp_room < (self.t_set - self.hysteresis):
            self.is_on = False
            
        # 2. Physics Logic (The 'Modelica-style' Equations)
        # Heat gain from outside (Q_in)
        heat_gain = self.insulation_k * (self.temp_outside - self.temp_room)
        
        # Heat removed by AC (Q_out)
        # We multiply power by efficiency (COP) to get cooling capacity
        cooling_power = (self.power_watt * self.cooling_eff) / 1000 if self.is_on else 0
        heat_removal = cooling_power * self.air_mass_const
        
        # Update Room Temperature
        self.temp_room += (heat_gain - heat_removal)
        
        # 3. Energy & Activity Tracking (For your 'New Framework')
        current_power = self.power_watt if self.is_on else 0
        self.energy_used_wh += (current_power * (dt_minutes / 60))
        
        # Tracking 'Activity' (The absolute energy flow over time)
        self.activity_log.append(current_power)

        return self.temp_room, current_power


def calculate_daily(data):
    return (data['watts'] / data['eer'] * data['star_factor'] * data['hours'] * data['qty']) / 1000