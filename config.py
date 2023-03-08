import os

db_user = os.getenv("DB_USER", "default")
db_password = os.getenv("DB_PASSWORD", "default")
db_name = os.getenv("DB_NAME", "default")
db_host = os.getenv("DB_HOST", "default")
db_port = os.getenv("DB_PORT", "default")

db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}"

redis = os.getenv("REDIS", "default")

