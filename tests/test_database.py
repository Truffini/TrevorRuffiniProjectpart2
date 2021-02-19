import sqlite3
from typing import Tuple
import APImain


def open_db(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS school_data
                               (
                                   school_name text,
                                   school_city text,
                                   student_size_2017 real,
                                   student_size_2018 real,
                                   earnings_3_yrs_after_completion_overall_count_over_poverty_line_2017 real,
                                   repayment_3_yr_repayment_overall_2016 real
                               )'''
                   )


def add_new_school(cursor: sqlite3.Cursor):
    cursor.execute(f'''INSERT INTO SCHOOL_DATA (school_name, school_city, student_size_2017, student_size_2018, 
    earnings_3_yrs_after_completion_overall_count_over_poverty_line_2017, repayment_3_yr_repayment_overall_2016)
            VALUES('BSU', 'Braintree', 1, 2, 3, 4)
            ''')


def test_get_data2(cursor):
    APImain.main()
    add_new_school(cursor)


def main():
    conn, cursor = open_db("data.db")
    setup_db(cursor)
    test_get_data2(cursor)
    close_db(conn)


if __name__ == '__main__':
    main()
