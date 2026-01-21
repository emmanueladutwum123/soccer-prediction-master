"""
Main data collection orchestrator
"""

import asyncio
import pandas as pd
import logging
from typing import Dict, List
import yaml
from pathlib import Path

from .api_client import FootballDataClient, FreeFootballData

logger = logging.getLogger(__name__)

class DataCollector:
    """Orchestrates data collection from multiple sources"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.clients = self._initialize_clients()
        
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return {}
    
    def _initialize_clients(self) -> Dict:
        """Initialize API clients"""
        clients = {}
        
        # Football-data.org client
        api_key = self.config.get('data_sources', {}).get('football_data_org', {}).get('api_key')
        if api_key:
            clients['football_data'] = FootballDataClient(api_key=api_key)
            logger.info("Initialized FootballData.org client")
        
        # Free data client
        clients['free_data'] = FreeFootballData()
        logger.info("Initialized free data client")
        
        return clients
    
    async def collect_league_data(self, league_code: str, season: str) -> pd.DataFrame:
        """Collect all data for a specific league and season"""
        logger.info(f"Collecting data for {league_code} {season}")
        
        tasks = []
        
        # Collect from football-data.org if available
        if 'football_data' in self.clients:
            tasks.append(
                self._collect_matches_football_data(league_code, season)
            )
        
        # Collect from free sources
        tasks.append(
            self._collect_free_data(league_code, season)
        )
        
        # Execute all collection tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results
        combined_data = self._combine_results(results)
        
        # Save to data/raw
        self._save_data(combined_data, league_code, season)
        
        return combined_data
    
    async def _collect_matches_football_data(self, league_code: str, season: str) -> pd.DataFrame:
        """Collect matches from football-data.org"""
        try:
            client = self.clients.get('football_data')
            if client:
                matches = client.get_matches(league_code, int(season[:4]))
                logger.info(f"Collected {len(matches)} matches from football-data.org")
                return matches
        except Exception as e:
            logger.error(f"Error collecting from football-data.org: {e}")
        return pd.DataFrame()
    
    async def _collect_free_data(self, league_code: str, season: str) -> pd.DataFrame:
        """Collect data from free sources"""
        # TODO: Implement web scraping from Understat/FBref
        logger.info(f"Would collect free data for {league_code} {season}")
        return pd.DataFrame()
    
    def _combine_results(self, results: List) -> pd.DataFrame:
        """Combine data from multiple sources"""
        if not results:
            return pd.DataFrame()
        
        # Filter out exceptions and empty dataframes
        valid_results = []
        for result in results:
            if isinstance(result, pd.DataFrame) and not result.empty:
                valid_results.append(result)
            elif isinstance(result, Exception):
                logger.error(f"Data collection error: {result}")
        
        if not valid_results:
            return pd.DataFrame()
        
        # Start with first dataframe
        combined = valid_results[0].copy()
        
        # Merge additional dataframes
        for df in valid_results[1:]:
            if 'match_id' in df.columns and 'match_id' in combined.columns:
                combined = pd.merge(combined, df, on='match_id', how='outer', suffixes=('', '_dup'))
        
        return combined
    
    def _save_data(self, data: pd.DataFrame, league_code: str, season: str):
        """Save collected data"""
        if data.empty:
            logger.warning("No data to save")
            return
        
        # Create filename
        filename = f"data/raw/{league_code}_{season.replace('-', '_')}.csv"
        
        # Ensure directory exists
        Path("data/raw").mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        data.to_csv(filename, index=False)
        logger.info(f"Saved data to {filename}")
        
        # Also save as Parquet for better performance
        parquet_file = f"data/raw/{league_code}_{season.replace('-', '_')}.parquet"
        data.to_parquet(parquet_file, index=False)
        logger.info(f"Saved data to {parquet_file}")

async def main():
    """Main function to run data collection"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Collect soccer match data")
    parser.add_argument("--league", required=True, help="League code (e.g., PL, PD)")
    parser.add_argument("--season", required=True, help="Season (e.g., 2023-2024)")
    
    args = parser.parse_args()
    
    collector = DataCollector()
    data = await collector.collect_league_data(args.league, args.season)
    
    if not data.empty:
        print(f"\n✅ Collected {len(data)} matches")
        print("\nSample data:")
        print(data.head())
    else:
        print("❌ No data collected")

if __name__ == "__main__":
    asyncio.run(main())
