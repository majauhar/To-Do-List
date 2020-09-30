from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task + str(self.deadline)
    def __str__(self):
        return self.task
    def dead_line(self):
        return self.deadline


Base.metadata.create_all(engine)
