import pandas as pd
from cache import get_from_cache, set_to_cache
from dotenv import load_dotenv
import os
import logging
import time

load_dotenv()

CACHE_TTL = int(os.getenv("CACHE_TTL", 600))
CSV_FILE = os.getenv("CSV_FILE", "data/flights.csv")
AIRLINES_FILE = os.getenv("AIRLINES_FILE", "data/airlines.csv")
AIRPORTS_FILE = os.getenv("AIRPORTS_FILE", "data/airports.csv")

# 🔹 Configurer logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def prepare_dataframe():
    # Load CSV
    flights = pd.read_csv(CSV_FILE)
    airlines = pd.read_csv(AIRLINES_FILE)
    airports = pd.read_csv(AIRPORTS_FILE)

    # Replace IATA codes with real names
    flights = flights.merge(airlines, left_on="AIRLINE", right_on="IATA_CODE", how="left")
    flights.rename(columns={'AIRLINE_y': 'OP_CARRIER'}, inplace=True)
    flights = flights.merge(airports[['AIATA_CODE', 'AIRPORT']], left_on="ORIGIN_AIRPORT", right_on="AIATA_CODE", how="left")
    flights.rename(columns={'AIRPORT': 'ORIGIN'}, inplace=True)
    flights = flights.merge(airports[['AIATA_CODE', 'AIRPORT']], left_on="DESTINATION_AIRPORT", right_on="AIATA_CODE", how="left")
    flights.rename(columns={'AIRPORT': 'DEST'}, inplace=True)

    # Construct FL_DATE
    flights['FL_DATE'] = pd.to_datetime(flights[['YEAR', 'MONTH', 'DAY']])

    # Keep only useful columns
    flights = flights[['OP_CARRIER', 'ORIGIN', 'DEST', 'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'FL_DATE']]
    flights.rename(columns={
        'DEPARTURE_DELAY': 'DEP_DELAY',
        'ARRIVAL_DELAY': 'ARR_DELAY'
    }, inplace=True)

    return flights

def average_arrival_delay_per_airline():
    """Get the average arrival delay per airline"""

    cache_key = "avg_arr_delay_airline"

    # Check Redis cache
    cached_result = get_from_cache(cache_key)
    if cached_result:
        logging.info("Result retrieved from Redis ✅")
        return cached_result

    # If not found in cache, read from CSV and compute
    logging.info("Cache empty → Computing from CSV ⏳")
    start = time.time()

    df = prepare_dataframe()
    result = df.groupby("OP_CARRIER")["ARR_DELAY"].mean().to_dict()

    elapsed = time.time() - start
    logging.info(f"Computation finished in {elapsed:.2f} seconds")

    # Cache the result
    set_to_cache(cache_key, result, ttl=CACHE_TTL)
    logging.info("Result stored in Redis ✅")
    return result

if __name__ == "__main__":
    result = average_arrival_delay_per_airline()
    print(result)