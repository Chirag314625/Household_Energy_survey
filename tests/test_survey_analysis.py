import sys
import unittest
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from survey_analytics.survey_analysis import (  # noqa: E402
    EnergyConsumptionCosts,
    safe_numeric_conversion,
)


class SurveyAnalysisTests(unittest.TestCase):
    def test_safe_numeric_conversion_cleans_currency_and_commas(self):
        self.assertEqual(safe_numeric_conversion("50,000"), 50000)
        self.assertEqual(safe_numeric_conversion("not a number", default=7), 7)

    def test_estimate_annual_electricity_consumption_breakdown(self):
        row = {
            "Q9_num_refrigerators": 1,
            "Q10_refrigerator_size": "Medium (17.6 to 22.5 cubic feet)",
            "Q12_refrigerator_age": "Less than 2 years old",
            "Q37_has_ac": "No",
            "Q38_uses_central_ac": "No",
            "Q42_num_ceiling_fans": 2,
            "Q47_num_light_bulbs_total": 4,
            "Q48_num_light_bulbs_4hr_plus": 2,
            "Q49_LED__light_emitting_diode_": "Yes",
            "Q49_CFL__compact_fluorescent_lamp_": "No",
            "Q49_Incandescent": "No",
            "Q26_num_televisions": 1,
            "Q27_tv_size": "40 to 59 inches",
            "Q28_tv_type": "LED",
            "Q29_tv_daily_hours": 4,
            "Q43_has_water_heater": "Yes",
            "Q46_water_heater_fuel": "Electricity",
            "Q19_has_clothes_washer": "No",
        }

        total_kwh, breakdown = EnergyConsumptionCosts(row).estimate_annual_electricity_consumption()

        self.assertAlmostEqual(breakdown["Refrigerator"], 657.0)
        self.assertAlmostEqual(breakdown["Ceiling Fans"], 657.0)
        self.assertAlmostEqual(breakdown["Lighting"], 58.4)
        self.assertAlmostEqual(breakdown["Televisions"], 140.16)
        self.assertAlmostEqual(breakdown["Water Heater (Electric)"], 730.0)
        self.assertAlmostEqual(total_kwh, sum(breakdown.values()))


if __name__ == "__main__":
    unittest.main()
