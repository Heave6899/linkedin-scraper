import sys
if sys.version_info[0]==2:
    import six
    from six.moves.urllib import request
    import random
    username = 'lum-customer-c_3b483b89-zone-residentialrotator'
    password = 'maau0b8jhjrq'
    port = 22225
    session_id = random.random()
    super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
        (username, session_id, password, port))
    proxy_handler = request.ProxyHandler({
        'http': super_proxy_url,
        'https': super_proxy_url,
    })
    opener = request.build_opener(proxy_handler)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
    print('Performing request')
    print(opener.open('http://lumtest.com/myip.json').read())
if sys.version_info[0]==3:
    import urllib.request
    import random
    def fn():
        username = 'lum-customer-c_3b483b89-zone-isp'
        password = 'j7ncpeqq3z22'
        port = 22225
        session_id = random.random()
        # super_proxy_url = ('http://%s-session-%s:%s@zproxy.lum-superproxy.io:%d' %
            # (username, session_id, password, port))
        super_proxy_url = 'http://127.0.0.1:24000'
        proxy_handler = urllib.request.ProxyHandler({
            'http': super_proxy_url,
            'https': super_proxy_url,
        })
        opener = urllib.request.build_opener(proxy_handler)
        # opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        print('Performing request')
        # print(opener.open('http://lumtest.com/myip.json').read())
        # print(opener.open('https://www.linkedin.com').read())
        print(opener.open('https://www.linkedin.com/company/amazon').read())

    fn()
    # e = Exception
    # while e == Exception :
    #     try: 
    #         fn()
    #         e = None
    #     except Exception as e:
    #         e = e 
        
    # try:
    # except Exception as e:
    #     pass
    # while True:
    #     try:
    #         print(opener.open('https://www.linkedin.com/company/bewustsociaalopweb/').read())
    #     except:
    #         pass