import APImain
import secrets
import requests


def test_data_items():
    response = requests.get(f"https://api.data.gov/ed/collegescorecard/v1/schools.json?school.degrees_awarded"
                            f".predominant=2,3&fields=school.name,school.city,2018.student.size,2017.student.size,"
                            f"2017.earnings.3_yrs_after_completion.overall_count_over_poverty_line,"
                            f"2016.repayment.3_yr_repayment.overall&api_key={secrets.api_key}")
    page_of_data = response.json()
    total_res = page_of_data['metadata']['total']
    items = total_res
    assert items > 1000
    assert items == 3203


def test_get_data():
    results = APImain.get_data()
    assert len(results) > 1000
