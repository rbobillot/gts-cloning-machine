from urllib import urlencode
import urllib2
import json

def http_post(url, post_data, json=False):
    if (json):
        headers = {'Content-Type': 'application/json'}
    else:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    req = urllib2.Request(url, post_data, headers)
    response = urllib2.urlopen(req)
    content = response.read()
    response.close()
    return content

def notify_gts_service(notify_category, status, gts_service_url):
    try:
        http_post(
            url=gts_service_url,
            post_data=status,
            json=True)
    except Exception as e:
        print('Failed to notify "%s". Error: %s' % (notify_category, e))