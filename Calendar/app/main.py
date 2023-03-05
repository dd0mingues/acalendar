import calendar
import datetime
import os
import sqlite3
import argparse
from database import database

def main():
    db_path = 'exercice.db'
    db = database(db_path)
    
    parser = argparse.ArgumentParser(description='Exercise tracker CLI')
    
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('streak', help='Get current exercise streak')
    
    log_parser = subparsers.add_parser('log', help='Log exercise for today')
    log_parser.add_argument('--date', help='Log exercise for a specific date (YYYY-MM-DD format)')
    
    args = parser.parse_args()
    
    # process the command
    if args.command == 'streak':
        streak = db.get_streak()
        print(f"Current exercise streak: {streak}")
    elif args.command == 'log':
        if args.date is not None:
            try:
                date = datetime.datetime.strptime(args.date, '%Y-%m-%d').date()
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return
        else:
            date = datetime.date.today()
        db.log_exercise()
        streak = db.get_streak()
        print(f"Current exercise streak: {streak}")
    # close the database connection
    del db

if __name__ == '__main__':
    main()