import sqlite3
from pandas import read_excel

conn = sqlite3.connect("data.db")

sheet_name1 = 'State_M2019_dl'
file_name1 = 'state_M2019_dl.xlsx'


def _read_excel(sheet_name, file_name):
    all_data = []
    data_file = read_excel(file_name, sheet_name=sheet_name, engine='openpyxl')
    total_fetch_result = 0
    for index, row in data_file.iterrows():
        if row['o_group'] == 'major':
            print(row['area_title'], row['occ_title'], row['tot_emp'], row['h_pct25'], row['a_pct25'])
            item_data = (row['area_title'], row['occ_title'], row['tot_emp'], row['h_pct25'], row['a_pct25'])
            total_fetch_result += 1
            all_data.append(item_data)
    print(total_fetch_result, " ITEMS")
    return all_data


def add_to_database(all_data):
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS emp_data;''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS emp_data
                            (
                                state,
                                occupation_major_title,
                                total_employment,
                                h_percentile_salary_25,
                                a_percent_salary_25
                            )'''
              )
    cursor.executemany('INSERT INTO emp_data VALUES (?,?,?,?,?)', all_data)
    conn.commit()


def main():
    all_data = _read_excel(sheet_name1, file_name1)
    add_to_database(all_data)


if __name__ == '__main__':
    main()
