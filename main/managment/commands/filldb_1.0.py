import sqlite3
import os
from Versionize.settings import BASE_DIR


conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
cursor = conn.cursor()

with open('versionize_inserts.sql') as file:
    for sql_command in file.readlines():
        cursor.execute(f'{sql_command}')
        conn.commit()
