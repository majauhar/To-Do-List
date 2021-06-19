import db # db.py contains the codes dealing with database,schema, and datetime
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=db.engine)
session = Session()


def todays_tasks():
    # Shows tasks with today's deadline
    today = db.datetime.today()
    print("Today", today.day, today.strftime('%b'), ':')
    tasks = session.query(db.Task).filter(db.Task.deadline == today.date()).all()

    if len(tasks) == 0:
        print("Nothing to do")
    else:
        i = 1
        for task in tasks:
            print(str(i) + '.', task)
            i += 1


def weeks_tasks():
    ''' Shows tasks with deadlines in the coming week.
    
    Coming week means the next 7 days, excluding the current day
    '''
    today = db.datetime.today()

    for i in range(7):
        this_day = today + db.timedelta(days=i)
        print()
        print(this_day.strftime('%A'), this_day.day, this_day.strftime('%b'))
        tasks = session.query(db.Task).filter(db.Task.deadline == this_day.date()).all()

        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            i = 1
            for task in tasks:
                print(str(i) + '.', task)
                i += 1


def all_tasks():
    # Shows all the tasks present in the database
    print('All tasks:')
    tasks = session.query(db.Task).order_by(db.Task.deadline).all()

    if len(tasks) == 0:
        print('No task to do')
    else:
        i = 1
        for task in tasks:
            print(str(i) + '. ', task, '. ', task.dead_line().day, ' ', task.dead_line().strftime('%b'), sep='')
            i += 1


def add_task():
    '''Adds a new task with a task name, and the corresponding deadline.
    Deadline should be in YYYY-MM-DD format
    '''
    new_task = input('Enter task\n')
    deadline = input('Enter deadline\n')
    deadline = [int(x) for x in deadline.split('-')]
    deadline = db.datetime(deadline[0], deadline[1], deadline[2])

    new_task = db.Task(task=new_task, deadline=deadline)
    
    session.add(new_task)
    session.commit()


def missed_tasks():
    # Shows the tasks whose deadlines lie before the current (today's) date
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
    '''Deletes a specified task by its index.
    First, all the tasks present in the database are printed with index from [1, 2, ..., n]
    Then, the indexed entry is removed from the database permanently
    '''
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

        session.delete(tasks[task_number-1])
        session.commit()


while True:
    # MENU
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

