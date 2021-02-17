import APImain


def test_get_data():
    results = APImain.get_data()
    assert len(results) == 3203