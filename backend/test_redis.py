import redis

try:
    r = redis.Redis(host='localhost', port=6379, db=0)
    response = r.ping()
    if response:
        print("Successfully connected to Redis!")
    else:
        print("Failed to connect to Redis.")
except Exception as e:
    print(f"Error connecting to Redis: {e}")