import sqlite3
import os
import re
from Versionize.settings import BASE_DIR

TABLE_NAME = 'main_standardsection'
pattern = r'(.*)\t(.*)'

conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
cursor = conn.cursor()
id_counter = 1

with open('area_obj_codes', 'r', encoding='utf-8') as area_obj:
    for line in area_obj.readlines():
        data = re.match(pattern, line)
        name = data.group(1)
        abbreviation = data.group(2)
        # project_type choices at main/models.py
        project_type = 1

        sql_command = f"INSERT INTO `{TABLE_NAME}` (`id`, `abbreviation`, `name`, `project_type`) VALUES " \
                      f"({id_counter}, '{abbreviation}', '{name}', {project_type});"

        cursor.execute(f'{sql_command}')
        conn.commit()
        id_counter += 1

with open('linear_obj_codes', 'r', encoding='utf-8') as linear_obj:
    for line in linear_obj.readlines():
        data = re.match(pattern, line)
        name = data.group(1)
        abbreviation = data.group(2)
        # project_type choices at main/models.py
        project_type = 2

        sql_command = f"INSERT INTO `{TABLE_NAME}` (`id`, `abbreviation`, `name`, `project_type`) VALUES " \
                      f"({id_counter}, '{abbreviation}', '{name}', {project_type});"

        cursor.execute(f'{sql_command}')
        conn.commit()
        id_counter += 1
