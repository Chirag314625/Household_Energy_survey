# Kitchen model placeholder
class KitchenAppliances:
    def __init__(self):
        # Rated Power in Watts
        self.catalog = {
            "Coffee_Maker": 900,
            "Blender": 400,
            "Toaster_Oven": 1500,
            "Air_Fryer": 1800,
            "Mixer": 300
        }
        
        # Energy and Activity tracking
        self.total_energy_wh = 0
        self.activity_log = []

    def run_task(self, appliance_name, duration_minutes):
        """Simulates running a kitchen appliance for a set time"""
        if appliance_name in self.catalog:
            power = self.catalog[appliance_name]
            # Energy = Power * (minutes/60)
            task_energy = power * (duration_minutes / 60)
            self.total_energy_wh += task_energy
            
            # For the simulation log, we add 'duration' minutes of high power
            # and the rest is zero.
            return [power] * int(duration_minutes)
        return []

    def simulate_day(self):
        # A typical kitchen schedule (1440 minutes)
        day_log = [0] * 1440
        
        # Morning: 7:30 AM (Minute 450) - Coffee and Toast
        day_log[450:460] = self.run_task("Coffee_Maker", 10)
        day_log[460:465] = self.run_task("Toaster_Oven", 5)
        
        # Afternoon: 1:00 PM (Minute 780) - Blender for smoothie
        day_log[780:782] = self.run_task("Blender", 2)
        
        # Evening: 8:00 PM (Minute 1200) - Air Fryer for dinner
        day_log[1200:1220] = self.run_task("Air_Fryer", 20)
        
        self.activity_log = day_log
        return day_log


def calculate_daily(data):
    micro = data['micro_watts'] * (data['micro_mins'] / 60)
    mixer = data['mixer_watts'] * (data['mixer_mins'] / 60)
    ind = data['induction_watts'] * data['induction_hours']
    return (micro + mixer + ind) / 1000