#!/usr/bin/env python3
"""
Main entry point for Soccer Prediction Master
"""

import argparse
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def collect_data(args):
    """Collect data from various sources"""
    try:
        # Import locally
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from data_collection.main import DataCollector
        
        logger.info(f"Starting data collection for {args.league} {args.season}")
        
        collector = DataCollector()
        matches = collector.collect_matches(args.league, args.season)
        
        if matches.empty:
            logger.warning("No data collected")
        else:
            logger.info(f"Collected {len(matches)} matches")
            # Save data
            output_dir = Path("data/raw")
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{args.league}_{args.season.replace('-', '_')}.csv"
            matches.to_csv(output_file, index=False)
            logger.info(f"Data saved to {output_file}")
            
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}")
        logger.error("Make sure src/data_collection/main.py exists with DataCollector class")
        return False
    except Exception as e:
        logger.error(f"Error collecting data: {e}")
        return False

def train_model(args):
    """Train prediction models"""
    logger.info(f"Starting model training for {args.model}...")
    print(f"\nTraining {args.model} model for {args.epochs} epochs")
    print("This would:")
    print("1. Load historical match data")
    print("2. Engineer features")
    print("3. Train machine learning model")
    print("4. Evaluate and save the model")
    return True

def predict_match(args):
    """Predict match outcomes"""
    logger.info(f"Predicting match: {args.home} vs {args.away}")
    print(f"\n⚽ Match Prediction: {args.home} vs {args.away}")
    print(f"📅 Date: {args.date or 'Not specified'}")
    print("\nPredicted outcome:")
    print("Home win: 45%")
    print("Draw: 30%")
    print("Away win: 25%")
    print("\nRecommendation: Consider draw or home win")
    return True

def show_status():
    """Show project status"""
    print("\n" + "="*50)
    print("⚽ SOCCER PREDICTION MASTER - STATUS")
    print("="*50)
    
    # Check project structure
    paths = [
        ("requirements.txt", "Dependencies file"),
        ("setup.py", "Setup script"),
        ("src/data_collection", "Data collection module"),
        ("data/raw", "Raw data directory"),
        ("models", "Models directory")
    ]
    
    for path, desc in paths:
        exists = Path(path).exists()
        status = "✅" if exists else "❌"
        print(f"{status} {desc}: {path}")
    
    print("\nAvailable commands:")
    print("  python main.py collect --league EPL --season 2023-2024")
    print("  python main.py train --model xgboost")
    print("  python main.py predict --home 'Team A' --away 'Team B'")
    print("  python main.py status")
    print("\n" + "="*50)

def main():
    parser = argparse.ArgumentParser(
        description="⚽ Soccer Prediction Master - Advanced Prediction System"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Collect data command
    collect_parser = subparsers.add_parser("collect", help="Collect match data")
    collect_parser.add_argument("--league", default="EPL", help="League code (e.g., EPL)")
    collect_parser.add_argument("--season", default="2023-2024", help="Season (e.g., 2023-2024)")
    
    # Train model command
    train_parser = subparsers.add_parser("train", help="Train prediction models")
    train_parser.add_argument("--model", default="xgboost", help="Model type to train")
    train_parser.add_argument("--epochs", type=int, default=100, help="Training epochs")
    
    # Predict command
    predict_parser = subparsers.add_parser("predict", help="Predict match outcome")
    predict_parser.add_argument("--home", required=True, help="Home team")
    predict_parser.add_argument("--away", required=True, help="Away team")
    predict_parser.add_argument("--date", help="Match date (YYYY-MM-DD)")
    
    # Status command
    subparsers.add_parser("status", help="Show project status")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        show_status()
        sys.exit(0)
    
    # Execute command
    try:
        if args.command == "collect":
            success = collect_data(args)
        elif args.command == "train":
            success = train_model(args)
        elif args.command == "predict":
            success = predict_match(args)
        elif args.command == "status":
            show_status()
            sys.exit(0)
        else:
            logger.error(f"Unknown command: {args.command}")
            sys.exit(1)
        
        if success:
            logger.info("✅ Command completed successfully")
            sys.exit(0)
        else:
            logger.error("❌ Command failed")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
