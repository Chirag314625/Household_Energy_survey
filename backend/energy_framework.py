# energy_framework.py

class ApplianceModel:
    """
    Base class for all household appliance energy models.
    Inspired by Modelica's component-based energy modeling approach.
    """
    def __init__(self, name, rated_power_watts):
        self.name = name
        self.rated_power = rated_power_watts   # in Watts
        self.daily_energy_kwh = 0
        self.monthly_energy_kwh = 0
        self.annual_energy_kwh = 0
        self.cost_per_unit = 6.0  # ₹ per kWh (adjust for your region)

    def calculate_energy(self, **kwargs):
        raise NotImplementedError("Each appliance must implement this")

    def calculate_cost(self):
        return {
            "daily_cost":   round(self.daily_energy_kwh * self.cost_per_unit, 2),
            "monthly_cost": round(self.monthly_energy_kwh * self.cost_per_unit, 2),
            "annual_cost":  round(self.annual_energy_kwh * self.cost_per_unit, 2),
        }

    def get_report(self):
        cost = self.calculate_cost()
        return {
            "appliance": self.name,
            "daily_kwh":   round(self.daily_energy_kwh, 3),
            "monthly_kwh": round(self.monthly_energy_kwh, 3),
            "annual_kwh":  round(self.annual_energy_kwh, 3),
            **cost
        }