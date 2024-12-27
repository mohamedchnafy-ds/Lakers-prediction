# NBA Data Engineering Project

This project implements a comprehensive data pipeline for collecting, processing, and storing NBA data in real-time. The pipeline scrapes data from basketball-reference.com, processes it, and stores it in a PostgreSQL database.

## Project Structure

```
project/
│
├── src/
│   ├── scraper.py      # Data collection module
│   ├── database.py     # Database operations
│   ├── models.py       # SQLAlchemy models
│   └── etl.py          # Main ETL pipeline
│
├── requirements.txt    # Project dependencies
└── README.md          # Project documentation
```

## Features

- Real-time NBA data scraping
- Automated ETL pipeline
- PostgreSQL database storage
- Team and player statistics tracking
- Scheduled data updates

## Setup

1. Create a PostgreSQL database
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your database configuration:
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/nba_data
   ```

## Usage

Run the ETL pipeline:
```bash
python src/etl.py
```

The pipeline will:
- Run immediately upon startup
- Schedule automatic updates every 6 hours
- Log all operations and errors

## Data Model

### Teams Table
- Basic team information
- Current season performance metrics

### Players Table
- Player biographical information
- Team affiliations

### Player Stats Table
- Detailed player statistics
- Updated regularly with new game data

## Error Handling

The pipeline includes comprehensive error handling:
- Network request retries
- Database transaction management
- Detailed logging
- Graceful failure recovery

## Maintenance

- Logs are available in the console output
- Database tables are created automatically if they don't exist
- Data is upserted to prevent duplicates

## Dependencies

- requests: Web scraping
- beautifulsoup4: HTML parsing
- pandas: Data manipulation
- sqlalchemy: Database ORM
- psycopg2-binary: PostgreSQL adapter
- python-dotenv: Environment configuration
- schedule: Task scheduling
- lxml: XML processing
