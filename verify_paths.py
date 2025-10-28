import os
from pathlib import Path

print("=== File Path Verification ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Is this a Hugging Face Space? {'SPACE_ID' in os.environ}")

# Check model file
model_path = Path("/home/user/app/Models/svc.pkl")
print(f"\nChecking model file at: {model_path}")
print(f"Exists: {model_path.exists()}")

# Check data directory
data_dir = Path("/home/user/app/Data.csv")
print(f"\nChecking data directory at: {data_dir}")
print(f"Exists: {data_dir.exists()}")
print(f"Contents: {list(data_dir.glob('*')) if data_dir.exists() else 'N/A'}")

# Check local paths for comparison
local_model = Path("Models/svc.pkl")
print(f"\nLocal model path: {local_model.absolute()}")
print(f"Local model exists: {local_model.exists()}")

# Check environment variables
print("\nEnvironment Variables:")
for var in ['SPACE_ID', 'IS_HF_SPACE', 'PYTHONPATH']:
    print(f"{var}: {os.environ.get(var, 'Not set')}")

print("\n=== Verification Complete ===")
