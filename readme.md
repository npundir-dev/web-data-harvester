# Web Data Harvester CLI

An automated web scraping tool that collects book data from 
books.toscrape.com on a configurable schedule and delivers 
clean, structured output — no manual work required.

## Features
- Scrapes title, price, rating, and availability from live website
- Cleans and structures raw HTML data automatically
- Exports to both CSV and JSON formats
- CLI menu for manual or scheduled runs
- Full logging to terminal and log file
- Production-grade structure with error handling throughout

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file in project root:
LOG_LEVEL=INFO
LOG_FOLDER=logs
OUTPUT_DIR=data

## Usage
```bash
python main.py
```
Then select from the menu:
- **1** — Scrape now
- **2** — Schedule automatic scraping
- **3** — Exit

## Output
Results are saved to the `data/` folder:
- `books.csv` — for Excel and spreadsheet tools
- `books.json` — for APIs and developer tools

## Project Structure
web_harvester/
├── scraper/        # Harvester and data cleaner
├── storage/        # CSV and JSON handlers
├── utils/          # Logger and scheduler
├── config.py       # Centralised settings
└── main.py         # Entry point

## Requirements
- Python 3.10+
- See requirements.txt
