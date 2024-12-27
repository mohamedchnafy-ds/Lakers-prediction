from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Team, Player, PlayerStats
import logging
import os
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, database_url: str = None):
        if database_url is None:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///nba_data.db')
        
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        logger.info("Database tables created successfully")
    
    def _convert_to_float(self, value: str) -> float:
        """Convert string to float, handling empty strings and percentage signs"""
        if not value or value.strip() == '':
            return 0.0
        return float(value.rstrip('%'))
    
    def upsert_team(self, team_data: Dict) -> None:
        """Upsert team data into the database"""
        session = self.Session()
        try:
            team = session.query(Team).filter_by(team_id=team_data['team_id']).first()
            if team:
                for key, value in team_data.items():
                    setattr(team, key, value)
            else:
                team = Team(**team_data)
                session.add(team)
            
            session.commit()
            logger.info(f"Successfully upserted team: {team_data['name']}")
        except Exception as e:
            session.rollback()
            logger.error(f"Error upserting team: {str(e)}")
        finally:
            session.close()
    
    def upsert_players(self, players_data: List[Dict]) -> None:
        """Upsert multiple players into the database"""
        session = self.Session()
        try:
            for player_data in players_data:
                player = session.query(Player).filter_by(player_id=player_data['player_id']).first()
                if player:
                    for key, value in player_data.items():
                        setattr(player, key, value)
                else:
                    player = Player(**player_data)
                    session.add(player)
            
            session.commit()
            logger.info(f"Successfully upserted {len(players_data)} players")
        except Exception as e:
            session.rollback()
            logger.error(f"Error upserting players: {str(e)}")
        finally:
            session.close()
    
    def upsert_player_stats(self, stats_data: List[Dict]) -> None:
        """Upsert player statistics into the database"""
        session = self.Session()
        try:
            # First, remove old stats for the current season
            session.query(PlayerStats).filter_by(season=2024).delete()
            
            # Insert new stats
            for stat_data in stats_data:
                # Convert string values to appropriate types
                for key in ['games_played', 'games_started']:
                    if key in stat_data and stat_data[key]:
                        stat_data[key] = int(stat_data[key])
                
                for key in ['minutes_played', 'field_goals', 'field_goal_attempts',
                           'field_goal_percentage', 'three_pointers', 'three_point_attempts',
                           'three_point_percentage', 'two_pointers', 'two_point_attempts',
                           'two_point_percentage', 'points_per_game', 'rebounds_per_game',
                           'assists_per_game']:
                    if key in stat_data and stat_data[key]:
                        stat_data[key] = self._convert_to_float(stat_data[key])
                
                stats = PlayerStats(**stat_data)
                session.add(stats)
            
            session.commit()
            logger.info(f"Successfully upserted stats for {len(stats_data)} players")
        except Exception as e:
            session.rollback()
            logger.error(f"Error upserting player stats: {str(e)}")
        finally:
            session.close()
