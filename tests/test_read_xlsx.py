from pandas import read_excel

sheet_name1 = 'State_M2019_dl'
file_name1 = 'state_M2019_dl.xlsx'


def test_get_xlsx_data():
    all_data = []
    df = read_excel(file_name1, sheet_name=sheet_name1, engine='openpyxl')
    total_fetch_result = 0
    for index, row in df.iterrows():
        if row['o_group'] == 'major':
            item_data = (row['area_title'])
            total_fetch_result += 1
            all_data.append(item_data)
    assert (len(list(set(all_data))) >= 50)
    print(list(set(all_data)))


def test_get_xlsx_data2():
    all_data2 = []
    df = read_excel(file_name1, sheet_name=sheet_name1, engine='openpyxl')
    total_fetch_result = 0
    for index, row in df.iterrows():
        if row['o_group'] == 'major':
            item_data = (row['occ_title'])
            total_fetch_result += 1
            all_data2.append(item_data)
    assert (len(list(set(all_data2))) >= 22)
    print(list(set(all_data2)))
