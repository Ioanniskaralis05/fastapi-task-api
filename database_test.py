import sqlite3

connection = sqlite3.connect("tasks.db")
cursor = connection.cursor()

# UPDATE task
cursor.execute("""
UPDATE tasks
SET title = ?
WHERE id = ?
""", ("Study FastAPI", 1))

connection.commit()

# DELETE task
cursor.execute("""
DELETE FROM tasks
WHERE id = ?
""", (1,))

connection.commit()

# SHOW remaining tasks
cursor.execute("SELECT * FROM tasks")
tasks = cursor.fetchall()

print(tasks)

connection.close()