from peewee import *
from flask_login import UserMixin
from datetime import datetime

db = SqliteDatabase('db.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class User(UserMixin, BaseModel):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    avatar = CharField(null=True)
    bio = TextField(default='')

    def get_id(self):
        return str(self.id)


class CodePost(BaseModel):
    title = CharField()
    description = TextField()
    code = TextField()
    image = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    user = ForeignKeyField(User, backref='posts')
class Comment(BaseModel):
    text = TextField()
    created_at = DateTimeField(default=datetime.now)

    user = ForeignKeyField(User, backref='comments')
    post = ForeignKeyField(CodePost, backref='comments')


db.connect()
db.create_tables([User, CodePost, Comment])