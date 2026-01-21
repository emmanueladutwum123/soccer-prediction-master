#!/usr/bin/env python3
"""
Main entry point for Soccer Prediction Master
"""

import argparse
import sys
import logging
from pathlib import Path

# Add src to path to allow imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def collect_data(args):
    """Collect data from various sources"""
    try:
        from data_collection.main import DataCollector
        logger.info(f"Starting data collection for {args.league} {args.season}")
        
        collector = DataCollector()
        matches = collector.collect_matches(args.league, args.season)
        
        if matches.empty:
            logger.warning("No data collected")
        else:
            logger.info(f"Collected {len(matches)} matches")
            # Save data
            output_file = f"data/raw/{args.league}_{args.season.replace('-', '_')}.csv"
            Path("data/raw").mkdir(parents=True, exist_ok=True)
            matches.to_csv(output_file, index=False)
            logger.info(f"Data saved to {output_file}")
            
        return True
    except ImportError as e:
        logger.error(f"Import error: {e}. Make sure src/data_collection/main.py exists")
        return False
    except Exception as e:
        logger.error(f"Error collecting data: {e}")
        return False

def train_model(args):
    """Train prediction models"""
    logger.info("Starting model training...")
    logger.info(f"Training {args.model} model for {args.epochs} epochs")
    
    # TODO: Implement actual training
    print("\nModel training would include:")
    print("1. Loading historical match data")
    print("2. Feature engineering")
    print("3. Training ML models (XGBoost, Random Forest, etc.)")
    print("4. Model evaluation and selection")
    
    return True

def predict_match(args):
    """Predict match outcomes"""
    logger.info(f"Predicting match: {args.home} vs {args.away}")
    
    # TODO: Implement actual prediction
    print(f"\nMatch Prediction:")
    print(f"Home: {args.home}")
    print(f"Away: {args.away}")
    print(f"Date: {args.date or 'Not specified'}")
    print("\nPrediction would include:")
    print("1. Team form analysis")
    print("2. Head-to-head statistics")
    print("3. Player availability")
    print("4. ML model prediction")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description="⚽ Soccer Prediction Master - Advanced Prediction System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py collect --league EPL --season 2023-2024
  python main.py train --model xgboost --epochs 100
  python main.py predict --home "Manchester United" --away "Liverpool"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Collect data command
    collect_parser = subparsers.add_parser("collect", help="Collect match data")
    collect_parser.add_argument("--league", required=True, help="League code (e.g., EPL)")
    collect_parser.add_argument("--season", required=True, help="Season (e.g., 2023-2024)")
    collect_parser.add_argument("--source", default="demo", help="Data source (demo/api)")
    
    # Train model command
    train_parser = subparsers.add_parser("train", help="Train prediction models")
    train_parser.add_argument("--model", default="xgboost", help="Model type to train")
    train_parser.add_argument("--epochs", type=int, default=100, help="Training epochs")
    
    # Predict command
    predict_parser = subparsers.add_parser("predict", help="Predict match outcome")
    predict_parser.add_argument("--home", required=True, help="Home team")
    predict_parser.add_argument("--away", required=True, help="Away team")
    predict_parser.add_argument("--date", help="Match date (YYYY-MM-DD)")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    try:
        if args.command == "collect":
            success = collect_data(args)
        elif args.command == "train":
            success = train_model(args)
        elif args.command == "predict":
            success = predict_match(args)
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
