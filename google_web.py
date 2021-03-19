from helpers import get_token, get_a_proxy
import requests
from bs4 import BeautifulSoup


def google_report_1(plink, sitekey="6LdCiQETAAAAADLZgnQbEQ8zAGa1eL7YA7TtN4N1",
                    add_message="This website is a phishing website, Please take some actions on this!"):
    """
    :param plink: string | url encoded parsed link
    :param sitekey: string | Google ReCaptcha sitekey
    :param add_message: string | additional message for reporting the website
    :return: Boolean | if it reported successfully
    """
    url = "https://safebrowsing.google.com/safebrowsing/report_badware/"
    token = get_token(sitekey=sitekey, url=url)

    callable_url = f"https://safebrowsing.google.com/safebrowsing/report_badware/Captcha?id=&tpl=&hl=&url={plink}&g-recaptcha-response={token}&dq={add_message}&submit=Submit+Report"
    response = requests.get(url=callable_url, proxies=get_a_proxy(), timeout=200)
    if 'Thank you!' in BeautifulSoup(response.text, features='html.parser').find('title').text:
        return {'status': True, 'google': 'badware', 'message': "Success", 'reporting_link': plink}
    else:
        return {'status': False, 'google': 'badware', 'message': response.text, 'reporting_link': plink}


def google_report_2(plink, sitekey="6LdCiQETAAAAADLZgnQbEQ8zAGa1eL7YA7TtN4N1",
                    add_message="This website is a phishing website, Please take some actions on this!"):
    """
    :param plink: string | url encoded parsed link
    :param sitekey: string | Google ReCaptcha sitekey
    :param add_message: string | additional message for reporting the website
    :return: Boolean | if it reported successfully
    """
    url = "https://safebrowsing.google.com/safebrowsing/report_general/"
    token = get_token(sitekey=sitekey, url=url)

    callable_url = f"https://safebrowsing.google.com/safebrowsing/report_general/Captcha?url={plink}&g-recaptcha-response={token}&category=falseneg&dq={add_message}&submit=Submit+Report"
    response = requests.get(url=callable_url, proxies=get_a_proxy(), timeout=200)
    if 'Thank you!' in BeautifulSoup(response.text, features='html.parser').find('title').text:
        return {'status': True, 'google': 'general', 'message': "Success", 'reporting_link': plink}
    else:
        return {'status': False, 'google': 'general', 'message': response.text, 'reporting_link': plink}


def google_report_3(plink, sitekey="6LdCiQETAAAAADLZgnQbEQ8zAGa1eL7YA7TtN4N1",
                    add_message="This website is a phishing website, Please take some actions on this!"):
    """
    :param plink: string | url encoded parsed link
    :param sitekey: string | Google ReCaptcha sitekey
    :param add_message: string | additional message for reporting the website
    :return: Boolean | if it reported successfully
    """
    url = "https://safebrowsing.google.com/safebrowsing/report_phish/"
    token = get_token(sitekey=sitekey, url=url)

    callable_url = f"https://safebrowsing.google.com/safebrowsing/report_phish/Captcha?url={plink}&g-recaptcha-response={token}&dq={add_message}&submit=Submit+Report"
    response = requests.get(url=callable_url, proxies=get_a_proxy(), timeout=200)
    if 'Thank you!' in BeautifulSoup(response.text, features='html.parser').find('title').text:
        return {'status': True, 'google': 'phishing', 'message': "Success", 'reporting_link': plink}
    else:
        return {'status': False, 'google': 'phishing', 'message': response.text, 'reporting_link': plink}
