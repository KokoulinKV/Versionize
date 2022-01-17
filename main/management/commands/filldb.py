import sqlite3
import os
# from Versionize.settings import BASE_DIR
from django.core.management.base import BaseCommand
from django.conf import settings

# conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
# cursor = conn.cursor()

# with open('versionize_inserts_1.1.sql') as file:
#     for sql_command in file.readlines():
#         cursor.execute(f'{sql_command}')
#         conn.commit()


class Command(BaseCommand):
    help = 'Заполнение базы данных'

    def handle(self, *args, **options):

        conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'db.sqlite3'))
        file_path = os.path.join(settings.BASE_DIR, 'main/management/commands/versionize_inserts_1.1.sql')
        cursor = conn.cursor()
        with open(file_path) as file:
            for sql_command in file.readlines():
                cursor.execute(f'{sql_command}')
                conn.commit()