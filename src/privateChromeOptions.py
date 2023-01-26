from selenium.webdriver.chrome.options import Options
import random
import os

# from fake_useragent import UserAgent

list_device_example = ['iPad', 'iPad Pro', 'iPhone X', 'Pixel 2', 'Pixel 2 XL', 'Galaxy S5']


def setting_chrome_privated(proxy):
    # private chrome options
    chrome_options = Options()
    random_user_agent = 'Mozilla/5.0 (Windows NT {}; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/{}.0.{}.60 ' \
                        'Safari/537.17'.format(random.choice(['6,1', '10.0']),
                                               random.randrange(65, 92), random.choice(['1312', '1077']))
    # add user agents
    # ua = UserAgent()

    chrome_options.add_argument('user-agent={}'.format(random_user_agent))
    # chrome_options.add_argument('user-agent={}'.format(ua['google chrome']))
    # chrome_options.add_argument('--proxy-server=socks5://' + proxy)

    if proxy:
        chrome_options.add_argument('--proxy-server=%s' % proxy)


    # chrome_options.add_experimental_option("mobileEmulation", {
    #     "deviceName": 'iPhone X',
    # })

    # tat bao mat web
    # chrome_options.add_argument("test-type")
    # chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--disable-web-security")
    # chrome_options.add_argument("--allow-running-insecure-content")

    # add extension, only file crx appect
    # chrome_options.add_extension(r'C:\Users\This PC\PycharmProjects\RegHotMail_version_pro\AnyCaptchaExtension.crx')
    # load extension
    chrome_options.add_argument(r"--load-extension=" + os.getcwd() + '\\AnyCaptchaExtension')

    # chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins-discovery")
    # fix lỗi devtools nhưng sẽ hiện "chrome is being controlled by automated test software"
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # disable image
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false')

    # disable gpu
    chrome_options.add_argument("--disable-gpu")

    # disable js
    # chrome_options.add_experimental_option("prefs", {'profile.managed_default_content_settings.javascript': 2})

    # headless browser
    # chrome_options.headless = True

    # without login image
    # not_load_image = {'profile.managed_default_content_settings.images': 2}
    # chrome_options.add_experimental_option("prefs", not_load_image)

    # not loading css
    # prefs = {"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option("prefs", prefs)
    # prefs = {"profile.default_content_setting_values.geolocation": 2}
    # chrome_options.add_experimental_option("prefs", prefs)

    # turn off save password popup
    chrome_options.add_experimental_option('prefs', {
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    })
    # partially disable webrtc and geolocation, disable noftification
    preferences = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False,
        "profile.default_content_setting_values.geolocation": 2,
        "profile.default_content_setting_values.notifications": 2,
        'credentials_enable_service': False,
        'profile': {
            'password_manager_enabled': False
        }
    }
    chrome_options.add_experimental_option("prefs", preferences)
    # End Privated chrome

    return chrome_options
