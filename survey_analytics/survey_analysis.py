import os
os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(os.path.dirname(__file__)), ".matplotlib")
)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import matplotlib.cm as cm  # Import colormap for diverse colors
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# ==================== APPLIANCE SIMULATION MODELS ====================

class AirConditionerModel:
    """Simulates AC operation with thermal physics and control logic"""
    def __init__(self, power_watt=2000, cop=3.5):
        self.t_set = 22.0
        self.hysteresis = 1.0
        self.power_watt = power_watt
        self.cooling_eff = cop
        self.temp_room = 28.0
        self.temp_outside = 35.0
        self.insulation_k = 0.05
        self.air_mass_const = 0.1
        self.is_on = False
        self.energy_used_wh = 0
        self.activity_log = []

    def simulate_step(self, dt_minutes=1, outside_temp=35.0):
        self.temp_outside = outside_temp
        if self.temp_room > (self.t_set + self.hysteresis):
            self.is_on = True
        elif self.temp_room < (self.t_set - self.hysteresis):
            self.is_on = False
        
        heat_gain = self.insulation_k * (self.temp_outside - self.temp_room)
        cooling_power = (self.power_watt * self.cooling_eff) / 1000 if self.is_on else 0
        heat_removal = cooling_power * self.air_mass_const
        
        self.temp_room += (heat_gain - heat_removal)
        current_power = self.power_watt if self.is_on else 0
        self.energy_used_wh += (current_power * (dt_minutes / 60))
        self.activity_log.append(current_power)
        return self.temp_room, current_power


class CeilingFanModel:
    """Simulates ceiling fan operation with variable speeds"""
    def __init__(self, max_power=75.0):
        self.max_power_watt = max_power
        self.current_speed = 0
        self.speed_map = {0: 0, 1: 15, 2: 30, 3: 45, 4: 60, 5: 75}
        self.energy_used_wh = 0
        self.activity_log = []

    def set_speed(self, speed):
        if 0 <= speed <= 5:
            self.current_speed = speed

    def simulate_step(self, dt_minutes=1):
        current_power = self.speed_map[self.current_speed]
        self.energy_used_wh += (current_power * (dt_minutes / 60))
        self.activity_log.append(current_power)
        return current_power


class LightingSystemModel:
    """Simulates lighting system with multiple bulb types"""
    def __init__(self, room_name="Living Room", num_bulbs=4):
        self.room_name = room_name
        self.bulb_types = {"LED": 9, "CFL": 20, "Incandescent": 60}
        self.active_type = "LED"
        self.num_bulbs = num_bulbs
        self.is_on = False
        self.energy_used_wh = 0
        self.activity_log = []

    def set_bulb_type(self, type_name):
        if type_name in self.bulb_types:
            self.active_type = type_name

    def simulate_step(self, hour, minute):
        if (18 <= hour <= 23) or (7 <= hour <= 8):
            self.is_on = True
        else:
            self.is_on = False
        
        current_power = (self.num_bulbs * self.bulb_types[self.active_type]) if self.is_on else 0
        self.energy_used_wh += (current_power * (1 / 60))
        self.activity_log.append(current_power)
        return current_power


class WashingMachineModel:
    """Simulates washing machine cycle stages"""
    def __init__(self):
        self.program = [
            {"state": "WASH", "duration": 30, "power": 2000},
            {"state": "RINSE", "duration": 15, "power": 300},
            {"state": "SPIN", "duration": 10, "power": 800}
        ]
        self.current_minute = 0
        self.total_energy_wh = 0
        self.activity_log = []

    def simulate_cycle(self):
        for stage in self.program:
            duration = stage["duration"]
            power_level = stage["power"]
            for m in range(duration):
                minute_energy = power_level * (1/60)
                self.total_energy_wh += minute_energy
                self.activity_log.append(power_level)
                self.current_minute += 1
        return self.total_energy_wh


class TelevisionModel:
    """Simulates TV operation with size and technology factors"""
    def __init__(self, size_inches=55, tech="LED"):
        self.size = size_inches
        self.tech = tech
        power_factor = 0.15 if tech == "OLED" else 0.12
        self.active_power = self.size * 2.0 * power_factor
        self.standby_power = 1.5
        self.is_on = False
        self.energy_used_wh = 0
        self.activity_log = []

    def simulate_step(self, hour, minute):
        if (7 == hour and minute >= 30) or (8 == hour and minute <= 30) or (19 <= hour <= 23):
            self.is_on = True
        else:
            self.is_on = False
        
        current_power = self.active_power if self.is_on else self.standby_power
        self.energy_used_wh += (current_power * (1 / 60))
        self.activity_log.append(current_power)
        return current_power


class RefrigeratorModel:
    """Simulates refrigerator compressor operation with thermostat control"""
    def __init__(self, power_watt=150):
        self.t_set = 4.0
        self.hysteresis = 1.0
        self.power_watt = power_watt
        self.temp_inside = 10.0
        self.temp_ambient = 25.0
        self.insulation_k = 0.02
        self.energy_used = 0
        self.activity_log = []

    def simulate_step(self, dt_minutes=1):
        is_on = self.temp_inside > (self.t_set + self.hysteresis)
        heat_leak = self.insulation_k * (self.temp_ambient - self.temp_inside)
        cooling = 0.5 if is_on else 0
        self.temp_inside += (heat_leak - cooling)
        
        current_power = self.power_watt if is_on else 0
        self.energy_used += (current_power * (dt_minutes / 60))
        self.activity_log.append(abs(current_power))
        return current_power


class ComputingLoadModel:
    """Simulates computer usage with different states (Sleep, Idle, High Work)"""
    def __init__(self, device_type="Laptop"): 
        self.type = device_type
        if device_type == "Desktop":
            self.states = {"Sleep": 5, "Idle": 80, "High_Work": 250}
        else:
            self.states = {"Sleep": 1, "Idle": 15, "High_Work": 65}
        self.current_state = "Idle"
        self.energy_used_wh = 0
        self.activity_log = []

    def simulate_step(self, hour, minute):
        if (9 <= hour <= 17) or (20 <= hour <= 23):
            self.current_state = "High_Work"
        elif (0 <= hour <= 8):
            self.current_state = "Sleep"
        else:
            self.current_state = "Idle"
        
        current_power = self.states[self.current_state]
        self.energy_used_wh += (current_power * (1 / 60))
        self.activity_log.append(current_power)
        return current_power


class WaterHeaterModel:
    """Simulates electric water heater with thermostat control"""
    def __init__(self, capacity_liters=25, power_watt=3000):
        self.capacity = capacity_liters
        self.power_watt = power_watt
        self.t_set = 60.0
        self.t_deadband = 2.0
        self.temp_water = 25.0
        self.temp_ambient = 25.0
        self.insulation_k = 0.001
        self.specific_heat_water = 4186
        self.is_heating = False
        self.energy_used_wh = 0
        self.activity_log = []

    def use_hot_water(self, liters):
        fraction_replaced = min(liters / self.capacity, 1.0)
        self.temp_water = (self.temp_water * (1 - fraction_replaced)) + (25.0 * fraction_replaced)

    def simulate_step(self, hour, minute, dt_seconds=60):
        if hour == 8 and minute == 0:
            self.use_hot_water(15)
        
        if self.temp_water < (self.t_set - self.t_deadband):
            self.is_heating = True
        elif self.temp_water >= self.t_set:
            self.is_heating = False
        
        q_in = (self.power_watt * dt_seconds) if self.is_heating else 0
        q_loss = self.insulation_k * (self.temp_water - self.temp_ambient) * dt_seconds
        mass = self.capacity
        self.temp_water += (q_in - q_loss) / (mass * self.specific_heat_water)
        
        current_power = self.power_watt if self.is_heating else 0
        self.energy_used_wh += (current_power * (dt_seconds / 3600))
        self.activity_log.append(current_power)
        return current_power


class KitchenAppliancesModel:
    """Simulates kitchen appliances (coffee maker, blender, toaster, etc.)"""
    def __init__(self):
        self.catalog = {
            "Coffee_Maker": 900,
            "Blender": 400,
            "Toaster_Oven": 1500,
            "Air_Fryer": 1800,
            "Mixer": 300
        }
        self.total_energy_wh = 0
        self.activity_log = []

    def run_task(self, appliance_name, duration_minutes):
        if appliance_name in self.catalog:
            power = self.catalog[appliance_name]
            task_energy = power * (duration_minutes / 60)
            self.total_energy_wh += task_energy
            return [power] * int(duration_minutes)
        return []

    def simulate_day(self):
        day_log = [0] * 1440
        day_log[450:460] = self.run_task("Coffee_Maker", 10)
        day_log[460:465] = self.run_task("Toaster_Oven", 5)
        day_log[780:782] = self.run_task("Blender", 2)
        day_log[1200:1220] = self.run_task("Air_Fryer", 20)
        self.activity_log = day_log
        return day_log


# ==================== APPLIANCE ANALYSIS FRAMEWORK ====================

