import sqlite3

conn = sqlite3.connect("data.db")


def test_tables_in_database():
    c = conn.cursor()
    c.execute("select * from SQLite_master")

    tables = c.fetchall()

    for table in tables:
        print("Table Name: %s" % (table[2]))
        table_name = table[2]
        print(len(tables), len(set(tables)))
        assert table_name == 'emp_data' or 'student_data'
        assert table_name == 'student_data' or 'emp_data'
        assert len(tables) == len(set(tables))
        assert len(tables) > 1
    conn.close()



