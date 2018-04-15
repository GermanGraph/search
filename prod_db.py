import playhouse.postgres_ext as peewee

db = peewee.PostgresqlExtDatabase(
    database='postgres',
    host='85.143.174.69',
    port=15432,
    user='postgres',
    password='postgres123456',
    autorollback=True,
    register_hstore=True
)
