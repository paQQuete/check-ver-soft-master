from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase
import sensdata

dbhandle = PostgresqlExtDatabase(
    sensdata.db_name, user=sensdata.user,
    password=sensdata.password,
    host='localhost'
)


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Machine(BaseModel):
    id = PrimaryKeyField(null=False)
    username = CharField(null=True)
    hostname = CharField(null=False, unique=True)


class Row(BaseModel):
    machine = ForeignKeyField(Machine, related_name='on PC')
    unixtime_query = TimestampField(null=False)
    normaltime_query = DateTimeField(null=False)
    publisher = CharField(null=False)
    displayname = CharField(null=False)
    displayversion = CharField(null=False)
    displaversionFloat = FloatField(null=False)
    installdate = DateTimeField(null=True)


if __name__ == '__main__':
    dbhandle.connect()
    Machine.create_table()
    Row.create_table()
