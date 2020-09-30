# Write your code here
import db
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db.engine)
session = Session()


def todays_tasks():
    print("Today:")
    tasks = session.query(db.Task).all()
    if len(tasks) == 0:
        print("Nothing to do")
        return
    else:
        i = 1
        for task in tasks:
            print(str(i) + '.', task)
def add_task():
    new_task = input('Enter task\n')
    new_task = db.Task(task=new_task)
    session.add(new_task)
    session.commit()

while True:
    print('''1) Today's tasks
2) Add task
0) Exit''')
    option = int(input())
    if option == 0:
        break
    if option == 1:
        todays_tasks()
    if option ==2:
        add_task()

