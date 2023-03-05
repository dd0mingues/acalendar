import os
import sqlite3
import datetime
from datetime import datetime, timedelta

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
        
    def get_all_exercises(self):
        query = "SELECT * FROM exercise;"
        cursor = self.conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        return data

    def log_exercise(self):
        today = datetime.today().strftime("%Y-%m-%d")
        exercise_done = input("Did you exercise today? (y/n): ")
        if exercise_done.lower() == "y":
            c = self.conn.cursor()
            c.execute("INSERT INTO exercise VALUES (?, 1)", (today,))
            self.conn.commit()
            print("Exercise logged for", today)

    def get_streak(self):
        c = self.conn.cursor()
        c.execute("SELECT date FROM exercise ORDER BY date DESC")
        rows = c.fetchall()
        streak = 0
        for i in range(len(rows)-1):
            current = datetime.strptime(rows[i][0], '%Y-%m-%d').date()
            prev = datetime.strptime(rows[i+1][0], '%Y-%m-%d').date()
            if (current - prev).days == 1:
                streak += 1
            else:
                break
        
        print(f"Current exercise streak: {streak+1}")
        return streak+1
    
    def view_calendar(self, year=None, month=None):
        """Print a calendar month with the days exercised highlighted."""
        today = datetime.today()
        if year is None:
            year = today.year
        if month is None:
            month = today.month

        # Compute the first day and the number of days in the month
        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)

        # Query the database for exercises within the specified month
        c = self.conn.cursor()
        c.execute("SELECT date FROM exercise WHERE date >= ? AND date <= ?", (first_day.date(), last_day.date()))
        exercises = c.fetchall()

        # Compute the days exercised in the month
        days_exercised = set()
        for exercise in exercises:
            days_exercised.add(datetime.strptime(exercise[0], "%Y-%m-%d").day)

        # Print the calendar month
        print(first_day.strftime("%B %Y"))
        print("Mo Tu We Th Fr Sa Su")
        for day in range(1, last_day.day + 1):
            if day in days_exercised:
                print("\033[32m{:2d}\033[0m".format(day), end=" ")
            else:
                print("{:2d}".format(day), end=" ")
            if (first_day + timedelta(days=day - 1)).weekday() == 6:
                print()
        print()


    def __del__(self):
        self.conn.close()