class ApplianceSimulator:
    """Manages and simulates all household appliances for detailed energy analysis"""
    def __init__(self):
        self.appliances = {}
        self.initialize_appliances()

    def initialize_appliances(self):
        self.appliances = {
            'AC': AirConditionerModel(),
            'Ceiling_Fan': CeilingFanModel(),
            'Living_Room_Lights': LightingSystemModel("Living Room", 4),
            'Bedroom_Lights': LightingSystemModel("Bedroom", 3),
            'Refrigerator': RefrigeratorModel(),
            'Washing_Machine': WashingMachineModel(),
            'Television': TelevisionModel(55, "LED"),
            'Laptop': ComputingLoadModel("Laptop"),
            'Desktop': ComputingLoadModel("Desktop"),
            'Water_Heater': WaterHeaterModel(),
            'Kitchen_Appliances': KitchenAppliancesModel()
        }

    def simulate_24_hours(self):
        """Simulate all appliances for 24 hours and collect energy data"""
        daily_energy = {}
        hourly_data = []
        
        for hour in range(24):
            for minute in range(0, 60, 15):  # Simulate 15 minute intervals
                hour_data = {}
                total_power = 0
                
                for name, appliance in self.appliances.items():
                    if isinstance(appliance, AirConditionerModel):
                        outside_temp = 28 if 8 <= hour <= 18 else 24
                        _, power = appliance.simulate_step(15, outside_temp)
                    elif isinstance(appliance, LightingSystemModel):
                        power = appliance.simulate_step(hour, minute)
                    elif isinstance(appliance, TelevisionModel):
                        power = appliance.simulate_step(hour, minute)
                    elif isinstance(appliance, ComputingLoadModel):
                        power = appliance.simulate_step(hour, minute)
                    elif isinstance(appliance, RefrigeratorModel):
                        power = appliance.simulate_step(15)
                    elif isinstance(appliance, WaterHeaterModel):
                        power = appliance.simulate_step(hour, minute, 900)
                    else:
                        power = 0
                    
                    hour_data[name] = power
                    total_power += power
                
                hourly_data.append({'hour': hour, 'minute': minute, 'total_power_w': total_power, **hour_data})
        
        # Calculate daily totals
        for name, appliance in self.appliances.items():
            if hasattr(appliance, 'energy_used_wh'):
                daily_energy[name] = appliance.energy_used_wh
            elif hasattr(appliance, 'energy_used'):
                daily_energy[name] = appliance.energy_used
        
        return daily_energy, pd.DataFrame(hourly_data)

    def get_peak_load_analysis(self, hourly_df):
        """Analyze peak load patterns throughout the day"""
        peak_data = hourly_df.groupby('hour')['total_power_w'].agg(['max', 'mean', 'min'])
        return peak_data

    def get_appliance_efficiency_ratings(self, daily_energy):
        """Calculate efficiency ratings for each appliance"""
        max_energy = max(daily_energy.values()) if daily_energy.values() else 1
        efficiency = {name: ((max_energy - energy) / max_energy * 100) for name, energy in daily_energy.items()}
        return efficiency


# --- Appliance and Usage Data (Typical Values Only) ---
# Appliance power consumption in Watts (now single typical value)
APPLIANCE_POWER_TYPICAL = {
    # Refrigerator Sizes (based on cubic feet, approximate wattage)
    'Refrigerator_Half_Compact': 40,  # W (for Half-size or compact)
    'Refrigerator_Small': 50,  # W (for Small 17.5 cubic feet or less)
    'Refrigerator_Medium': 75,  # W (for Medium 17.6 to 22.5 cubic feet)
    'Refrigerator_Large': 100,  # W (for Large 22.6 to 29.5 cubic feet)
    'Refrigerator_XLarge': 150,  # W (for Very large bigger than 29.5 cubic feet)

    # Refrigerator Age Factors (multipliers for base consumption)
    'Refrigerator_Age_Less_2_Factor': 1.0,  # Less than 2 years old (baseline)
    'Refrigerator_Age_2_4_Factor': 1.05,  # 2 to 4 years old (5% more)
    'Refrigerator_Age_5_9_Factor': 1.10,  # 5 to 9 years old (10% more)
    'Refrigerator_Age_10_14_Factor': 1.25,  # 10 to 14 years old (25% more)
    'Refrigerator_Age_15_19_Factor': 1.35,  # 15 to 19 years old (35% more)
    'Refrigerator_Age_20_Plus_Factor': 1.50,  # 20 or more years old (50% more)

    'AC': 1500,  # W (e.g., 1.5 Ton)
    # AC Age Factors (multipliers for base consumption) - NEW
    'AC_Age_Less_2_Factor': 1.0,
    'AC_Age_2_4_Factor': 1.03,
    'AC_Age_5_9_Factor': 1.08,
    'AC_Age_10_14_Factor': 1.15,
    'AC_Age_15_19_Factor': 1.25,
    'AC_Age_20_Plus_Factor': 1.40,

    'Ceiling_Fan': 75,  # W
    'Lighting_LED': 10,  # W per bulb
    'Lighting_CFL': 15,  # W per bulb
    'Lighting_Incandescent': 60,  # W per bulb

    # TV Sizes (approximate wattage)
    'TV_Size_Less_27_inches': 50,  # W
    'TV_Size_27_39_inches': 75,  # W
    'TV_Size_40_59_inches': 120,  # W
    'TV_Size_60_or_larger_inches': 180,  # W (now explicitly mapped)

    # TV Types (approximate wattage, general averages) - These can be refined if specific models/years are known
    'TV_Type_CRT': 100,  # W (older, higher consumption)
    'TV_Type_LCD': 80,  # W
    'TV_Type_LED': 60,  # W (generally more efficient than LCD)
    'TV_Type_Plasma': 200,  # W (higher consumption)
    'TV_Type_OLED': 70,  # W (efficient, but can vary)

    'Water_Heater_Electric': 2000,  # W (geyser)
    'Clothes_Washer': 500,  # W (effective during cycle)
    'Clothes_Dryer_Electric': 3000,  # W
    'Desktop_Computer': 100,  # W
    'Laptop_Computer': 50,  # W
    'Wireless_Router': 10,  # W
    'Small_Appliance_Toaster': 1000,  # W
    'Small_Appliance_Coffee_Maker': 800,  # W
    'Small_Appliance_Blender': 500,  # W
    'Small_Appliance_Rice_Cooker': 700,  # W
}

# Usage hours/frequency (now single typical value)
USAGE_HOURS_TYPICAL = {
    'AC_Daily_Hours': 8,  # hours/day during peak months
    'Ceiling_Fan_Daily_Hours': 12,  # hours/day
    'Lighting_4hr+_Daily_Hours': 6,  # hours/day for bulbs used >4hr
    'Lighting_Other_Daily_Hours': 2,  # hours/day for other bulbs
    'TV_Daily_Hours_Factor': 1.0,  # Multiplier for reported TV hours
    'Water_Heater_Daily_Hours': 1.0,  # hours/day
    'Clothes_Washer_Weekly_Use_Factor': 1.0,  # Multiplier for reported washer usage
    'Clothes_Dryer_Weekly_Hours': 1.5,  # hours/week
    'Desktop_Daily_Hours': 6,  # hours/day
    'Laptop_Daily_Hours': 8,  # hours/day
    'Small_Appliance_Daily_Hours_Factor': 1.0,  # Multiplier for small appliance daily hours
    'Other_Use_Per_Adult_KWH': 100,  # kWh/year per adult
    'Other_Use_Default_KWH': 200,  # kWh/year default
}

# Fuel conversion factors (BTU per unit) and estimated quantities (now single typical value)
FUEL_BTU_TYPICAL = {
    'LPG_KG_TO_BTU': 47500,  # BTU per kg of LPG
    'FUEL_OIL_LITRE_TO_BTU': 38000,  # BTU per litre of fuel oil
    'NATURAL_GAS_SCM_TO_BTU': 35000,  # BTU per Standard Cubic Meter (SCM)
    'WOOD_KG_TO_BTU': 7000,  # BTU per kg of wood (highly variable)
    'NATURAL_GAS_TYPICAL_ANNUAL_SCM': 150,  # SCM/year
    'WOOD_TYPICAL_ANNUAL_KG': 500,  # kg/year
}


# --- Helper function for safe numeric conversion ---
def safe_numeric_conversion(value, default=0):
    try:
        # Check for non-numeric strings that pandas might convert to NaN
        if isinstance(value, str):
            # Attempt to clean string if it contains non-numeric characters before conversion
            # e.g., "₹50,000" -> "50000"
            cleaned_value = value.replace('₹', '').replace(',', '').strip()
            if cleaned_value.replace('.', '', 1).isdigit():  # Check if it's purely numeric after cleaning
                return pd.to_numeric(cleaned_value, errors='coerce')
            else:
                return default  # If still not numeric, return default
        return pd.to_numeric(value, errors='coerce')
    except:
        return default


# --- Define Classes for Each Category ---
class HouseholdInformation:
    def __init__(self, row):
        self._id = row.get('_id')
        self.name = row.get('Q0_name')
        self.city = row.get('Q1_City')
        self.pincode = row.get('Q1_Pincode')
        self.num_adults = safe_numeric_conversion(row.get('Q2_num_adults'))


class HomeCharacteristics:
    def __init__(self, row):
        self.home_type = row.get('Q3_home_type')
        self.ownership = row.get('Q4_ownership')
        self.year_built = row.get('Q5_year_built')
        self.move_in_year = row.get('Q6_move_in_year')
        self.sq_ft_home = safe_numeric_conversion(row.get('Q7_sq_ft_home'))
        self.sq_ft_basement = row.get('Q8_sq_ft_basement')
        self.sq_ft_attic = row.get('Q8_sq_ft_attic')
        self.sq_ft_garage = row.get('Q8_sq_ft_garage')


class Refrigerator:
    def __init__(self, row):
        self.num_refrigerators = safe_numeric_conversion(row.get('Q9_num_refrigerators'))
        self.size = str(row.get('Q10_refrigerator_size')).lower()
        self.type = row.get('Q11_refrigerator_type')
        self.age = str(row.get('Q12_refrigerator_age')).lower()


class Stove:
    def __init__(self, row):
        self.num_stoves = safe_numeric_conversion(row.get('Q13_num_stoves'))
        self.fuel = str(row.get('Q14_stove_fuel')).lower()
        self.other_fuel = row.get('Q14_other')


class WallOven:
    def __init__(self, row):
        self.num_wall_ovens = safe_numeric_conversion(row.get('Q15_num_wall_ovens'))
        self.fuel = str(row.get('Q16_wall_oven_fuel')).lower()
        self.other_fuel = row.get('Q16_other')
        self.usage = safe_numeric_conversion(row.get('Q17_wall_oven_usage'))


