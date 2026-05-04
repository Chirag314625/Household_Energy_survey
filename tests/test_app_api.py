import importlib
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "app" / "backend"
sys.path.insert(0, str(BACKEND_DIR))

os.environ["DISABLE_MONGODB"] = "1"
app_module = importlib.import_module("app")


class FakeSurveyCollection:
    def __init__(self):
        self.inserted_documents = []

    def insert_one(self, document):
        self.inserted_documents.append(document)
        return SimpleNamespace(inserted_id="test-survey-id")


class FlaskApiTests(unittest.TestCase):
    def setUp(self):
        app_module.app.config["TESTING"] = True
        self.client = app_module.app.test_client()

    def tearDown(self):
        app_module.db = None
        app_module.surveys_collection = None

    def test_calculate_returns_expected_totals(self):
        response = self.client.post(
            "/api/calculate",
            json={
                "tariff": 7,
                "fridge": {"watts": 100, "duty": 0.5, "qty": 2},
                "lighting": {"watts": 10, "qty": 5, "hours": 4},
            },
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertEqual(data["total_daily"], 2.6)
        self.assertEqual(data["total_monthly"], 78)
        self.assertEqual(data["monthly_cost"], 546)
        self.assertEqual(data["tariff"], 7)
        self.assertEqual(
            {item["name"]: item["daily"] for item in data["appliances"]},
            {"Refrigerator": 2.4, "Lighting": 0.2},
        )

    def test_submit_survey_saves_to_collection(self):
        fake_collection = FakeSurveyCollection()
        app_module.db = object()
        app_module.surveys_collection = fake_collection

        response = self.client.post(
            "/api/submit-survey",
            json={"name": "Test User", "Q2_num_adults": 3},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["id"], "test-survey-id")
        self.assertEqual(len(fake_collection.inserted_documents), 1)
        inserted = fake_collection.inserted_documents[0]
        self.assertEqual(inserted["name"], "Test User")
        self.assertIn("submitted_at", inserted)

    def test_submit_survey_rejects_empty_request(self):
        response = self.client.post("/api/submit-survey", json=None)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()["error"], "No form data provided")


if __name__ == "__main__":
    unittest.main()
