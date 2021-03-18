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


def test_add_school():
    conn, cursor = open_db("test_data.db")
    APImain.add_to_database()
    cursor = conn.cursor()

    cursor.execute(f'''INSERT INTO school_data (school_name, school_city,school_state, student_size_2017, 
    student_size_2018,earnings_3_yrs_after_completion_overall_count_over_poverty_line_2017, 
    repayment_3_yr_repayment_overall_2016,repayment_repayment_cohort_3_year_declining_balance_2016)
    VALUES('BSU', 'Braintree', 'MA', 1, 2, 3, 4, 5)''')

    conn.commit()

    conn, cursor = open_db("test_data.db")
    cursor.execute('''SELECT name FROM sqlite_master
        WHERE type ='table' AND name LIKE 'school_%';''')
    results = cursor.fetchall()
    assert len(results) == 1
    cursor.execute(''' SELECT school_name FROM school_data''')
    results = cursor.fetchall()
    test_name = results[0]
    assert test_name[0] == 'BSU'
