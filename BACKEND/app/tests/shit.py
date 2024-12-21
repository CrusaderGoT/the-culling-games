from pathlib import Path

# Get the base directory of the current script or project
base_dir = Path(__file__).resolve().parent

print(base_dir)