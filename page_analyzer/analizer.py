import requests


def analiz_url(url):
    resp = requests.get(url)
    check_dict = {}
    check_dict['status_code'] = resp.status_code
    return check_dict
