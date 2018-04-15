import playhouse.postgres_ext as peewee

db = peewee.PostgresqlExtDatabase(
    database='postgres',
    host='localhost',
    port=5432,
    user='postgres',
    password='postgres123456',
    autorollback=True,
    register_hstore=True
)
