    # -*- coding: UTF-8 -*-
    
    """
    # get json done
    # may be the important js
    # https://web.umeng.com/static/js/traf/referrals.js?t=201603181110
    """
    import urllib
    import urllib2
    import cookielib
    import time
    
    
    # import pprint
    
    # 登录的主页面
    
    class CnzzCatch:
        is_login = False
    
        def __set_cookie(self):
            """add cookie listener"""
            cj = cookielib.LWPCookieJar()
            cookie_support = urllib2.HTTPCookieProcessor(cj)
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
    
        def __init__(self, site_id):
            """construct of logining to cnzz"""
            self.site_id = site_id
            self.__host_url = 'http://new.cnzz.com/v1/login.php?siteid=' + self.site_id
            self.__post_url = 'http://new.cnzz.com/v1/login.php?t=login&siteid=' + self.site_id
            self.password = '***' #your password here
            self.__set_cookie()
            self.__login()
    
        def __login(self):
            """login & catch"""
            if urllib2.urlopen(self.__host_url):
                print 'Open host success!'
            # headers
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                       'Referer': 'http://new.cnzz.com/v1/login.php?siteid=' + self.site_id,
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Language': 'en-US,en;q=0.7,zh;q=0.3',
                       'Accept-Encoding': 'zip, deflate',
                       'Connection': 'keep-alive',
                       'Content-Type': 'application/x-www-form-urlencoded',
                       'Content-Length': '15'
                       }
            # 构造Post数据。
            post_data = {'password': self.password}
    
            # 需要给Post数据编码
            post_data = urllib.urlencode(post_data)
    
            # 通过urllib2提供的request方法来向指定Url发送我们构造的数据，并完成登录过程
            request = urllib2.Request(self.__post_url, post_data, headers)
            response = None
            try:
                response = urllib2.urlopen(request)
            except urllib2.URLError as e:
                if hasattr(e, 'code'):
                    return 'LOGIN ERROR CODE', e.code
                elif hasattr(e, 'reason'):
                    return 'LOGIN ERROR REASON', e.reason
            finally:
                if response:
                    print 'Login finish!'
                    self.is_login = True
    
        def get_data(self, current_page, page_num, start_date, end_date=time.strftime("%Y-%m-%d", time.localtime())):
            """get summary json data"""
            print 'Getting data...'
            if self.is_login:
                data_url = 'https://web.umeng.com/main.php?c=traf&a=domain&ajax=module=summary|module=inputList|module=innerList|module=refererDomainList_orderBy=pv_orderType=-1_currentPage=%d_pageType=%d&siteid=%s&st=%s&et=%s&domainCondType=&itemName=&itemNameType=&itemVal=&siteType=' % (current_page, page_num, self.site_id, start_date, end_date)
                response = None
                try:
                    response = urllib2.urlopen(data_url)
                except urllib2.URLError as e:
                    if hasattr(e, 'code'):
                        return 'GETDATA ERROR CODE', e.code
                    elif hasattr(e, 'reason'):
                        return 'GETDATA ERROR REASON', e.reason
                finally:
                    if response:
                        return response.read()
    
    # 实例化测试
    x = CnzzCatch('6666666666')  #your website_id  here
    s = x.get_data(1, 30, '2016-07-19')
    print s
