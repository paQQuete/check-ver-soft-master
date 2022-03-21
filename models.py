from peewee import *

user = '*'
password = '*'
db_name = '*'

dbhandle = MySQLDatabase(
    db_name, user=user,
    password=password,
    host='localhost'
)


class BaseModel(Model):
    class Meta:
        database = dbhandle


class PSQuery(BaseModel):
    id = PrimaryKeyField(null=False)
    username = CharField(null=True)
    hostname = CharField(null=False)
    unixtime_query = TimestampField(null=False)
    normaltime_query = DateTimeField(null=False)
    publisher = CharField(null=False)
    displayname = CharField(null=False)
    displayversion = CharField(null=False)
    displaversionFloat = FloatField(null=False)
    installdate = DateTimeField(null=True)
