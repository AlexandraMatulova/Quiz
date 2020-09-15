import sqlite3


# SQLite execution
def sql_execute(sql):
    connection = sqlite3.connect('db.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    ret = cursor.execute(sql)
    connection.commit()
    #connection.close()
    return ret