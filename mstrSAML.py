# developed by Pawel Gnatowski - in case of issues mail to: pgnatowski@gmail.com
import time
from seleniumwire import webdriver
# ISSUES certificate is not trusted:
# https://github.com/wkeeling/selenium-wire/issues/31
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests

# webDriver might need to be added to path
# for SSO it is necessary to read profile of the User to read all cockies etc.
# get profile folder path from: chrome://version => Profile Path
# remove /Default from path
# if there are multiple profiles you need to specify additionally directgory Path option
# inititate SAML workflow via browser instance


def browser(browser='', ssoProfile='') -> webdriver:
    if browser.lower() == 'chrome' or browser == '':
        options = webdriver.ChromeOptions()
        if ssoProfile != '':
            options.add_argument('--user-data-dir=' + ssoProfile)
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # TODO add proper edge support
    if browser.lower() == 'edge':
        return webdriver.Edge(EdgeChromiumDriverManager().install())
    raise NameError(
        r'selected browser is not supported. Try browser="chrome" or Edge or modify browser function in the library)')


def doSamlAuth(base_url, timeout=5, useBrowser='', user_data_dir='') -> dict:

    driver = browser(browser=useBrowser, ssoProfile=user_data_dir)
    driver.get(base_url)

    time.sleep(timeout)

    while base_url not in driver.current_url:
        time.sleep(timeout)

    authCookies = driver.get_cookies()

    # try 3 times to claim token
    i = 0
    token = ''
    while i < 3 and (token == '' or token is None):
        for request in driver.requests:

            xauth = request.headers.get('x-mstr-authToken')

            print(request.headers)

            if xauth is not None:
                token = xauth
                print('authed' + xauth)

        i += 1

        if token is None or token == '':
            # wait for token, then try again
            # TODO rewrite to use hooks
            time.sleep(timeout)
        else:
            driver.quit()

    if authCookies is None or authCookies == '':
        raise NameError(
            'cookies could not be retrieved - try increasing timeout maybe?')
    if token == '' or token is None:
        raise NameError(
            'authtoken could not be retrived - try increasing timeout maybe? ')
    credentials = dict()
    credentials['cookies'] = authCookies
    credentials['authToken'] = token

    return credentials


def MstrSession(base_url, timeout=5, useBrowser='', user_data_dir='') ->requests.Session:
    # check if base_url ends with /
    if base_url[-1] != '/':
        base_url += '/'

    auth = doSamlAuth(base_url, timeout=timeout,
                      useBrowser=useBrowser, user_data_dir=user_data_dir)

    mstrSession = requests.Session()
    mstrSession.headers.update({
        'X-MSTR-AuthToken': auth['authToken']
    })
    cookieDict = auth['cookies']
    exceptionList = ['httpOnly', 'expiry', 'sameSite']
    for cookie in cookieDict:
        for exclude in exceptionList:

            if exclude in cookie:
                cookie.pop(exclude)
        mstrSession.cookies.set(**cookie)
    mstrSession.baseURL = base_url
    # all we really neeed is the authToken and cookies, then depending on the endpoint we also might need Project header.
    return mstrSession
