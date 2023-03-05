import os
import sqlite3
import datetime

class database:
    def __init__(self, db_name):
        self.db_name =  os.getcwd() + '/calendar/data/' + db_name
        self.conn = sqlite3.connect(self.db_name)
        self.create_table()

    def create_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS exercise
                    (date TEXT, exercise_done INTEGER)''')
        self.conn.commit()

    def log_exercise(self):
        today = datetime.date.today().strftime("%Y-%m-%d")
        c = self.conn.cursor()
        c.execute("INSERT INTO exercise (date, exercise_done) VALUES (?,?)", (today, 1))
        self.conn.commit()

    def get_streak(self):
        c = self.conn.cursor()
        c.execute("SELECT date FROM exercise ORDER BY date DESC")
        rows = c.fetchall()
        streak = 0
        for i in range(len(rows)-1):
            current = datetime.datetime.strptime(rows[i][0], '%Y-%m-%d').date()
            prev = datetime.datetime.strptime(rows[i+1][0], '%Y-%m-%d').date()
            if (current - prev).days == 1:
                streak += 1
            else:
                break
        return streak+1

    def __del__(self):
        self.conn.close()
