from bs4 import BeautifulSoup
import requests


def analiz_url(url):
    resp = requests.get(url)
    bs = BeautifulSoup(resp.text, 'html.parser')
    check_dict = {}
    check_dict['status_code'] = resp.status_code
    check_dict['h1'] = find_h(bs)
    check_dict['title'] = find_title(bs)
    check_dict['description'] = find_meta(bs)
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
