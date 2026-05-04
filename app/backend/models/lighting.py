# Lighting model placeholder
class LightingSystem:
    def __init__(self, room_name="Living Room"):
        self.room_name = room_name
        # Power per bulb type (Watts)
        self.bulb_types = {
            "LED": 9,
            "CFL": 20,
            "Incandescent": 60
        }
        
        # Configuration
        self.active_type = "LED"
        self.num_bulbs = 4
        self.is_on = False
        
        # Tracking
        self.energy_used_wh = 0
        self.activity_log = []

    def set_bulb_type(self, type_name):
        if type_name in self.bulb_types:
            self.active_type = type_name

    def simulate_step(self, hour, minute):
        # 1. Occupancy Logic (When are lights usually on?)
        # Logic: On between 6 PM (18:00) and 11 PM (23:00)
        # And briefly in the morning 7 AM to 8 AM
        if (18 <= hour <= 23) or (7 <= hour <= 8):
            self.is_on = True
        else:
            self.is_on = False
            
        # 2. Power Calculation
        # Total Power = Number of Bulbs * Wattage of Active Type
        current_power = (self.num_bulbs * self.bulb_types[self.active_type]) if self.is_on else 0
        
        # 3. Energy & Activity (Ref 1)
        self.energy_used_wh += (current_power * (1 / 60))
        self.activity_log.append(current_power)
        
        return current_power


def calculate_daily(data):
    return (data['watts'] * data['qty'] * data['hours']) / 1000