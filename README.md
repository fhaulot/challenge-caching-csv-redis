# Airline On-Time Data Caching with Redis

This project demonstrates caching CSV-based computations using Redis. It processes the Airline On-Time dataset and caches aggregation results to improve performance.

---

## 📂 Project Structure

```
.
├── main.py # Entry point
├── cache.py # Redis cache helper functions
├── data
│ ├── flights.csv
│ ├── airlines.csv
│ └── airports.csv
├── assets # Screenshots and other assets
├── .env # Environment variables (CACHE_TTL, CSV_FILE, etc.)
├── requirements.txt
└── README.md
```

## ⚙️ Setup

1. **Clone the repo**

```bash
git clone <repo-url>
cd challenge-caching-csv-redis
```
2. **Create a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
pip install -r requirements.txt
```
3. **Start Redis**

Local installation: Make sure Redis server is running on localhost:6379.

Docker:

```bash
docker run -d -p 6379:6379 redis
```
## 🏃 Running the App

First run: CSV is processed and results are cached.

Subsequent runs within TTL: results are retrieved from Redis.

Logs indicate cache hits and computation times.

## 📝 Example Queries

Average arrival delay per airline

Total flights per origin airport

Average departure delay per month

## 📸 Screenshots

Screenshots of execution can be found in the assets
folder.

## 💡 Notes

Ensure column mappings are correct for merging airline and airport names.

TTL can be adjusted in the .env file.

Cache performance can be logged with retrieval time.