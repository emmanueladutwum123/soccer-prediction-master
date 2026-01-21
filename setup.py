"""
Setup script for Soccer Prediction Master project.
Run this script to create the complete project structure.
"""

import os
from pathlib import Path
import sys

def create_project_structure():
    """Create the complete folder structure for the project"""
    
    print("🚀 Creating Soccer Prediction Master Project Structure...")
    print("=" * 60)
    
    # Define all folders to create
    folders = [
        # Data directories
        'data/raw',
        'data/processed', 
        'data/features',
        
        # Model directories
        'models/training',
        'models/trained_models',
        'models/evaluation',
        
        # Source code directories
        'src/data_collection',
        'src/feature_engineering', 
        'src/modeling',
        'src/prediction',
        'src/web_app',
        
        # Other directories
        'tests',
        'docs',
        'notebooks',
        
        # Web app directories
        'web_app/static',
        'web_app/templates',
    ]
    
    # Create each folder
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created: {folder}/")
        
        # Create .gitkeep file to preserve empty folders
        gitkeep_file = Path(folder) / '.gitkeep'
        gitkeep_file.write_text('# Placeholder to keep folder in Git\n')
    
    # Create requirements.txt
    requirements_content = """# Core
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
scipy==1.11.1

# ML/DL
xgboost==1.7.6
lightgbm==4.0.0
catboost==1.2.2

# Data collection
requests==2.31.0
beautifulsoup4==4.12.2
selenium==4.12.0

# Web app
flask==3.0.0
plotly==5.17.0
dash==2.14.0

# Utilities
python-dotenv==1.0.0
joblib==1.3.1
tqdm==4.65.0
loguru==0.7.2
"""
    
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    print("📝 Created: requirements.txt")
    
    # Create initial __init__.py files
    init_files = [
        'src/__init__.py',
        'src/data_collection/__init__.py',
        'src/feature_engineering/__init__.py',
        'src/modeling/__init__.py',
        'src/prediction/__init__.py',
        'src/web_app/__init__.py',
        'web_app/__init__.py',
    ]
    
    for init_file in init_files:
        Path(init_file).write_text('"""Package initialization"""\n\n__version__ = "0.1.0"\n')
        print(f"📄 Created: {init_file}")
    
    # Create a simple main.py for data collection
    main_py_content = '''"""
Main data collection module for soccer prediction system.
This will collect data from various football data sources.
"""

print("⚽ Soccer Prediction Master - Data Collection Module")
print("Initial setup complete. Ready to build advanced prediction system!")

if __name__ == "__main__":
    print("\\nTo start collecting data, implement API calls to:")
    print("1. football-data.org (match results)")
    print("2. Understat.com (advanced stats)")
    print("3. Odds APIs (betting market data)")
'''
    
    with open('src/data_collection/main.py', 'w') as f:
        f.write(main_py_content)
    print("📄 Created: src/data_collection/main.py")
    
    print("\n" + "=" * 60)
    print("✅ Project structure created successfully!")
    print("\n📋 Next steps:")
    print("1. Commit these files to your repository")
    print("2. Open in GitHub Codespaces to run the setup")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Start building your prediction system!")
    
    return len(folders)

if __name__ == "__main__":
    try:
        folders_created = create_project_structure()
        print(f"\n📊 Summary: Created {folders_created} directories")
    except Exception as e:
        print(f"❌ Error creating structure: {e}")
        sys.exit(1)
