import config
import psycopg2

db = psycopg2.connect(
    host=config.POSTGRESQL_HOST,
    user=config.POSTGRESQL_USER,
    password=config.POSTGRESQL_PASSWORD,
    database=config.POSTGRESQL_DATABASE,
    port=config.POSTGRESQL_HOST
)

