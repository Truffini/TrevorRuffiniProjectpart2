import sqlite3
import math
import requests
import secrets

url = (f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded"
       f".predominant=2,3&fields=school.name,school.city,2018.student.size,2017.student.size,"
       f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
       f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}")

fields = ",".join([
    "school.name",
    "school.city",
    "school.state",
    "2018.student.size",
    "2017.student.size",
    "2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line",
    "2016.repayment.3_yr_repayment.overall",
    "2016.repayment.repayment_cohort.3_year_declining_balance"
])

conn = sqlite3.connect("data.db")


def get_data():
    all_data = []
    response = requests.get(f"{url}&fields={fields}&per_page={100}")

    page_of_data = response.json()
    if response.status_code != 200:
        print(response.reason)
        print(page_of_data)
    total_res = page_of_data['metadata']['total']
    items_per_page = page_of_data['metadata']['per_page']

    total_pages = math.ceil(total_res / items_per_page)
    total_fetch_result = 0
    for page in range(0, total_pages):
        response = requests.get(f"{url}&fields={fields}&api_key={secrets}&page={page}&per_page={100}")
        if response.status_code != 200:
            print("Error with data syncing process")
            exit(-1)

        page_of_data = response.json()
        result = page_of_data['results']
        print(f"Syncing Page {page + 1:02} of {total_pages} | {len(result):03} Data Items ")
        for item in page_of_data['results']:
            item_data = (
                item["school.name"],
                item["school.city"],
                item["school.state"],
                item["2017.student.size"],
                item["2018.student.size"],
                item["2016.repayment.3_yr_repayment.overall"],
                item["2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line"],
                item["2016.repayment.repayment_cohort.3_year_declining_balance"]
            )
            total_fetch_result += 1
            all_data.append(item_data)
    print("fetched items: ", total_fetch_result)
    return all_data


# create tables - may not need all_data
def add_to_database():
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE IF EXISTS school_data;''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS school_data
                            (
                                school_name text,
                                school_city text,
                                school_state text,
                                student_size_2017 real,
                                student_size_2018 real,
                                earnings_3_yrs_after_completion_overall_count_over_poverty_line_2017 real,
                                repayment_3_yr_repayment_overall_2016 real,
                                repayment_repayment_cohort_3_year_declining_balance_2016 real
                            )'''
              )


def save_data(all_data):
    cursor = conn.cursor()
    cursor.executemany('INSERT INTO school_data VALUES (?,?,?,?,?,?,?,?)', all_data)
    conn.commit()


def main():
    all_data = get_data()
    add_to_database()
    save_data(all_data)


if __name__ == '__main__':
    main()
