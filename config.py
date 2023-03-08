import os
import config_local

db_user = os.getenv("DB_USER", config_local.db_user)
db_password = os.getenv("DB_PASSWORD", config_local.db_password)
db_name = os.getenv("DB_NAME", config_local.db_name)
db_host = os.getenv("DB_HOST", config_local.db_host)
db_port = os.getenv("DB_PORT", config_local.db_port)

db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

redis = os.getenv("REDIS", config_local.redis)

