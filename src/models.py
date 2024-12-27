from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Team(Base):
    __tablename__ = 'teams'

    team_id = Column(String, primary_key=True)
    name = Column(String)
    year = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    last_updated = Column(DateTime)

class Player(Base):
    __tablename__ = 'players'

    player_id = Column(String, primary_key=True)
    team_id = Column(String, ForeignKey('teams.team_id'))
    name = Column(String)
    number = Column(String)
    position = Column(String)
    height = Column(String)
    weight = Column(String)
    birth_date = Column(String)
    nationality = Column(String)
    experience = Column(String)
    college = Column(String)

class PlayerStats(Base):
    __tablename__ = 'player_stats'

    id = Column(Integer, primary_key=True)
    player_id = Column(String, ForeignKey('players.player_id'))
    team_id = Column(String, ForeignKey('teams.team_id'))
    season = Column(Integer)
    games_played = Column(Integer)
    games_started = Column(Integer)
    minutes_played = Column(Float)
    field_goals = Column(Float)
    field_goal_attempts = Column(Float)
    field_goal_percentage = Column(Float)
    three_pointers = Column(Float)
    three_point_attempts = Column(Float)
    three_point_percentage = Column(Float)
    two_pointers = Column(Float)
    two_point_attempts = Column(Float)
    two_point_percentage = Column(Float)
    points_per_game = Column(Float)
    rebounds_per_game = Column(Float)
    assists_per_game = Column(Float)
    last_updated = Column(DateTime, default=datetime.now)
