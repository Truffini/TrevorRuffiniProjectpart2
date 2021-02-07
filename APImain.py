import secrets
import requests
import math


def get_data():
    all_data = []
    response1 = requests.get(f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded"
                             f".predominant=2,3&fields=school.name,school.city,2018.student.size,2017.student.size,"
                             f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                             f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}")
    page_of_data = response1.json()
    total_res = page_of_data['metadata']['total']
    items_per_page = page_of_data['metadata']['per_page']
    print(page_of_data['metadata'])
    for page in range(0, (math.floor(total_res / items_per_page) + 1)):
        response = requests.get(f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded"
                                f".predominant=2,3&fields=school.name,school.city,2018.student.size,"
                                f"2017.student.size,"
                                f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                                f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}&page={page}")
        if response.status_code != 200:
            print("error with data")
            exit(-1)
        page_of_data = response.json()
        page_of_school_data = page_of_data['results']
        all_data.extend(page_of_school_data)
        filename = open('Data.txt', 'a')
        print(page_of_data, file=filename)


def main():
    get_data()
    print(get_data)


if __name__ == '__main__':
    main()