class SmallKitchenAppliances:
    def __init__(self, row):
        self.toaster = str(row.get('Q18_Toaster')).lower()
        self.toaster_oven = str(row.get('Q18_Toaster_oven')).lower()
        self.coffee_maker = str(row.get('Q18_Coffee_maker')).lower()
        self.crock_pot_or_slow_cooker = str(row.get('Q18_Crock_pot_or_slow_cooker')).lower()
        self.food_processor = str(row.get('Q18_Food_processor')).lower()
        self.rice_cooker = str(row.get('Q18_Rice_cooker')).lower()
        self.blender_or_juicer = str(row.get('Q18_Blender_or_juicer')).lower()
        self.other_specify = row.get('Q18_Other__please_specify_')
        self.other_specify_detail = row.get('Q18_Other__please_specify__other')


class ClothesWasher:
    def __init__(self, row):
        self.has_clothes_washer = str(row.get('Q19_has_clothes_washer')).lower()
        self.usage = safe_numeric_conversion(row.get('Q20_clothes_washer_usage'))
        self.age = row.get('Q21_clothes_washer_age')


class ClothesDryer:
    def __init__(self, row):
        self.has_clothes_dryer = str(row.get('Q22_has_clothes_dryer')).lower()
        self.type = row.get('Q23_uses_clothes_dryer_type')
        self.fuel = str(row.get('Q24_clothes_dryer_fuel')).lower()
        self.other_fuel = row.get('Q24_other')
        self.age = row.get('Q25_clothes_dryer_age')


class Televisions:
    def __init__(self, row):
        self.num_televisions = safe_numeric_conversion(row.get('Q26_num_televisions'))
        self.tv_size = str(row.get('Q27_tv_size')).lower()
        self.tv_type = str(row.get('Q28_tv_type')).lower()  # Ensure type is also lowercased for matching
        self.tv_other = row.get('Q28_other')
        self.tv_daily_hours = safe_numeric_conversion(row.get('Q29_tv_daily_hours'))


class ComputersConnectivity:
    def __init__(self, row):
        self.num_desktop_computers = safe_numeric_conversion(row.get('Q30_num_desktop_computers'))
        self.num_laptop_computers = safe_numeric_conversion(row.get('Q30_num_laptop_computers'))
        self.num_tablets_ereaders = safe_numeric_conversion(row.get('Q30_num_tablets_ereaders'))
        self.num_printers_scanners = safe_numeric_conversion(row.get('Q30_num_printers_scanners_etc'))
        self.num_smart_phones = safe_numeric_conversion(row.get('Q30_num_smart_phones'))
        self.num_other_cell_phones = safe_numeric_conversion(row.get('Q30_num_other_cell_phones'))
        self.access_internet = str(row.get('Q31_access_internet')).lower()
        self.has_wireless_router = str(row.get('Q32_has_wireless_router')).lower()


class HeatingEquipment:
    def __init__(self, row):
        self.is_home_heated = str(row.get('Q33_is_home_heated')).lower()
        self.main_heating_equipment = row.get('Q34_main_heating_equipment')
        self.main_heating_equipment_other = row.get('Q34_other')
        self.main_heating_equipment_age = row.get('Q35_main_heating_equipment_age')
        self.main_heating_fuel = str(row.get('Q36_main_heating_fuel')).lower()
        self.main_heating_fuel_other = row.get('Q36_other')


class CoolingEquipment:
    def __init__(self, row):
        self.has_ac = str(row.get('Q37_has_ac')).lower()
        self.uses_central_ac = str(row.get('Q38_uses_central_ac')).lower()  # Ensure lowercased
        self.central_ac_is_heat_pump = row.get('Q39_central_ac_is_heat_pump')
        self.central_ac_age = str(row.get('Q40_central_ac_age')).lower()  # Ensure lowercased
        self.temp_summer_day_home = safe_numeric_conversion(row.get('Q41_temp_summer_day_home'))
        self.temp_summer_day_away = safe_numeric_conversion(row.get('Q41_temp_summer_day_away'))
        self.temp_summer_night = safe_numeric_conversion(row.get('Q41_temp_summer_night'))
        self.num_ceiling_fans = safe_numeric_conversion(row.get('Q42_num_ceiling_fans'))
        self.num_floor_window_fans = safe_numeric_conversion(row.get('Q42_num_floor_window_fans'))
        self.num_whole_house_fans = safe_numeric_conversion(row.get('Q42_num_whole_house_fans'))
        self.num_attic_fans = safe_numeric_conversion(row.get('Q42_num_attic_fans'))


class WaterHeater:
    def __init__(self, row):
        self.has_water_heater = str(row.get('Q43_has_water_heater')).lower()
        self.size = row.get('Q44_water_heater_size')
        self.age = row.get('Q45_water_heater_age')
        self.fuel = str(row.get('Q46_water_heater_fuel')).lower()
        self.other_fuel = row.get('Q46_other')


class Lighting:
    def __init__(self, row):
        self.num_light_bulbs_total = safe_numeric_conversion(row.get('Q47_num_light_bulbs_total'))
        self.num_light_bulbs_4hr_plus = safe_numeric_conversion(row.get('Q48_num_light_bulbs_4hr_plus'))
        self.incandescent = str(row.get('Q49_Incandescent')).lower()
        self.natural_gas_lights = str(row.get('Q49_Natural_gas_lights')).lower()
        self.cfl = str(row.get('Q49_CFL__compact_fluorescent_lamp_')).lower()
        self.led = str(row.get('Q49_LED__light_emitting_diode_')).lower()


