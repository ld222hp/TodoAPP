import mysql.connector
from mysql.connector import errorcode
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="todouser",
    password="NewPassword",
    database = "todo_db"
)

cursor = mydb.cursor()

def welcomeRoutine():
    print("Welcome to your TODO app.")
    print("Do you want to:")
    print("[1] View tasks")
    print("[2] View category")
    print("[3] Create category")
    print("[4] Create task")
    print("[5] Delete task")
    print("[6] Delete category")
    print("[7] Count tasks")
    print("[8] Get priority tasks over 5 prio")


    action = 0
    while action > 8 or action <= 0:
        action = int(input("Choose your action:"))
    return action

action = welcomeRoutine()

def createCategory():
    categoryName = input("Enter new category name:")
    insert_newCategory = "INSERT INTO category (name) VALUES ('"+categoryName+"')"
    cursor.execute(insert_newCategory)
    mydb.commit()

def createTask():
    cursor.execute("SELECT * FROM category")
    myresult = cursor.fetchall()
    for row in myresult:
        print(str(row[0]) + " | " + row[1] )
    
    categoryId = input("Choose category to create a task in:")
    taskDescription = input("Enter new task:")
    taskPriority = input("Enter task priority:")

    insert_newTask = "INSERT INTO task (description, priority, category_id) VALUES (%s, %s, %s)"
    cursor.execute(insert_newTask, (taskDescription, taskPriority, categoryId))
    mydb.commit()

def viewTasks():
    cursor.execute("SELECT description, priority, category.name FROM task JOIN category on category.id = task.category_id")

    myresult = cursor.fetchall()
    for row in myresult:
        print("Category: " + str(row[2]) + " | Task: " + row[0] + " | Priority: " + str(row[1]))

def viewCategory():
    cursor.execute("SELECT name FROM category")
    myresult = cursor.fetchall()
    for row in myresult:
        print(str(row[0]))

def countTasks():
    cursor.execute("select category.name, count(task.id) as countTasks from category join task on task.category_id = category.id group by category.name order by countTasks DESC;")
    myresult = cursor.fetchall()
    for row in myresult:
        print(row[0] + " | Tasks: " + str(row[1]))

def deleteTask():
    cursor.execute("SELECT * FROM task")
    myresult = cursor.fetchall()
    for row in myresult:
        print("ID: " + str(row[0]) + " | Task: " + row[1] + " | Priority: " + str(row[2]))

    taskID = input("Task ID to be removed:")
    delete_task = "DELETE FROM task WHERE id=('"+taskID+"')"
    cursor.execute(delete_task)
    mydb.commit()

def deleteCategory():

    cursor.execute("SELECT * FROM category")
    myresult = cursor.fetchall()
    for row in myresult:
        print("ID: " + str(row[0]) + " | Task: " + row[1])

    categoryID = input("Category ID to be removed:")
    delete_tasks = "DELETE FROM task WHERE category_id=('"+categoryID+"')"
    delete_category = "DELETE FROM category WHERE id=('"+categoryID+"')"

    cursor.execute(delete_tasks)
    cursor.execute(delete_category)
    mydb.commit()

def getHighestPriorityTasks():
    cursor.execute("SELECT * FROM prioView order by prioview.priority DESC;")
    myresult = cursor.fetchall()
    for row in myresult:
        print("Prio: " +str(row[1])  + "| " + row[0])

if action == 1:
    viewTasks()
elif action == 2:
    viewCategory()
elif action == 3:
    createCategory()
elif action == 4:
    createTask()
elif action == 5:
    deleteTask()
elif action == 6:
    deleteCategory()
elif action == 7:
    countTasks()
elif action == 8:
    getHighestPriorityTasks()
