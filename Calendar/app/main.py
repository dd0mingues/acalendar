import calendar
import datetime
import os
import sqlite3
from database import database


def main():
    db = database('exercice.db')
    db.log_exercise()
    streak = db.get_streak()
    del db
    
    print(streak)


if __name__ == '__main__':
    main()