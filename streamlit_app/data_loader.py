import sqlite3
import pandas as pd
from typing import Tuple, Dict
import os

def load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load data from SQLite database
    Returns:
        Tuple of DataFrames (team_df, players_df, stats_df)
    """
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nba_data.db')
    conn = sqlite3.connect(db_path)
    
    # Load team data
    team_df = pd.read_sql_query("SELECT * FROM teams", conn)
    
    # Load players data
    players_df = pd.read_sql_query("""
        SELECT 
            player_id,
            name,
            number,
            position,
            CAST(SUBSTR(height, 1, INSTR(height, '-')-1) AS INTEGER) * 12 + 
            CAST(SUBSTR(height, INSTR(height, '-')+1) AS INTEGER) as height_inches,
            CAST(weight AS INTEGER) as weight,
            college
        FROM players
    """, conn)
    
    # Load player stats data with player names
    stats_df = pd.read_sql_query("""
        SELECT 
            ps.*,
            p.name,
            p.position,
            p.height,
            p.weight
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
    """, conn)
    
    # Convert numeric columns to float
    numeric_columns = ['points_per_game', 'rebounds_per_game', 'assists_per_game',
                      'field_goal_percentage', 'three_point_percentage', 'two_point_percentage']
    for col in numeric_columns:
        stats_df[col] = pd.to_numeric(stats_df[col], errors='coerce')
    
    conn.close()
    
    # Convert height to numeric format
    if 'height' in players_df.columns:
        players_df['height'] = players_df['height'].astype(str)
    
    return team_df, players_df, stats_df

def prepare_ml_features(stats_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Prepare features for ML model
    """
    if stats_df.empty:
        # Return empty DataFrames with correct columns if no data
        feature_cols = [
            'games_played', 'minutes_played', 'field_goal_percentage',
            'three_point_percentage', 'rebounds_per_game', 'assists_per_game'
        ]
        return pd.DataFrame(columns=feature_cols), pd.Series(dtype=float)
    
    # Select relevant features
    feature_cols = [
        'games_played', 'minutes_played', 'field_goal_percentage',
        'three_point_percentage', 'rebounds_per_game', 'assists_per_game'
    ]
    
    # Create feature matrix X and target variable y
    X = stats_df[feature_cols].copy()
    y = stats_df['points_per_game'].copy()
    
    # Convert to numeric and handle missing values
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce')
    X = X.fillna(X.mean())
    y = pd.to_numeric(y, errors='coerce').fillna(y.mean())
    
    return X, y
