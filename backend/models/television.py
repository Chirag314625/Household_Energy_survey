# Television model placeholder
class Television:
    def __init__(self, size_inches=55, tech="LED"):
        # --- Parameters ---
        self.size = size_inches
        self.tech = tech
        
        # Base power calculation (LED ~0.12W per sq inch, OLED ~0.15W)
        power_factor = 0.15 if tech == "OLED" else 0.12
        self.active_power = self.size * 2.0 * power_factor # Approximation
        self.standby_power = 1.5 # 1.5 Watts even when 'off'
        
        # Tracking
        self.is_on = False
        self.energy_used_wh = 0
        self.activity_log = []

    def simulate_step(self, hour, minute):
        # 1. User Behavior Logic (Schedule)
        # Morning news: 7:30 AM - 8:30 AM
        # Prime time: 7:00 PM - 11:00 PM (19:00 - 23:00)
        if (7 == hour and minute >= 30) or (8 == hour and minute <= 30) or (19 <= hour <= 23):
            self.is_on = True
        else:
            self.is_on = False
            
        # 2. Power Logic
        current_power = self.active_power if self.is_on else self.standby_power
        
        # 3. Energy & Activity (Ref 1)
        self.energy_used_wh += (current_power * (1 / 60))
        self.activity_log.append(current_power)
        
        return current_power


def calculate_daily(data):
    return (data['watts'] * data['qty'] * data['hours']) / 1000