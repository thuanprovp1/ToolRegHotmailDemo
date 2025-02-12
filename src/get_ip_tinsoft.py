import random
import time

import requests


def get_new_ip_tinsoft(api_key):
    location_ip = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    url = f'http://proxy.tinsoftsv.com/api/changeProxy.php?key={api_key}&location={random.choice(location_ip)}'
    # print(url)
    try:
        re = requests.get(url, timeout=10)
        proxy = check_status(re)
        write_new_proxy(proxy)
        return proxy
    except Exception as e:
        time.sleep(12)
        return False


def check_status(response):
    if response.json()['success'] == True:
        return response.json()['proxy']
    elif response.json()['success'] == False:
        with open("tinsoft_proxy.txt", 'r') as f:
            firstline = f.readline().rstrip()
        return firstline
    else:
        raise Exception('loi ip tinsoft')


def write_new_proxy(proxy):
    with open('tinsoft_proxy.txt', 'w') as file_output:
        file_output.write(proxy + '\n')


# print(get_new_ip_tinsoft('TLUJwPCh19gFMiLYKRLlMCtJ2OZxma8Sglx5om'))
# write_new_proxy('2343')
