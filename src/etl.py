import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from scraper import LakersDataScraper
from database import DatabaseManager

# Load environment variables
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LakersDataPipeline:
    def __init__(self):
        """Initialize the Lakers data pipeline."""
        db_url = os.getenv('DATABASE_URL', 'sqlite:///nba_data.db')
        self.db = DatabaseManager(db_url)
        self.scraper = LakersDataScraper()
        
    def run(self):
        """Run the data pipeline."""
        try:
            # Get Lakers team info
            logger.info("Getting Lakers team info...")
            team_data = self.scraper.get_team_info()
            if team_data:
                self.db.upsert_team(team_data)
            
            # Get Lakers roster
            logger.info("Getting Lakers roster...")
            roster_data = self.scraper.get_roster()
            if roster_data:
                self.db.upsert_players(roster_data)
            
            # Get Lakers player stats
            logger.info("Getting Lakers player stats...")
            stats_data = self.scraper.get_player_stats()
            if stats_data:
                self.db.upsert_player_stats(stats_data)
            
            logger.info("Lakers data pipeline completed successfully")
        except Exception as e:
            logger.error(f"Error in Lakers data pipeline: {str(e)}")
            raise

def main():
    """Main entry point for the ETL pipeline."""
    pipeline = LakersDataPipeline()
    pipeline.run()

if __name__ == "__main__":
    main()
