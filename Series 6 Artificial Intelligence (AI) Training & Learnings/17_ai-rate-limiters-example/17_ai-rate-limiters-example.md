# Project 17: AI Rate Limiters Example
# ------------------------------------
# ------------------------------------
# Folder:
17_ai-rate-limiters-example

🧠 Concept
A rate limiter controls how many requests can be made within a certain time window — for example, “5 requests per 10 seconds.” If the limit is reached, the client must wait before sending more.

⚙️ How it Works
The program allows 5 requests every 10 seconds.
Each request is timestamped and stored in a queue.

When a new request comes in:
Old timestamps outside the 10-second window are removed.
If fewer than 5 timestamps remain, the request is allowed.
Otherwise, it’s blocked.

# Install venv
python3 -m venv .venv
source .venv/bin/activate

# Installations
pip install --upgrade pip
pip install python-dotenv openai
pip install langchain langchain-openai langchain-experimental

# To run example 1 (Simple example of Rate Limiter):
python3 1_basic_example.py

# Example output:
Request 1 allowed ✅
Request 2 allowed ✅
Request 3 allowed ✅
Request 4 allowed ✅
Request 5 allowed ✅
Request 6 blocked 🚫 (Rate limit exceeded)
Request 7 blocked 🚫 (Rate limit exceeded)
Request 8 blocked 🚫 (Rate limit exceeded)
Request 9 blocked 🚫 (Rate limit exceeded)
Request 10 blocked 🚫 (Rate limit exceeded)

# To run example 2 (Per User)
python3 2_per_user_example.py

# Example output:
--- Attempt 1 ---
[alice] Request allowed ✅ (1/3 used)
[bob] Request allowed ✅ (1/3 used)

--- Attempt 2 ---
[alice] Request allowed ✅ (2/3 used)
[bob] Request allowed ✅ (2/3 used)

--- Attempt 3 ---
[alice] Request allowed ✅ (3/3 used)
[bob] Request allowed ✅ (3/3 used)

--- Attempt 4 ---
[alice] Request blocked 🚫 (Rate limit exceeded)
[bob] Request blocked 🚫 (Rate limit exceeded)

--- Attempt 5 ---
[alice] Request blocked 🚫 (Rate limit exceeded)
[bob] Request blocked 🚫 (Rate limit exceeded)

# NOTE: To run redis in docker
cd /Users/gjohnson/Downloads/17_ai-rate-limiters-example
docker run --name redis-demo -p 6379:6379 -d redis

Stop the container using:
docker stop redis-demo

# To run example 3 (Using Redis)
🧪 Option A: Sliding-window limiter with Redis (simple & effective)
pip install redis

python3 3_redis_sliding_window_limiter.py

It uses a sliding window per user (accurate and smooth), implemented with a Redis sorted set.

# How it works
Each user has a Redis ZSET whose scores and members are timestamps (ms).
For a new request:
ZADD the current timestamp
ZREMRANGEBYSCORE to remove entries older than now - window
ZCARD to see how many are in-window
If count > max_requests, we remove the inserted timestamp and deny.
This is accurate (true sliding window) and fast. It works across many app servers because Redis is shared.

⚡ Option B: Fixed-window counter (simpler, burstier)
This is the classic “N per window” approach with INCR and EXPIRE. It’s dead simple, but resets on window boundaries (can allow short bursts at edges).

# To run example 4 (Using Redis Fixed Window)
python3 4_redis_fixed_window_counter.py

🧰 Production tips
Atomicity: The sliding-window pipeline above is usually fine. For the strictest atomicity under extreme concurrency, use a Lua script so all steps happen server-side in a single operation.
Dimensions: Limit by user, API key, IP, and resource (e.g., user + model_name).
Backoff headers: Return helpful metadata (e.g., Retry-After) so clients know when to try again.
Metrics: Emit counters (allowed/blocked) and latencies. Alarms on sustained block rates.
Redis hygiene: Namespaces, expirations, and periodic scans (if needed) to keep memory tidy.