class EnergyConsumptionCosts:
    def __init__(self, row):
        self.electricity_payment_responsibility = row.get('Q50_electricity_payment_responsibility')
        self.electricity_payment_responsibility_other = row.get('Q50_other')
        self.natural_gas_payment_responsibility = str(row.get('Q51_natural_gas_payment_responsibility')).lower()
        self.natural_gas_payment_responsibility_other = row.get('Q51_other')
        self.fuel_oil_payment_responsibility = row.get('Q52_fuel_oil_payment_responsibility')
        self.fuel_oil_payment_responsibility_other = row.get('Q52_other')
        self.has_backup_generator = row.get('Q53_has_backup_generator')
        self.on_site_electricity_generation = row.get('Q54_on_site_electricity_generation')
        self.on_site_electricity_generation_other = row.get('Q54_other')
        self.avg_annual_electricity_spending = row.get('Q55_avg_annual_electricity_spending')
        self.receives_fuel_oil_deliveries = str(row.get('Q56_receives_fuel_oil_deliveries')).lower()
        self.fuel_oil_tank_size = safe_numeric_conversion(row.get('Q57_fuel_oil_tank_size'))
        self.fuel_oil_num_deliveries_past_year = safe_numeric_conversion(
            row.get('Q57_fuel_oil_num_deliveries_past_year'))
        self.fuel_oil_total_cost_past_year = row.get('Q57_fuel_oil_total_cost_past_year')
        self.uses_wood_for_fuel = str(row.get('Q58_uses_wood_for_fuel')).lower()
        self.wood_pellets_total_amount_past_year = safe_numeric_conversion(
            row.get('Q59_wood_pellets_total_amount_past_year'))
        self.wood_total_cost_past_year = row.get('Q59_wood_total_cost_past_year')
        self.num_lpg_propane_cylinders_year = safe_numeric_conversion(row.get('Q60_num_lpg_propane_cylinders_year'))
        self.last_electricity_bill_amount = row.get('Q61_last_electricity_bill_amount')
        self.last_electricity_consumption = row.get('Q62_last_electricity_consumption')
        # Store the entire row to access all Q-values
        self._row = row

    def _calculate_kwh_typical(self, typical_value, num_units=1):
        """Helper to calculate typical kWh for an appliance."""
        return round(typical_value * num_units, 2)

    def simulate_household_appliances(self):
        """Simulate all household appliances for 24-hour period"""
        simulator = ApplianceSimulator()
        daily_energy, hourly_df = simulator.simulate_24_hours()
        peak_load = simulator.get_peak_load_analysis(hourly_df)
        efficiency = simulator.get_appliance_efficiency_ratings(daily_energy)
        
        return {
            'daily_energy': daily_energy,
            'hourly_data': hourly_df,
            'peak_load': peak_load,
            'efficiency_ratings': efficiency
        }

    def estimate_annual_electricity_consumption(self):
        """
        Estimates annual electricity consumption based on a bottom-up approach
        using appliance characteristics, estimated power consumption (Watts),
        and average daily usage hours for an Indian context.

        Returns:
            tuple:
                total_typical_kwh,
                detailed_breakdown_dict,
        """
        total_typical_kwh = 0
        breakdown = {}  # To store typical kWh for each appliance category

        # Refrigerator
        num_refrigerators = safe_numeric_conversion(self._row.get('Q9_num_refrigerators'))
        refrigerator_size = str(self._row.get('Q10_refrigerator_size')).lower()
        refrigerator_age = str(self._row.get('Q12_refrigerator_age')).lower()

        if num_refrigerators > 0:
            power_w_refrigerator = 0  # Initialize
            if 'half-size or compact' in refrigerator_size:
                power_w_refrigerator = APPLIANCE_POWER_TYPICAL['Refrigerator_Half_Compact']
            elif 'small (17.5 cubic feet or less)' in refrigerator_size:
                power_w_refrigerator = APPLIANCE_POWER_TYPICAL['Refrigerator_Small']
            elif 'medium (17.6 to 22.5 cubic feet)' in refrigerator_size:
                power_w_refrigerator = APPLIANCE_POWER_TYPICAL['Refrigerator_Medium']
            elif 'large (22.6 to 29.5 cubic feet)' in refrigerator_size:
                power_w_refrigerator = APPLIANCE_POWER_TYPICAL['Refrigerator_Large']
            elif 'very large (bigger than 29.5 cubic feet)' in refrigerator_size:
                power_w_refrigerator = APPLIANCE_POWER_TYPICAL['Refrigerator_XLarge']
            else:
                # Default if size not recognized, use medium as a fallback
                power_w_refrigerator = APPLIANCE_POWER_TYPICAL['Refrigerator_Medium']

            typical_kwh_refrigerator = power_w_refrigerator * 24 * 365 / 1000  # Base kWh

            # Adjust for age (older refrigerators are less efficient)
            age_factor = 1.0  # Default to no age adjustment
            if 'less than 2 years old' in refrigerator_age:
                age_factor = APPLIANCE_POWER_TYPICAL['Refrigerator_Age_Less_2_Factor']
            elif '2 to 4 years old' in refrigerator_age:
                age_factor = APPLIANCE_POWER_TYPICAL['Refrigerator_Age_2_4_Factor']
            elif '5 to 9 years old' in refrigerator_age:
                age_factor = APPLIANCE_POWER_TYPICAL['Refrigerator_Age_5_9_Factor']
            elif '10 to 14 years old' in refrigerator_age:
                age_factor = APPLIANCE_POWER_TYPICAL['Refrigerator_Age_10_14_Factor']
            elif '15 to 19 years old' in refrigerator_age:
                age_factor = APPLIANCE_POWER_TYPICAL['Refrigerator_Age_15_19_Factor']
            elif '20 or more years old' in refrigerator_age:
                age_factor = APPLIANCE_POWER_TYPICAL['Refrigerator_Age_20_Plus_Factor']
            # 'Don't know' or unhandled ages will use the default age_factor of 1.0

            typical_kwh_refrigerator *= age_factor

            typical_kwh_refrigerator = self._calculate_kwh_typical(typical_kwh_refrigerator, num_refrigerators)
            breakdown['Refrigerator'] = typical_kwh_refrigerator
            total_typical_kwh += typical_kwh_refrigerator

        # Air Conditioning (AC)
        has_ac = str(self._row.get('Q37_has_ac')).lower()
        uses_central_ac = str(self._row.get('Q38_uses_central_ac')).lower()
        central_ac_age = str(self._row.get('Q40_central_ac_age')).lower()

        if has_ac == 'yes' and uses_central_ac == 'yes':  # Only calculate if central AC is used
            typical_kwh_ac = (APPLIANCE_POWER_TYPICAL['AC'] * USAGE_HOURS_TYPICAL['AC_Daily_Hours'] * 365) / 1000

            # Apply AC age factor - NEW
            ac_age_factor = 1.0  # Default
            if 'less than 2 years old' in central_ac_age:
                ac_age_factor = APPLIANCE_POWER_TYPICAL['AC_Age_Less_2_Factor']
            elif '2 to 4 years old' in central_ac_age:
                ac_age_factor = APPLIANCE_POWER_TYPICAL['AC_Age_2_4_Factor']
            elif '5 to 9 years old' in central_ac_age:
                ac_age_factor = APPLIANCE_POWER_TYPICAL['AC_Age_5_9_Factor']
            elif '10 to 14 years old' in central_ac_age:
                ac_age_factor = APPLIANCE_POWER_TYPICAL['AC_Age_10_14_Factor']
            elif '15 to 19 years old' in central_ac_age:
                ac_age_factor = APPLIANCE_POWER_TYPICAL['AC_Age_15_19_Factor']
            elif '20 or more years old' in central_ac_age:
                ac_age_factor = APPLIANCE_POWER_TYPICAL['AC_Age_20_Plus_Factor']

            typical_kwh_ac *= ac_age_factor  # Apply age factor
            typical_kwh_ac = self._calculate_kwh_typical(typical_kwh_ac, 1)
            breakdown['Air Conditioning'] = typical_kwh_ac
            total_typical_kwh += typical_kwh_ac

        # Ceiling Fans
        num_ceiling_fans = safe_numeric_conversion(self._row.get('Q42_num_ceiling_fans'))
        if num_ceiling_fans > 0:
            typical_kwh_fans = (APPLIANCE_POWER_TYPICAL['Ceiling_Fan'] * USAGE_HOURS_TYPICAL[
                'Ceiling_Fan_Daily_Hours'] * 365) / 1000
            typical_kwh_fans = self._calculate_kwh_typical(typical_kwh_fans, num_ceiling_fans)
            breakdown['Ceiling Fans'] = typical_kwh_fans
            total_typical_kwh += typical_kwh_fans

        # Lighting
        num_light_bulbs_total = safe_numeric_conversion(self._row.get('Q47_num_light_bulbs_total'))
        num_light_bulbs_4hr_plus = safe_numeric_conversion(self._row.get('Q48_num_light_bulbs_4hr_plus'))
        led_present = str(self._row.get('Q49_LED__light_emitting_diode_')).lower()
        cfl_present = str(self._row.get('Q49_CFL__compact_fluorescent_lamp_')).lower()
        incandescent_present = str(self._row.get('Q49_Incandescent')).lower()

        if num_light_bulbs_total > 0:
            lighting_kwh_typical = 0

            avg_bulb_power_w_typical = APPLIANCE_POWER_TYPICAL['Lighting_CFL']  # Default to CFL
            if led_present == 'yes':
                avg_bulb_power_w_typical = APPLIANCE_POWER_TYPICAL['Lighting_LED']
            elif incandescent_present == 'yes':
                avg_bulb_power_w_typical = APPLIANCE_POWER_TYPICAL['Lighting_Incandescent']

            if num_light_bulbs_4hr_plus > 0:
                usage_4hr_plus_hours_typical = USAGE_HOURS_TYPICAL['Lighting_4hr+_Daily_Hours']
                lighting_kwh_typical += self._calculate_kwh_typical(
                    (avg_bulb_power_w_typical * usage_4hr_plus_hours_typical * 365) / 1000, num_light_bulbs_4hr_plus)

            remaining_bulbs = num_light_bulbs_total - num_light_bulbs_4hr_plus
            if remaining_bulbs > 0:
                usage_other_hours_typical = USAGE_HOURS_TYPICAL['Lighting_Other_Daily_Hours']
                lighting_kwh_typical += self._calculate_kwh_typical(
                    (avg_bulb_power_w_typical * usage_other_hours_typical * 365) / 1000, remaining_bulbs)

            breakdown['Lighting'] = round(lighting_kwh_typical, 2)
            total_typical_kwh += breakdown['Lighting']

        # Televisions
        num_televisions = safe_numeric_conversion(self._row.get('Q26_num_televisions'))
        tv_daily_hours_reported = safe_numeric_conversion(self._row.get('Q29_tv_daily_hours'))
        tv_size = str(self._row.get('Q27_tv_size')).lower()
        tv_type = str(self._row.get('Q28_tv_type')).lower()

        if num_televisions > 0 and tv_daily_hours_reported > 0:
            # Determine base power based on TV type
            power_w_type = 0  # Initialize
            if 'crt' in tv_type:
                power_w_type = APPLIANCE_POWER_TYPICAL['TV_Type_CRT']
            elif 'lcd' in tv_type:
                power_w_type = APPLIANCE_POWER_TYPICAL['TV_Type_LCD']
            elif 'led' in tv_type:
                power_w_type = APPLIANCE_POWER_TYPICAL['TV_Type_LED']
            elif 'plasma' in tv_type:
                power_w_type = APPLIANCE_POWER_TYPICAL['TV_Type_Plasma']
            elif 'oled' in tv_type:
                power_w_type = APPLIANCE_POWER_TYPICAL['TV_Type_OLED']
            else:
                # Fallback if type not recognized, use LED as a modern default
                power_w_type = APPLIANCE_POWER_TYPICAL['TV_Type_LED']

            # Adjust power based on TV size (as a multiplier or direct override if sizes are distinct enough)
            # For simplicity, let's apply a size factor to the base type wattage
            size_factor = 1.0  # Default for medium
            if 'less than 27 inches' in tv_size:
                # Assuming TV_Size_Less_27_inches is a direct wattage, let's use it if available,
                # otherwise apply a factor to the type wattage.
                # For this implementation, let's prioritize the type wattage and apply a size factor.
                # If you want to use the TV_Size_X_inches as the primary wattage, the logic needs to change.
                # For now, let's make it a factor to the type wattage for more granular control.
                size_factor = APPLIANCE_POWER_TYPICAL['TV_Size_Less_27_inches'] / APPLIANCE_POWER_TYPICAL[
                    'TV_Size_27_39_inches']  # Factor relative to medium
            elif '40 to 59 inches' in tv_size:
                size_factor = APPLIANCE_POWER_TYPICAL['TV_Size_40_59_inches'] / APPLIANCE_POWER_TYPICAL[
                    'TV_Size_27_39_inches']
            elif '60 inches or larger' in tv_size:
                size_factor = APPLIANCE_POWER_TYPICAL['TV_Size_60_or_larger_inches'] / APPLIANCE_POWER_TYPICAL[
                    'TV_Size_27_39_inches']

            # Combine type and size influence
            power_w_final = power_w_type * size_factor

            usage_factor_typical = USAGE_HOURS_TYPICAL['TV_Daily_Hours_Factor']
            tv_usage_hours_typical = tv_daily_hours_reported * usage_factor_typical

            typical_kwh_tv = (power_w_final * tv_usage_hours_typical * 365) / 1000
            typical_kwh_tv = self._calculate_kwh_typical(typical_kwh_tv, num_televisions)
            breakdown['Televisions'] = typical_kwh_tv
            total_typical_kwh += typical_kwh_tv

        # Water Heater (Electric Geyser)
        has_water_heater = str(self._row.get('Q43_has_water_heater')).lower()
        water_heater_fuel = str(self._row.get('Q46_water_heater_fuel')).lower()
        if has_water_heater == 'yes' and water_heater_fuel == 'electricity':
            typical_kwh_geyser = (APPLIANCE_POWER_TYPICAL['Water_Heater_Electric'] * USAGE_HOURS_TYPICAL[
                'Water_Heater_Daily_Hours'] * 365) / 1000
            typical_kwh_geyser = self._calculate_kwh_typical(typical_kwh_geyser, 1)
            breakdown['Water Heater (Electric)'] = typical_kwh_geyser
            total_typical_kwh += typical_kwh_geyser

        # Clothes Washer (Electric)
        has_clothes_washer = str(self._row.get('Q19_has_clothes_washer')).lower()
        clothes_washer_usage = safe_numeric_conversion(self._row.get('Q20_clothes_washer_usage'))  # Times per week
        if has_clothes_washer == 'yes' and clothes_washer_usage > 0:
            washer_power_w_typical = APPLIANCE_POWER_TYPICAL['Clothes_Washer']
            washer_cycle_hours = 1  # Fixed 1 hour per cycle

            usage_factor_typical = USAGE_HOURS_TYPICAL['Clothes_Washer_Weekly_Use_Factor']
            washer_usage_per_week_typical = clothes_washer_usage * usage_factor_typical

            typical_kwh_washer = (
                                             washer_power_w_typical * washer_cycle_hours * washer_usage_per_week_typical * 52) / 1000
            typical_kwh_washer = self._calculate_kwh_typical(typical_kwh_washer, 1)
            breakdown['Clothes Washer'] = typical_kwh_washer
            total_typical_kwh += typical_kwh_washer

        # Clothes Dryer (Electric)
        has_clothes_dryer = str(self._row.get('Q22_has_clothes_dryer')).lower()
        dryer_fuel = str(self._row.get('Q24_clothes_dryer_fuel')).lower()
        if has_clothes_dryer == 'yes' and dryer_fuel == 'electricity':
            typical_kwh_dryer = (APPLIANCE_POWER_TYPICAL['Clothes_Dryer_Electric'] * USAGE_HOURS_TYPICAL[
                'Clothes_Dryer_Weekly_Hours'] * 52) / 1000
            typical_kwh_dryer = self._calculate_kwh_typical(typical_kwh_dryer, 1)
            breakdown['Clothes Dryer (Electric)'] = typical_kwh_dryer
            total_typical_kwh += typical_kwh_dryer

        # Computers & Connectivity
        num_desktop_computers = safe_numeric_conversion(self._row.get('Q30_num_desktop_computers'))
        num_laptop_computers = safe_numeric_conversion(self._row.get('Q30_num_laptop_computers'))
        has_wireless_router = str(self._row.get('Q32_has_wireless_router')).lower()

        computer_kwh_typical = 0
        if num_desktop_computers > 0:
            computer_kwh_typical += self._calculate_kwh_typical(
                (APPLIANCE_POWER_TYPICAL['Desktop_Computer'] * USAGE_HOURS_TYPICAL['Desktop_Daily_Hours'] * 365) / 1000,
                num_desktop_computers)

        if num_laptop_computers > 0:
            computer_kwh_typical += self._calculate_kwh_typical(
                (APPLIANCE_POWER_TYPICAL['Laptop_Computer'] * USAGE_HOURS_TYPICAL['Laptop_Daily_Hours'] * 365) / 1000,
                num_laptop_computers)

        if has_wireless_router == 'yes':
            computer_kwh_typical += self._calculate_kwh_typical(
                (APPLIANCE_POWER_TYPICAL['Wireless_Router'] * 24 * 365) / 1000, 1)

        if computer_kwh_typical > 0:  # Only add if there's actual consumption
            breakdown['Computers & Connectivity'] = round(computer_kwh_typical, 2)
            total_typical_kwh += breakdown['Computers & Connectivity']

        # Small Kitchen Appliances
        small_appliance_kwh_typical = 0
        daily_hours_factor_typical = USAGE_HOURS_TYPICAL['Small_Appliance_Daily_Hours_Factor']

        toaster_present = str(self._row.get('Q18_Toaster')).lower()
        coffee_maker_present = str(self._row.get('Q18_Coffee_maker')).lower()
        blender_present = str(self._row.get('Q18_Blender_or_juicer')).lower()
        rice_cooker_present = str(self._row.get('Q18_Rice_cooker')).lower()

        if toaster_present == 'yes':
            small_appliance_kwh_typical += self._calculate_kwh_typical(
                (APPLIANCE_POWER_TYPICAL['Small_Appliance_Toaster'] * 0.1 * daily_hours_factor_typical * 365) / 1000, 1)

        if coffee_maker_present == 'yes':
            typical_kwh_coffee = 60  # From example: 60 kWh
            typical_kwh_coffee = self._calculate_kwh_typical(typical_kwh_coffee, 1)
            breakdown['Coffee maker'] = typical_kwh_coffee  # Separate entry
            total_typical_kwh += typical_kwh_coffee

        if blender_present == 'yes':
            small_appliance_kwh_typical += self._calculate_kwh_typical(
                (APPLIANCE_POWER_TYPICAL['Small_Appliance_Blender'] * 0.05 * daily_hours_factor_typical * 365) / 1000,
                1)
        if rice_cooker_present == 'yes':
            small_appliance_kwh_typical += self._calculate_kwh_typical((APPLIANCE_POWER_TYPICAL[
                                                                            'Small_Appliance_Rice_Cooker'] * 0.5 * daily_hours_factor_typical * 365) / 1000,
                                                                       1)

        if small_appliance_kwh_typical > 0:
            breakdown['Other Small Kitchen Appliances'] = round(small_appliance_kwh_typical, 2)
            total_typical_kwh += breakdown['Other Small Kitchen Appliances']

        # Other Use (formerly Miscellaneous)
        num_adults = safe_numeric_conversion(self._row.get('Q2_num_adults'))
        other_use_kwh_typical = USAGE_HOURS_TYPICAL['Other_Use_Default_KWH']  # Default if no adults
        if num_adults > 0:
            other_use_kwh_typical = USAGE_HOURS_TYPICAL['Other_Use_Per_Adult_KWH'] * num_adults

        other_use_kwh_typical = self._calculate_kwh_typical(other_use_kwh_typical, 1)

        breakdown['Other Use'] = other_use_kwh_typical
        total_typical_kwh += other_use_kwh_typical

        return round(total_typical_kwh, 2), breakdown

    def calculate_btu_equivalents(self):
        """
        Calculates annual energy consumption in BTUs for various fuel types
        based on available data and typical Indian contexts.

        Returns:
            dict: A dictionary of annual energy consumption in BTUs for each fuel type as typical values.
        """
        btu_equivalents = {}

        # --- Conversion Factors (Approximate for Indian context) ---
        KWH_TO_BTU = 3412.14  # Fixed definition

        # 2. Natural Gas
        natural_gas_responsible = str(self._row.get('Q51_natural_gas_payment_responsibility')).lower()
        if natural_gas_responsible == 'household is responsible for paying for all natural gas used in this home':
            typical_annual_gas_scm = FUEL_BTU_TYPICAL['NATURAL_GAS_TYPICAL_ANNUAL_SCM']
            ng_btu_conversion_typical = FUEL_BTU_TYPICAL['NATURAL_GAS_SCM_TO_BTU']
            typical_btu = typical_annual_gas_scm * ng_btu_conversion_typical
            btu_equivalents['Natural Gas'] = round(typical_btu, 2)
        else:
            btu_equivalents['Natural Gas'] = 0

        # 3. Fuel Oil
        receives_fuel_oil = str(self._row.get('Q56_receives_fuel_oil_deliveries')).lower()
        num_deliveries = safe_numeric_conversion(self._row.get('Q57_fuel_oil_num_deliveries_past_year'))
        fuel_oil_tank_size_liters = safe_numeric_conversion(self._row.get('Q57_fuel_oil_tank_size'))

        if receives_fuel_oil == 'yes' and pd.notna(num_deliveries) and num_deliveries > 0 and \
                pd.notna(fuel_oil_tank_size_liters) and fuel_oil_tank_size_liters > 0:

            fuel_oil_btu_conversion_typical = FUEL_BTU_TYPICAL['FUEL_OIL_LITRE_TO_BTU']
            total_litres_typical = fuel_oil_tank_size_liters * num_deliveries
            typical_btu = total_litres_typical * fuel_oil_btu_conversion_typical
            btu_equivalents['Fuel Oil'] = round(typical_btu, 2)
        else:
            btu_equivalents['Fuel Oil'] = 0

        # 4. LPG/Propane
        num_lpg_cylinders = safe_numeric_conversion(self._row.get('Q60_num_lpg_propane_cylinders_year'))
        if num_lpg_cylinders > 0:
            lpg_kg_to_btu_typical = FUEL_BTU_TYPICAL['LPG_KG_TO_BTU']
            LPG_CYLINDER_KG = 14.2  # Standard LPG cylinder size in India (kg)
            typical_btu = num_lpg_cylinders * LPG_CYLINDER_KG * lpg_kg_to_btu_typical
            btu_equivalents['LPG/Propane'] = round(typical_btu, 2)
        else:
            btu_equivalents['LPG/Propane'] = 0

        # 5. Wood
        uses_wood = str(self._row.get('Q58_uses_wood_for_fuel')).lower()
        wood_amount = safe_numeric_conversion(
            self._row.get('Q59_wood_pellets_total_amount_past_year'))  # Assuming this is in kg

        if uses_wood == 'yes':
            wood_kg_to_btu_typical = FUEL_BTU_TYPICAL['WOOD_KG_TO_BTU']
            current_wood_kg = wood_amount
            if not pd.notna(current_wood_kg) or current_wood_kg <= 0:
                current_wood_kg = FUEL_BTU_TYPICAL['WOOD_TYPICAL_ANNUAL_KG']  # Use typical default if not provided

            typical_btu = current_wood_kg * wood_kg_to_btu_typical
            btu_equivalents['Wood'] = round(typical_btu, 2)
        else:
            btu_equivalents['Wood'] = 0

        return btu_equivalents


