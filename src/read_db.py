import sqlite3
import pandas as pd
from tabulate import tabulate
import os

def read_database():
    # Get the absolute path to the database file
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nba_data.db')
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # Read teams table
    print("\n=== LAKERS TEAM INFO ===")
    teams_df = pd.read_sql_query("SELECT * FROM teams", conn)
    print(tabulate(teams_df, headers='keys', tablefmt='pretty', showindex=False))
    
    # Read players table
    print("\n=== LAKERS ROSTER ===")
    players_df = pd.read_sql_query("SELECT name, number, position, height, weight, college FROM players", conn)
    print(tabulate(players_df, headers='keys', tablefmt='pretty', showindex=False))
    
    # Read player stats table
    print("\n=== LAKERS PLAYER STATS ===")
    stats_df = pd.read_sql_query("""
        SELECT 
            p.name,
            ps.games_played,
            ps.minutes_played,
            ps.points_per_game,
            ps.rebounds_per_game,
            ps.assists_per_game,
            ps.field_goal_percentage,
            ps.three_point_percentage
        FROM player_stats ps
        JOIN players p ON ps.player_id = p.player_id
        ORDER BY CAST(ps.points_per_game AS FLOAT) DESC
    """, conn)
    print(tabulate(stats_df, headers='keys', tablefmt='pretty', showindex=False))
    
    # Close the connection
    conn.close()

if __name__ == "__main__":
    read_database()
