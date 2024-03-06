from bs4 import BeautifulSoup
import requests


def analiz_url(url):
    resp = requests.get(url)
    resp.raise_for_status()
    status_code = resp.status_code
    bs = BeautifulSoup(resp.text, 'html.parser')
    return get_analize(bs, status_code)


def get_analize(text, status):
    check_dict = {}
    check_dict['status_code'] = status
    check_dict['h1'] = find_h(text)
    check_dict['title'] = find_title(text)
    check_dict['description'] = find_meta(text)
    return check_dict


def find_h(bs):
    h = bs.h1
    if h:
        return h.string
    return ''


def find_title(bs):
    title = bs.title
    if title:
        return title.string
    return ''


def find_meta(bs):
    meta = bs.select('meta[name="description"]')
    if not meta:
        return ""
    attributes = meta[0].attrs
    content = attributes.get('content')
    if not content:
        return ""
    return content
