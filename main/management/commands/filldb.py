import sqlite3
import os
from Versionize.settings import BASE_DIR
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Заполнение базы данных'

    def handle(self, *args, **options):

        conn = sqlite3.connect(os.path.join(settings.BASE_DIR, 'db.sqlite3'))
        file_path = os.path.join(settings.BASE_DIR, 'main/management/commands/versionize_inserts.sql')
        cursor = conn.cursor()
        with open(file_path) as file:
            for sql_command in file.readlines():
                cursor.execute(f'{sql_command}')
                conn.commit()


if __name__ == "__main__":
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'db.sqlite3'))
    cursor = conn.cursor()

    with open('versionize_inserts.sql', 'r', encoding='utf-8') as file:
        for sql_command in file.readlines():
            cursor.execute(f'{sql_command}')
            conn.commit()