class DetailedHouseholdAnalysis:
    """Provides comprehensive household energy analysis with recommendations"""
    
    def __init__(self, energy_costs_instance, electricity_breakdown_kwh, fuel_btu_equivalents):
        self.energy_costs = energy_costs_instance
        self.electricity_kwh = electricity_breakdown_kwh
        self.fuel_btu = fuel_btu_equivalents
        self.KWH_TO_BTU = 3412.14
        self.electricity_rate = 0.12  # Average $/kWh (can be parametrized)
        self.natural_gas_rate = 10.5  # $/1000 BTU (can be parametrized)

    def calculate_annual_cost_breakdown(self):
        """Calculate detailed annual costs by appliance category"""
        cost_breakdown = {}
        
        # Electricity costs
        for appliance, kwh in self.electricity_kwh.items():
            cost_breakdown[f"{appliance} (Electricity)"] = round(kwh * self.electricity_rate, 2)
        
        # Natural gas costs
        if self.fuel_btu.get('Natural Gas', 0) > 0:
            ng_cost = (self.fuel_btu['Natural Gas'] / 1000) * self.natural_gas_rate
            cost_breakdown['Natural Gas'] = round(ng_cost, 2)
        
        # Other fuel costs
        for fuel, btu in self.fuel_btu.items():
            if fuel not in ['Natural Gas', 'Electricity']:
                # Estimate cost (varies by location)
                fuel_cost = (btu / 1000) * 8  # Approximate rate
                cost_breakdown[fuel] = round(fuel_cost, 2)
        
        return cost_breakdown

    def get_major_energy_consumers(self, top_n=5):
        """Identify top N energy consuming appliances"""
        sorted_appliances = sorted(self.electricity_kwh.items(), key=lambda x: x[1], reverse=True)
        return sorted_appliances[:top_n]

    def generate_efficiency_recommendations(self):
        """Generate personalized energy efficiency recommendations"""
        recommendations = []
        
        major_consumers = self.get_major_energy_consumers()
        
        for appliance, kwh in major_consumers:
            if 'AC' in appliance and kwh > 3000:
                recommendations.append({
                    'appliance': appliance,
                    'current_kwh': kwh,
                    'recommendation': 'Consider upgrading to a high-efficiency AC unit (SEER 13+)',
                    'estimated_savings_kwh': kwh * 0.25
                })
            elif 'Refrigerator' in appliance and kwh > 1000:
                recommendations.append({
                    'appliance': appliance,
                    'current_kwh': kwh,
                    'recommendation': 'Refrigerator is older; consider ENERGY STAR model',
                    'estimated_savings_kwh': kwh * 0.30
                })
            elif 'Water Heater' in appliance and kwh > 2000:
                recommendations.append({
                    'appliance': appliance,
                    'current_kwh': kwh,
                    'recommendation': 'Use solar water heater or high-efficiency electric heater',
                    'estimated_savings_kwh': kwh * 0.40
                })
            elif 'Lighting' in appliance and kwh > 500:
                recommendations.append({
                    'appliance': appliance,
                    'current_kwh': kwh,
                    'recommendation': 'Replace all bulbs with LED (9W instead of 60W)',
                    'estimated_savings_kwh': kwh * 0.75
                })
        
        return recommendations

    def calculate_carbon_footprint(self):
        """Calculate household carbon footprint from energy consumption"""
        # CO2 factors (kg CO2 per unit)
        co2_factor_kwh = 0.45  # kg CO2 per kWh (varies by region)
        co2_factor_btu = 0.000053  # kg CO2 per BTU
        
        total_electricity_kwh = sum(self.electricity_kwh.values())
        electricity_co2 = total_electricity_kwh * co2_factor_kwh
        
        total_fuel_btu = sum(self.fuel_btu.values())
        fuel_co2 = total_fuel_btu * co2_factor_btu
        
        total_co2 = electricity_co2 + fuel_co2
        
        return {
            'electricity_co2_kg': round(electricity_co2, 2),
            'fuel_co2_kg': round(fuel_co2, 2),
            'total_co2_kg': round(total_co2, 2),
            'total_co2_metric_tons': round(total_co2 / 1000, 3)
        }

    def get_load_profile_analysis(self):
        """Analyze household load profile patterns"""
        simulator = ApplianceSimulator()
        daily_energy, hourly_df = simulator.simulate_24_hours()
        
        hourly_profile = hourly_df.groupby('hour')[['total_power_w']].mean()
        hourly_profile['peak_w'] = hourly_df.groupby('hour')['total_power_w'].max()
        hourly_profile['min_w'] = hourly_df.groupby('hour')['total_power_w'].min()
        
        return hourly_profile


