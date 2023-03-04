import calendar
import datetime
import sqlite3

def main():
    conn = sqlite3.connect('exercise.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS exercice
              (date TEXT, exercice_done INTEGER)''')
    conn.commit()
    conn.close()
    


if __name__ == '__main__':
    main()