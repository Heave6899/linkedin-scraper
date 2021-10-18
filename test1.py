import requests
#!/usr/bin/env python
import sys
import json

jsonString = ''

import urllib.request
opener = urllib.request.build_opener(
    urllib.request.ProxyHandler({'http': 'http://lum-customer-c_3b483b89-zone-residentialrotator:maau0b8jhjrq@zproxy.lum-superproxy.io:22225',
        'https': 'http://lum-customer-c_3b483b89-zone-residentialrotator:maau0b8jhjrq@zproxy.lum-superproxy.io:22225'}))
print(opener.open('http://lumtest.com/myip.json').read())
print(opener.open('https://www.linkedin.com').read())

# print(jsonString)
# print(jsonString['ip'])

# url = "https://www.linkedin.com/company/k7-music"
urls = ['https://www.linkedin.com/company/-pet-hoogeveen/','https://www.linkedin.com/company/k7-music',
        'https://www.linkedin.com/company/kawasaki-kinkai-kisen-kaisha-ltd/','https://www.linkedin.com/company/kp-vti-edaps-consortium/','https://www.linkedin.com/company/hash2/']

proxies = {
  # "https": "https://{0}:8080".format(jsonString['ip']),
  # "https": "https://83.229.8.9:3127"
}


for url in urls:
    print(url)
    payload={}
    headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-encoding': 'gzip, deflate, br',
      'accept-language': 'en-US,en;q=0.9',
      'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'none',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    }

    response = requests.get(url, headers=headers, data=payload, proxies=proxies)
    print(response.status_code)
    # if response.status_code == 200:
      # print(response.content)
    # assert response.status_code == 200
      # print('=='*50)