# --- Class for Plotting Energy Use (Parent Class for EnhancedPlotting) ---
class PlotElectricityUse:
    def plot_combined_energy_breakdowns(self, electricity_breakdown_data, total_energy_breakdown_data):
        """
        Plots both electricity consumption and total energy consumption breakdowns
        on a single figure with two subplots. Each subplot will have distinct colors,
        only percentages inside slices, and a legend outside.

        Args:
            electricity_breakdown_data (dict): A dictionary where keys are category names
                                               and values are their estimated annual electricity consumption (typical values).
            total_energy_breakdown_data (dict): A dictionary where keys are category names
                                                and values are their estimated annual total energy consumption (typical values).
        """
        fig, axes = plt.subplots(1, 2, figsize=(20, 10))

        colors = plt.colormaps.get_cmap('tab20')

        def autopct_format(pct):
            return ('%.1f%%' % pct) if pct > 0 else ''

        filtered_electricity_data = {k: v for k, v in electricity_breakdown_data.items() if pd.notna(v) and v > 0}

        if not filtered_electricity_data:
            axes[0].text(0.5, 0.5, "No valid electricity consumption data to plot.", horizontalalignment='center',
                         verticalalignment='center', transform=axes[0].transAxes, fontsize=12)
            axes[0].set_xticks([])
            axes[0].set_yticks([])
        else:
            labels_elec = list(filtered_electricity_data.keys())
            sizes_elec = list(filtered_electricity_data.values())
            pie_colors_elec = [colors(i % colors.N) for i in range(len(labels_elec))]

            wedges_elec, _, autotexts_elec = axes[0].pie(
                sizes_elec,
                autopct=autopct_format,
                startangle=90,
                pctdistance=0.85,
                colors=pie_colors_elec,
                wedgeprops=dict(width=0.3),
                textprops={'fontsize': 9, 'color': 'white'}
            )
            axes[0].axis('equal')
            axes[0].set_title('Annual Electricity Consumption Breakdown (kWh)', fontsize=14)
            axes[0].legend(wedges_elec, labels_elec, title="Electricity Categories",
                           loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        filtered_total_energy_data = {k: v for k, v in total_energy_breakdown_data.items() if pd.notna(v) and v > 0}

        if not filtered_total_energy_data:
            axes[1].text(0.5, 0.5, "No valid total energy consumption data to plot.", horizontalalignment='center',
                         verticalalignment='center', transform=axes[1].transAxes, fontsize=12)
            axes[1].set_xticks([])
            axes[1].set_yticks([])
        else:
            labels_total = list(filtered_total_energy_data.keys())
            sizes_total = list(filtered_total_energy_data.values())
            pie_colors_total = [colors(i % colors.N) for i in range(len(labels_total))]

            wedges_total, _, autotexts_total = axes[1].pie(
                sizes_total,
                autopct=autopct_format,
                startangle=90,
                pctdistance=0.85,
                colors=pie_colors_total,
                wedgeprops=dict(width=0.3),
                textprops={'fontsize': 9, 'color': 'white'}
            )
            axes[1].axis('equal')
            axes[1].set_title('Annual Total Energy Consumption Breakdown (BTU)', fontsize=14)
            axes[1].legend(wedges_total, labels_total, title="Total Energy Categories",
                           loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

        plt.tight_layout(rect=[0, 0, 0.9, 1])
        plt.show()

    def plot_energy_by_year_built(self, aggregated_data):
        """
        Plots Average BTU and Average Sq Ft by Year Range.

        Args:
            aggregated_data (pd.DataFrame): DataFrame with 'Year Range', 'Average BTU', and 'Average Sq Ft' columns.
        """
        if aggregated_data.empty:
            print("No data available to plot energy consumption by year built/moved-in.")
            return

        year_order = [
            'Before 1950', '1950-1959', '1960-1969', '1970-1979', '1980-1989',
            '1990-1999', '2000-2009', '2010-2019', '2020 or later'
        ]
        aggregated_data['Year Range'] = pd.Categorical(aggregated_data['Year Range'], categories=year_order, ordered=True)
        aggregated_data = aggregated_data.sort_values('Year Range')

        fig, ax1 = plt.subplots(figsize=(12, 7))

        color_sqft = 'tab:blue'
        ax1.set_xlabel('Year Built/Moved-in Range', fontsize=12)
        ax1.set_ylabel('Average Square Feet', color=color_sqft, fontsize=12)
        ax1.bar(aggregated_data['Year Range'], aggregated_data['Average Sq Ft'], color=color_sqft, alpha=0.6, width=0.7)
        ax1.tick_params(axis='y', labelcolor=color_sqft)
        ax1.set_ylim(bottom=0)

        ax2 = ax1.twinx()
        color_btu = 'tab:red'
        ax2.set_ylabel('Average Total BTU (Millions)', color=color_btu, fontsize=12)
        ax2.plot(aggregated_data['Year Range'], aggregated_data['Average BTU'], color=color_btu, marker='o', linestyle='-', linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color_btu)
        ax2.set_ylim(bottom=0)

        plt.title('Average Energy Consumption and Square Footage by Year Built/Moved-in', fontsize=16)
        fig.tight_layout()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        plt.show()


class EnhancedPlotting(PlotElectricityUse):
    """Enhanced plotting with additional visualization capabilities"""
    
    def plot_hourly_load_profile(self, hourly_profile):
        """Plot hourly load profile throughout the day"""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        hours = hourly_profile.index
        
        ax.fill_between(hours, hourly_profile['min_w'], hourly_profile['peak_w'], 
                        alpha=0.2, label='Peak-to-Min Range')
        ax.plot(hours, hourly_profile['total_power_w'], marker='o', linewidth=2, 
               label='Average Load', color='blue')
        ax.plot(hours, hourly_profile['peak_w'], linestyle='--', 
               label='Peak Load', color='red')
        ax.plot(hours, hourly_profile['min_w'], linestyle='--', 
               label='Minimum Load', color='green')
        
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Power (Watts)', fontsize=12)
        ax.set_title('Household Hourly Load Profile (24-Hour Simulation)', fontsize=14)
        ax.set_xticks(range(0, 24, 2))
        ax.legend()
        ax.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.show()


class Metadata:
    def __init__(self, row):
        self._id = row.get('__v')

# --- Main function to process and print data ---

def print_personal_appliance_data(file_path):
    """
    Loads a CSV file, processes electricity and fuel consumption for each person,
    and then prints only the relevant energy use details (typical values).
    Applies proportional scaling to estimated electricity consumption to match
    reported total electricity.
    Finally, generates combined plots for electricity consumption (kWh)
    and total energy consumption (BTU by all categories) across all users,
    using typical values for plotting.

    Args:
        file_path (str): The path to the CSV file.
    """
    try:
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)

        print("Successfully loaded the CSV file.")
        print("\n--- DataFrame Overview ---")
        print(f"Total rows: {len(df)}")
        print(f"Total columns: {len(df.columns)}")

        # Map category names to their respective classes
        category_classes = {
            'Household Information': HouseholdInformation,
            'Home Characteristics': HomeCharacteristics,
            'Refrigerator': Refrigerator,
            'Stove': Stove,
            'Wall Oven': WallOven,
            'Small Kitchen Appliances (Q18)': SmallKitchenAppliances,
            'Clothes Washer': ClothesWasher,
            'Clothes Dryer': ClothesDryer,
            'Televisions': Televisions,
            'Computers & Connectivity': ComputersConnectivity,
            'Heating Equipment': HeatingEquipment,
            'Cooling Equipment': CoolingEquipment,
            'Water Heater': WaterHeater,
            'Lighting': Lighting,
            'Energy Consumption & Costs': EnergyConsumptionCosts,
            'Metadata': Metadata
        }

        # Create an instance of the plotting class
        plotter = PlotElectricityUse()
        enhanced_plotter = EnhancedPlotting()

        # Dictionary to accumulate total electricity consumption (kWh) for each appliance category across all users
        # Stores typical values
        all_users_combined_electricity_kwh_breakdown = {}
        # Dictionary to accumulate total energy consumption (BTU) for all categories (appliances + fuels) across all users
        # Stores typical values
        all_users_combined_total_btu_breakdown = {}

        # List to accumulate data for the year built/moved-in plot
        year_data_for_plot = []

        # Define BTU conversion factor for kWh (fixed)
        KWH_TO_BTU = 3412.14

        # Iterate through each row (person) in the DataFrame
        for index, row_data in df.iterrows():
            person_name = row_data.get('Q0_name', 'N/A')  # Get the name
            print(f"\n{'=' * 50}")
            print(f"Energy Consumption Data for Person: {person_name} (Row {index + 1})")
            print(f"{'=' * 50}")

            # Process Energy Consumption & Costs category
            energy_costs_instance = EnergyConsumptionCosts(row_data)
            home_char_instance = HomeCharacteristics(row_data) # Also need home characteristics for year built/sq ft

            try:
                # --- Initial Electricity Consumption Estimates (kWh) ---
                total_uncalibrated_typical_kwh_all_appliances, \
                    electricity_appliance_breakdown_uncalibrated_kwh = \
                    energy_costs_instance.estimate_annual_electricity_consumption()

                # --- Proportional Scaling for Electricity Consumption ---
                electricity_appliance_breakdown_calibrated_kwh = electricity_appliance_breakdown_uncalibrated_kwh.copy()

                reported_annual_kwh = safe_numeric_conversion(energy_costs_instance.last_electricity_consumption)
                if pd.notna(reported_annual_kwh) and reported_annual_kwh > 0:
                    # Corrected: Multiply by 6 for a 2-month bill to get annual
                    reported_annual_kwh *= 6  # Convert last bill (2-month) to annual

                    print(f"\n--- Applying Proportional Scaling for Electricity ---")
                    print(f"  Reported Annual Electricity (from bill): {round(reported_annual_kwh, 2)} kWh")
                    print(
                        f"  Total Estimated Uncalibrated Electricity (All Appliances): {round(total_uncalibrated_typical_kwh_all_appliances, 2)} kWh")

                    if total_uncalibrated_typical_kwh_all_appliances > 0:
                        scaling_factor = reported_annual_kwh / total_uncalibrated_typical_kwh_all_appliances
                        print(f"  Calculated Scaling Factor: {round(scaling_factor, 4)}")

                        for appliance_name, typical_kwh_uncalibrated in electricity_appliance_breakdown_uncalibrated_kwh.items():
                            calibrated_typical_kwh = typical_kwh_uncalibrated * scaling_factor
                            # Ensure non-negative consumption
                            calibrated_typical_kwh = max(0, calibrated_typical_kwh)
                            electricity_appliance_breakdown_calibrated_kwh[appliance_name] = round(
                                calibrated_typical_kwh, 2)
                            print(f"    {appliance_name} Calibrated: {round(calibrated_typical_kwh, 2)} kWh/year")
                    else:
                        print("  Total uncalibrated electricity is zero. Cannot apply scaling.")
                        # If uncalibrated is zero, calibrated also remains zero
                        electricity_appliance_breakdown_calibrated_kwh = {k: 0 for k in
                                                                          electricity_appliance_breakdown_calibrated_kwh}
                else:
                    print(
                        "\n--- Proportional Scaling Skipped: No valid reported electricity consumption for scaling. ---")
                    # If no reported bill, use uncalibrated values as is
                    electricity_appliance_breakdown_calibrated_kwh = electricity_appliance_breakdown_uncalibrated_kwh.copy()

                # --- Recalculate Overall Total kWh after Scaling ---
                # Removed the extra rounding here to match the sum of individually rounded values
                total_typical_kwh_calibrated = sum(electricity_appliance_breakdown_calibrated_kwh.values())

                # --- Print Calibrated Electricity Consumption Details (kWh) ---
                print(f"\n--- Calibrated Annual Electricity Consumption (kWh) ---")
                for appliance, kwh_typical in electricity_appliance_breakdown_calibrated_kwh.items():
                    print(f"    {appliance}: {kwh_typical} kWh/year")
                    # Accumulate for the combined kWh plot (using calibrated values)
                    all_users_combined_electricity_kwh_breakdown[appliance] = \
                        all_users_combined_electricity_kwh_breakdown.get(appliance, 0) + kwh_typical

                    # Accumulate for the combined total BTU plot (electricity appliances)
                    all_users_combined_total_btu_breakdown[appliance] = \
                        all_users_combined_total_btu_breakdown.get(appliance, 0) + (kwh_typical * KWH_TO_BTU)

                print(
                    f"\n  Total Calibrated Annual Electricity Consumption: {round(total_typical_kwh_calibrated, 2)} kWh/year")

                # Re-print reported if available
                if pd.notna(reported_annual_kwh) and reported_annual_kwh > 0:
                    print(
                        f"  Reported Annual Electricity Consumption (from bill): {round(reported_annual_kwh, 2)} kWh/year")
                    print(
                        f"  Difference (Calibrated Typical - Reported): {round(total_typical_kwh_calibrated - reported_annual_kwh, 2)} kWh/year")

                # --- BTU Equivalents for Other Fuels (MOVED BEFORE DETAILED ANALYSIS) ---
                print(f"\n--- Estimated Annual Energy Consumption (BTU Equivalents by Fuel Type) ---")
                fuel_btu_equivalents = energy_costs_instance.calculate_btu_equivalents()

                total_fuel_btu = 0
                for fuel_type, btu_typical in fuel_btu_equivalents.items():
                    if fuel_type != 'Electricity (Total)':
                        print(f"    {fuel_type}: {btu_typical} BTU/year")
                        all_users_combined_total_btu_breakdown[fuel_type] = \
                            all_users_combined_total_btu_breakdown.get(fuel_type, 0) + btu_typical
                        total_fuel_btu += btu_typical

                # --- DETAILED HOUSEHOLD ANALYSIS ---
                print(f"\n--- Detailed Household Energy Analysis ---")
                detailed_analysis = DetailedHouseholdAnalysis(
                    energy_costs_instance,
                    electricity_appliance_breakdown_calibrated_kwh,
                    fuel_btu_equivalents
                )

                # Cost breakdown
                print(f"\n--- Annual Cost Breakdown by Appliance ---")
                cost_breakdown = detailed_analysis.calculate_annual_cost_breakdown()
                for appliance, cost in sorted(cost_breakdown.items(), key=lambda x: x[1], reverse=True):
                    print(f"    {appliance}: ${cost:.2f}")
                total_annual_cost = sum(cost_breakdown.values())
                print(f"  Total Estimated Annual Cost: ${total_annual_cost:.2f}")

                # Major energy consumers
                print(f"\n--- Top 5 Energy Consumers ---")
                major_consumers = detailed_analysis.get_major_energy_consumers(5)
                for i, (appliance, kwh) in enumerate(major_consumers, 1):
                    percentage = (kwh / total_typical_kwh_calibrated * 100) if total_typical_kwh_calibrated > 0 else 0
                    print(f"    {i}. {appliance}: {kwh} kWh/year ({percentage:.1f}%)")

                # Efficiency recommendations
                print(f"\n--- Energy Efficiency Recommendations ---")
                recommendations = detailed_analysis.generate_efficiency_recommendations()
                if recommendations:
                    for i, rec in enumerate(recommendations, 1):
                        print(f"    {i}. {rec['appliance']}")
                        print(f"       Current: {rec['current_kwh']} kWh/year")
                        print(f"       Recommendation: {rec['recommendation']}")
                        print(f"       Potential Savings: {rec['estimated_savings_kwh']:.0f} kWh/year (${rec['estimated_savings_kwh'] * 0.12:.2f})")
                else:
                    print("    No major inefficiencies detected.")

                # Carbon footprint
                print(f"\n--- Carbon Footprint Analysis ---")
                carbon_data = detailed_analysis.calculate_carbon_footprint()
                print(f"    Electricity CO2: {carbon_data['electricity_co2_kg']} kg")
                print(f"    Fuel CO2: {carbon_data['fuel_co2_kg']} kg")
                print(f"    Total CO2: {carbon_data['total_co2_kg']} kg ({carbon_data['total_co2_metric_tons']} metric tons/year)")
                equivalent_trees = carbon_data['total_co2_kg'] / 20  # 1 tree absorbs ~20 kg CO2/year
                print(f"    Equivalent to: {equivalent_trees:.1f} trees needed to offset")

                # --- Appliance-Level Detailed Simulation ---
                print(f"\n--- Detailed Appliance Simulation (24-Hour Profile) ---")
                try:
                    simulator_results = energy_costs_instance.simulate_household_appliances()
                    daily_energy = simulator_results['daily_energy']
                    peak_load = simulator_results['peak_load']
                    efficiency_ratings = simulator_results['efficiency_ratings']
                    
                    print(f"    Daily Energy Consumption by Appliance:")
                    for appliance, energy_wh in sorted(daily_energy.items(), key=lambda x: x[1], reverse=True):
                        energy_kwh = energy_wh / 1000
                        print(f"      {appliance}: {energy_kwh:.2f} kWh/day ({energy_kwh*365:.1f} kWh/year)")
                    
                    print(f"\n    Peak Load Analysis:")
                    print(f"      Average Peak Hour: {peak_load['max'].mean():.0f}W")
                    print(f"      Average Hourly Load: {peak_load['mean'].mean():.0f}W")
                    print(f"      Minimum Hourly Load: {peak_load['min'].mean():.0f}W")
                    print(f"      Peak-to-minimum ratio: {peak_load['max'].mean() / peak_load['min'].mean():.2f}x")
                    
                    print(f"\n    Appliance Efficiency Ratings (Higher is better):")
                    for appliance, rating in sorted(efficiency_ratings.items(), key=lambda x: x[1], reverse=True)[:5]:
                        print(f"      {appliance}: {rating:.1f}%")
                except Exception as sim_error:
                    print(f"    Note: Appliance simulation unavailable ({str(sim_error)[:50]}...)")

                # --- Data for Year Built/Moved-in Plot ---
                # Determine the relevant year based on ownership
                relevant_year_str = None
                if home_char_instance.ownership and isinstance(home_char_instance.ownership, str):
                    if 'own' in home_char_instance.ownership.lower():
                        relevant_year_str = home_char_instance.year_built
                    elif 'rent' in home_char_instance.ownership.lower() or 'lease' in home_char_instance.ownership.lower():
                        relevant_year_str = home_char_instance.move_in_year

                # Handle "2020 or later" and other non-standard year strings
                if relevant_year_str:
                    if '2020 or later' in str(relevant_year_str).lower():
                        year_range = '2020 or later'
                    elif 'before' in str(relevant_year_str).lower():
                        year_range = 'Before 1950'  # Standardize "Before X" to "Before 1950" if needed
                    elif '-' in str(relevant_year_str):
                        year_range = str(relevant_year_str)  # Keep ranges like "1950-1959" as is
                    else:
                        # Attempt to convert to int and then to a range
                        try:
                            year = int(relevant_year_str)
                            if year < 1950:
                                year_range = 'Before 1950'
                            elif 1950 <= year <= 1959:
                                year_range = '1950-1959'
                            elif 1960 <= year <= 1969:
                                year_range = '1960-1969'
                            elif 1970 <= year <= 1979:
                                year_range = '1970-1979'
                            elif 1980 <= year <= 1989:
                                year_range = '1980-1989'
                            elif 1990 <= year <= 1999:
                                year_range = '1990-1999'
                            elif 2000 <= year <= 2009:
                                year_range = '2000-2009'
                            elif 2010 <= year <= 2019:
                                year_range = '2010-2019'
                            else:  # 2020 and beyond
                                year_range = '2020 or later'
                        except ValueError:
                            year_range = None  # Cannot parse year
                else:
                    year_range = None

                sq_ft_home = safe_numeric_conversion(home_char_instance.sq_ft_home)

                # Convert calibrated kWh to BTU for total energy calculation
                electricity_btu = total_typical_kwh_calibrated * KWH_TO_BTU
                total_household_btu = electricity_btu + total_fuel_btu

                if year_range and pd.notna(total_household_btu) and pd.notna(sq_ft_home) and sq_ft_home > 0:
                    year_data_for_plot.append({
                        'Year Range': year_range,
                        'Total BTU': total_household_btu,
                        'Sq Ft': sq_ft_home
                    })


            except Exception as e:
                print(f"  An error occurred processing energy consumption for {person_name}: {e}")
                import traceback
                traceback.print_exc()  # Print full traceback for debugging

        # --- Plotting the combined electricity consumption breakdown (kWh) and total energy consumption (BTU) for all users ---
        print(f"\n\n{'=' * 50}")
        print("Generating Combined Energy Consumption Plots for All Users")
        print(f"{'=' * 50}")
        plotter.plot_combined_energy_breakdowns(
            all_users_combined_electricity_kwh_breakdown,
            all_users_combined_total_btu_breakdown
        )

        # --- Generate Enhanced Analysis Plots ---
        print(f"\n\n{'=' * 50}")
        print("Generating Advanced Energy Analysis Visualizations")
        print(f"{'=' * 50}")
        
        # Get sample household for detailed analysis (first valid record)
        for index, row_data in df.iterrows():
            try:
                energy_costs_instance = EnergyConsumptionCosts(row_data)
                total_kwh, breakdown = energy_costs_instance.estimate_annual_electricity_consumption()
                fuel_btu = energy_costs_instance.calculate_btu_equivalents()
                
                detailed_analysis = DetailedHouseholdAnalysis(energy_costs_instance, breakdown, fuel_btu)
                
                # Get hourly simulation data
                simulator_results = energy_costs_instance.simulate_household_appliances()
                hourly_df = simulator_results['hourly_data']
                
                # Plot hourly load profile
                print("Generating hourly load profile chart...")
                load_profile = detailed_analysis.get_load_profile_analysis()
                enhanced_plotter.plot_hourly_load_profile(load_profile)
                
                break  # Only for first valid record
            except:
                continue

        # --- Process and Plot Data for 'Energy by Year Built/Moved-in' ---
        print(f"\n\n{'=' * 50}")
        print("Generating Energy Consumption by Year Built/Moved-in Plot")
        print(f"{'=' * 50}")

        # Convert the list of dicts to a DataFrame for easier aggregation
        year_built_moved_in_df = pd.DataFrame(year_data_for_plot)

        if not year_built_moved_in_df.empty:
            # Group by 'Year Range' and calculate averages
            aggregated_year_data = year_built_moved_in_df.groupby('Year Range').agg(
                Average_BTU=('Total BTU', 'mean'),
                Average_Sq_Ft=('Sq Ft', 'mean')
            ).reset_index()

            # Convert BTU to million BTU for plotting as per the image
            aggregated_year_data['Average_BTU'] = aggregated_year_data['Average_BTU'] / 1_000_000

            # Rename columns for clarity in the plotting function
            aggregated_year_data.rename(columns={
                'Average_BTU': 'Average BTU',
                'Average_Sq_Ft': 'Average Sq Ft'
            }, inplace=True)

            plotter.plot_energy_by_year_built(aggregated_year_data)
        else:
            print("No valid year built/moved-in data found for plotting.")

        # --- FINAL SUMMARY REPORT ---
        print(f"\n\n{'=' * 70}")
        print("COMPREHENSIVE SURVEY ANALYSIS - FINAL SUMMARY")
        print(f"{'=' * 70}")
        print(f"\nTotal Households Analyzed: {len(df)}")
        print(f"\nAggregate Energy Statistics:")
        print(f"  Total Electricity Consumption: {sum(all_users_combined_electricity_kwh_breakdown.values()):.0f} kWh/year")
        print(f"  Total Energy (All Fuels): {sum(all_users_combined_total_btu_breakdown.values())/1_000_000:,.0f} Million BTU/year")
        
        if all_users_combined_electricity_kwh_breakdown:
            avg_kwh_per_household = sum(all_users_combined_electricity_kwh_breakdown.values()) / len(df)
            print(f"  Average per Household: {avg_kwh_per_household:.0f} kWh/year")
        
        print(f"\nTop 5 Energy Consuming Categories (Aggregate):")
        sorted_categories = sorted(all_users_combined_electricity_kwh_breakdown.items(), key=lambda x: x[1], reverse=True)
        for i, (category, kwh) in enumerate(sorted_categories[:5], 1):
            percentage = (kwh / sum(all_users_combined_electricity_kwh_breakdown.values()) * 100) if all_users_combined_electricity_kwh_breakdown else 0
            print(f"  {i}. {category}: {kwh:.0f} kWh/year ({percentage:.1f}%)")
        
        print(f"\nAnalysis Complete! Generated visualizations and detailed recommendations.")
        print(f"{'=' * 70}\n")


    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found. Please ensure it's in the correct directory.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty. Please provide a CSV with data.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging


# --- How to use the function ---
# Ensure your prepared CSV file (e.g., 'realistic_dummy_forms_prepared.csv')
# is in the same directory as this script, or provide the full path to the file.
if __name__ == '__main__':
    print_personal_appliance_data('realistic_dummy_forms.csv')  # Or 'realistic_dummy_forms_prepared.csv'
