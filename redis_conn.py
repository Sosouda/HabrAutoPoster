

import os
from dotenv import load_dotenv
from redis import Redis

load_dotenv()

redis_conn = Redis(
    host=os.environ.get("REDIS_HOST", "localhost"),
    port=int(os.environ.get("REDIS_PORT", 6379)),
    password=os.environ["RPASSW"],
)
