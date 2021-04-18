import requests


headers = {
    'Origin': 'application/json',
    'Sec-Fetch-Site': 'same-site',
    'Referer': 'https://icdcodelookup.com/'
}


def get_icd_codes(term):
    data = '{"terms":"' + term + '"}'
    response = requests.post('https://s.icdcodelookup.com/lookUp/search', headers=headers, data=data)
    data = response.json()['results']

    result = {}

    for i in range(len(data)):
        result[data[i]['name']] = data[i]['desc']

    print(result)
    return result
