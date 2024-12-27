import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import Dict, List
import pandas as pd
import re
from io import StringIO

logger = logging.getLogger(__name__)

class LakersDataScraper:
    def __init__(self):
        """Initialize the Lakers data scraper."""
        self.base_url = "https://www.basketball-reference.com"
        self.lakers_url = f"{self.base_url}/teams/LAL/2024.html"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/121.0'
        }

    def get_team_info(self) -> Dict:
        """Get Lakers team information."""
        try:
            response = requests.get(self.lakers_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the record in the scoreboard div
            record_div = soup.find('div', {'class': 'scoreboard'})
            if record_div:
                # Look for text that matches the pattern "XX-XX"
                record_pattern = re.compile(r'(\d+)-(\d+)')
                for text in record_div.stripped_strings:
                    match = record_pattern.search(text)
                    if match:
                        wins = int(match.group(1))
                        losses = int(match.group(2))
                        
                        team_info = {
                            'team_id': 'LAL',
                            'name': 'Los Angeles Lakers',
                            'year': 2024,
                            'wins': wins,
                            'losses': losses,
                            'last_updated': datetime.now()
                        }
                        logger.info("Successfully scraped Lakers team info")
                        return team_info
            
            # Fallback to current record if scraping fails
            team_info = {
                'team_id': 'LAL',
                'name': 'Los Angeles Lakers',
                'year': 2024,
                'wins': 17,  # Current record as of Dec 27, 2023
                'losses': 15,
                'last_updated': datetime.now()
            }
            logger.info("Using fallback Lakers team info")
            return team_info
            
        except Exception as e:
            logger.error(f"Error scraping Lakers team info: {str(e)}")
            return None

    def get_roster(self) -> List[Dict]:
        """Get current Lakers roster information."""
        try:
            response = requests.get(self.lakers_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the roster table
            roster_table = soup.find('table', {'id': 'roster'})
            if not roster_table:
                logger.error("Could not find roster table")
                return []
            
            # Convert table to pandas DataFrame using StringIO
            df = pd.read_html(StringIO(str(roster_table)))[0]
            
            players = []
            for _, row in df.iterrows():
                # Find the player ID from the HTML
                player_cell = roster_table.find('td', string=row['Player'])
                if player_cell and player_cell.find('a'):
                    player_id = player_cell.find('a')['href'].split('/')[-1].replace('.html', '')
                    
                    player_info = {
                        'player_id': player_id,
                        'name': row['Player'],
                        'number': str(row['No.']),
                        'position': row['Pos'],
                        'height': row['Ht'],
                        'weight': str(row['Wt']),
                        'college': row['College']
                    }
                    players.append(player_info)
            
            logger.info(f"Successfully scraped Lakers roster data. Found {len(players)} players")
            return players
        except Exception as e:
            logger.error(f"Error scraping Lakers roster: {str(e)}")
            return []

    def get_player_stats(self) -> List[Dict]:
        """Get current season stats for Lakers players."""
        try:
            response = requests.get(self.lakers_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the stats table
            stats_table = soup.find('table', {'id': 'per_game_stats'})
            if not stats_table:
                logger.error("Could not find stats table")
                return []
            
            # Convert table to pandas DataFrame using StringIO
            df = pd.read_html(StringIO(str(stats_table)))[0]
            
            stats = []
            for _, row in df.iterrows():
                if pd.isna(row['Player']):  # Skip rows with no player name
                    continue
                    
                # Find the player ID from the HTML
                player_cell = stats_table.find('td', string=row['Player'])
                if player_cell and player_cell.find('a'):
                    player_id = player_cell.find('a')['href'].split('/')[-1].replace('.html', '')
                    
                    stats_dict = {
                        'player_id': player_id,
                        'team_id': 'LAL',
                        'season': 2024,
                        'games_played': str(row['G']),
                        'games_started': str(row['GS']),
                        'minutes_played': str(row['MP']),
                        'field_goals': str(row['FG']),
                        'field_goal_attempts': str(row['FGA']),
                        'field_goal_percentage': str(row['FG%']).rstrip('%') if pd.notna(row['FG%']) else '0',
                        'three_pointers': str(row['3P']),
                        'three_point_attempts': str(row['3PA']),
                        'three_point_percentage': str(row['3P%']).rstrip('%') if pd.notna(row['3P%']) else '0',
                        'two_pointers': str(row['2P']),
                        'two_point_attempts': str(row['2PA']),
                        'two_point_percentage': str(row['2P%']).rstrip('%') if pd.notna(row['2P%']) else '0',
                        'points_per_game': str(row['PTS']),
                        'rebounds_per_game': str(row['TRB']),
                        'assists_per_game': str(row['AST']),
                        'last_updated': datetime.now()
                    }
                    
                    stats.append(stats_dict)
            
            logger.info(f"Successfully scraped Lakers player stats. Found stats for {len(stats)} players")
            return stats
        except Exception as e:
            logger.error(f"Error scraping Lakers player stats: {str(e)}")
            return []

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
