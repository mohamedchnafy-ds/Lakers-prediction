import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from data_loader import load_data, prepare_ml_features
from ml_model import LakersPredictor
import pandas as pd

# Page config
st.set_page_config(
    page_title="Lakers Analytics Dashboard",
    page_icon="🏀",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 5px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Load data
team_df, players_df, stats_df = load_data()

# Sidebar
st.sidebar.title("Lakers Dashboard")
selected_view = st.sidebar.radio(
    "Select View",
    ["Team Overview", "Player Stats", "Points Predictor"]
)

if selected_view == "Team Overview":
    st.title("Los Angeles Lakers Team Overview")
    
    # Team Record
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Wins", team_df['wins'].iloc[0])
    with col2:
        st.metric("Losses", team_df['losses'].iloc[0])
    with col3:
        win_pct = team_df['wins'].iloc[0] / (team_df['wins'].iloc[0] + team_df['losses'].iloc[0])
        st.metric("Win %", f"{win_pct:.3f}")
    
    # Roster Overview
    st.subheader("Team Roster")
    
    # Position distribution
    pos_dist = players_df['position'].value_counts()
    fig_pos = px.pie(
        values=pos_dist.values,
        names=pos_dist.index,
        title="Position Distribution"
    )
    st.plotly_chart(fig_pos)
    
    # Create height vs weight scatter plot
    fig_hw = px.scatter(
        players_df,
        x='height_inches',
        y='weight',
        text='name',
        title='Lakers Roster: Height vs Weight Distribution',
        labels={'height_inches': 'Height (inches)', 'weight': 'Weight (lbs)'}
    )
    fig_hw.update_traces(textposition='top center')
    st.plotly_chart(fig_hw)

elif selected_view == "Player Stats":
    st.title("Lakers Player Statistics")
    
    if stats_df.empty:
        st.warning("No player statistics available. Please run the ETL pipeline to collect data.")
    else:
        # Player selector
        selected_player = st.selectbox(
            "Select Player",
            stats_df['name'].unique()
        )
        
        # Player stats
        player_stats = stats_df[stats_df['name'] == selected_player]
        if not player_stats.empty:
            player_stats = player_stats.iloc[0]
            
            # Display key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Points per Game", f"{float(player_stats['points_per_game']):.1f}")
            with col2:
                st.metric("Rebounds per Game", f"{float(player_stats['rebounds_per_game']):.1f}")
            with col3:
                st.metric("Assists per Game", f"{float(player_stats['assists_per_game']):.1f}")
            with col4:
                st.metric("FG%", f"{float(player_stats['field_goal_percentage']):.1f}%")
            
            # Shooting splits
            fig_shooting = go.Figure()
            fig_shooting.add_trace(go.Bar(
                x=['Field Goal %', '3PT %', '2PT %'],
                y=[
                    player_stats['field_goal_percentage'],
                    player_stats['three_point_percentage'],
                    player_stats['two_point_percentage']
                ],
                name='Shooting Splits'
            ))
            fig_shooting.update_layout(title="Shooting Percentages")
            st.plotly_chart(fig_shooting)
        else:
            st.warning(f"No statistics available for {selected_player}")

else:  # Points Predictor
    st.title("Lakers Points Predictor")
    
    # Prepare data for ML
    X, y = prepare_ml_features(stats_df)
    
    if X.empty or len(X) < 2:
        st.warning("Insufficient data for prediction model. Please run the ETL pipeline to collect more data.")
    else:
        # Train model
        predictor = LakersPredictor()
        metrics = predictor.train(X, y)
        
        # Model metrics
        st.subheader("Model Performance")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("R² Score", f"{metrics['r2_score']:.3f}")
        with col2:
            st.metric("RMSE", f"{metrics['rmse']:.3f}")
        
        # Feature importance plot
        feat_imp = predictor.get_feature_importance()
        fig_imp = px.bar(
            feat_imp,
            x='importance',
            y='feature',
            orientation='h',
            title="Feature Importance"
        )
        st.plotly_chart(fig_imp)
        
        # Interactive prediction
        st.subheader("Predict Points per Game")
        
        col1, col2 = st.columns(2)
        with col1:
            games = st.number_input("Games Played", min_value=1, max_value=82, value=20)
            minutes = st.number_input("Minutes per Game", min_value=0, max_value=48, value=25)
            fg_pct = st.number_input("Field Goal %", min_value=0.0, max_value=100.0, value=45.0)
        
        with col2:
            three_pct = st.number_input("Three Point %", min_value=0.0, max_value=100.0, value=35.0)
            rebounds = st.number_input("Rebounds per Game", min_value=0.0, max_value=20.0, value=5.0)
            assists = st.number_input("Assists per Game", min_value=0.0, max_value=15.0, value=3.0)
        
        # Make prediction
        if st.button("Predict Points"):
            input_data = pd.DataFrame([[games, minutes, fg_pct, three_pct, rebounds, assists]], 
                                    columns=X.columns)
            prediction = predictor.predict(input_data)[0]
            st.success(f"Predicted Points per Game: {prediction:.1f}")

# Footer
st.markdown("---")
st.markdown("Lakers Analytics Dashboard | Data updated daily")
