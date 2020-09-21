import sqlite3
import random
import string



# SQLite execution
def sql_execute(sql):
    connection = sqlite3.connect('db.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    ret = cursor.execute(sql)
    connection.commit()
    #connection.close()
    return ret


# Session ID: Generates random string with the combination of lower and upper case, length 32
def get_random_string(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str