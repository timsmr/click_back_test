import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Chat(ormar.Model):
    class Meta(BaseMeta):
        tablename = "chats"
    
    id: int = ormar.Integer(primary_key=True)
    question: str = ormar.String(max_length=1024, unique=False, nullable=False)
    answer1: str = ormar.String(max_length=1024, unique=False, nullable=False)
    answer2: str = ormar.String(max_length=1024, unique=False, nullable=False)
    answer3: str = ormar.String(max_length=1024, unique=False, nullable=False)
    real_answer: str = ormar.String(max_length=1024, unique=False, nullable=False)
    language: str = ormar.String(max_length=1024, unique=False, nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)