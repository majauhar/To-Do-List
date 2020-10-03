# just a comment
# just another comment
import db
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=db.engine)
session = Session()


def todays_tasks():
    today = db.datetime.today()
    print("Today", today.day, today.strftime('%b'), ':')
    tasks = session.query(db.Task).filter(db.Task.deadline == today.date()).all()
    if len(tasks) == 0:
        print("Nothing to do")
        return
    else:
        i = 1
        for task in tasks:
            print(str(i) + '.', task)
            i += 1
        return
def weeks_tasks():
    today = db.datetime.today()
    # a_week = today + db.timedelta(days=6)

    for i in range(7):
        this_day = today + db.timedelta(days=i)
        print()
        print(this_day.strftime('%A'), this_day.day, this_day.strftime('%b'))
        tasks = session.query(db.Task).filter(db.Task.deadline == this_day.date()).all()
        # print(tasks)
        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            i = 1
            for task in tasks:
                # if task.dead_line() == this_day.date():
                print(str(i) + '.', task)
                i += 1


def all_tasks():
    print('All tasks:')
    tasks = session.query(db.Task).order_by(db.Task.deadline).all()
    if len(tasks) == 0:
        print('No task to do')
        return
    else:
        i = 1
        for task in tasks:
            print(str(i) + '. ', task, '. ', task.dead_line().day, ' ', task.dead_line().strftime('%b'), sep='')
            i += 1
    return

def add_task():
    new_task = input('Enter task\n')
    deadline = input('Enter deadline\n')
    deadline = [int(x) for x in deadline.split('-')]
    deadline = db.datetime(deadline[0], deadline[1], deadline[2])
    new_task = db.Task(task=new_task, deadline=deadline)
    session.add(new_task)
    session.commit()

def missed_tasks():
    today = db.datetime.today().date()
    tasks = session.query(db.Task).filter(db.Task.deadline < today).order_by(db.Task.deadline).all()
    if len(tasks) == 0:
        print('No missed tasks!')
    else:
        i = 1
        for task in tasks:
            print(str(i) + '. ', task, '. ', task.dead_line().day, ' ', task.dead_line().strftime('%b'), sep='')
            i += 1
    print()

def delete_task():
    tasks = session.query(db.Task).order_by(db.Task.deadline).all()
    if len(tasks) == 0:
        print('Nothing to delete!')
    else:
        i = 1
        print('Choose the number of the task you want to delete:')
        for task in tasks:
            print(str(i) + '. ', task, '. ', task.dead_line().day, ' ', task.dead_line().strftime('%b'), sep='')
            i += 1
        task_number = int(input())
        # task_to_be_deleted = tasks[task_number-1]
        session.delete(tasks[task_number-1])
        session.commit()


while True:
    print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
    option = int(input())
    if option == 0:
        print('Bye!')
        break
    if option == 1:
        todays_tasks()
    if option == 2:
        weeks_tasks()
    if option == 3:
        all_tasks()
    if option == 4:
        missed_tasks()
    if option == 5:
        add_task()
    if option == 6:
        delete_task()

