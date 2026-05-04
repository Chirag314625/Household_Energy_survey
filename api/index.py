from pathlib import Path
import importlib.util
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
BACKEND_DIR = ROOT_DIR / "app" / "backend"
APP_FILE = BACKEND_DIR / "app.py"

sys.path.insert(0, str(BACKEND_DIR))

spec = importlib.util.spec_from_file_location("household_energy_backend", APP_FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

app = module.app
