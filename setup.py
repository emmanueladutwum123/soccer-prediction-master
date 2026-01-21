"""
Setup script for Soccer Prediction Master
"""

import os
from pathlib import Path

print("🚀 Setting up Soccer Prediction Master...")

# Create directory structure
folders = [
    'data/raw',
    'data/processed',
    'data/features',
    'models/training',
    'models/trained_models',
    'models/evaluation',
    'src/data_collection',
    'src/feature_engineering',
    'src/modeling',
    'src/prediction',
    'src/web_app',
    'tests',
    'docs',
    'notebooks',
    'web_app/static',
    'web_app/templates'
]

print("Creating project structure...")
for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)
    print(f"  📁 {folder}")

# Create .gitkeep files to preserve empty folders
print("\nCreating placeholder files...")
for folder in folders:
    gitkeep = Path(folder) / '.gitkeep'
    if not gitkeep.exists():
        gitkeep.write_text('# Placeholder file')

print("\n✅ Setup complete!")
print("\nNext steps:")
print("1. Install dependencies: pip install -r requirements.txt")
print("2. Start building your prediction system")
print("3. Check the created folders in the file explorer")
