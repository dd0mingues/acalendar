import calendar
import datetime
import sqlite3
from Calendar.app.database import database, loadDatabase


def main():
    db = database('exercice.db')
    db.log_exercise()
    streak = db.get_streak()


if __name__ == '__main__':
    main()