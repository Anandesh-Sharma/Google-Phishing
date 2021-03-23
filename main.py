from concurrent.futures import ThreadPoolExecutor
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import threading
from config import *
import urllib
from google_web import google_report_1, google_report_2, google_report_3
from cloudflare import CloudFlareReport
from namecheap import namecheap
from report_ids import request
from helpers import get_cloudflare_links, get_a_proxy
import pymongo

client = pymongo.MongoClient('mongodb://{}:{}@localhost:27017'.format(mongo_username, mongo_password))


def get_ads_from_search(browser):
    link_ids = list()
    ads = browser.find_elements_by_xpath("//a[@data-rw]")

    for ad in ads:
        link_ids.append({'link': ad.find_element_by_xpath(".//span[2]").text,
                         'report_id': ad.get_attribute("data-rw").split('?')[1].split('&')[1].split('=')[1]})

    return link_ids


class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)

        super().__init__(group=group, target=function, name=name, daemon=daemon)


def google_reporting_links(plink):
    mt_requests = list()
    # add_message and sitekey can be added if necessary
    mt_requests.append(ThreadWithResult(target=google_report_1, args=(plink,)))
    mt_requests.append(ThreadWithResult(target=google_report_2, args=(plink,)))
    mt_requests.append(ThreadWithResult(target=google_report_3, args=(plink,)))

    for req in mt_requests:
        req.start()

    for req in mt_requests:
        req.join()
        print(req.result)


def google_report_ids(ids):
    mt_requests = list()
    for id in ids:
        mt_requests.append(ThreadWithResult(target=request, args=(email, id, add_message,)))
    for req in mt_requests:
        req.start()
    for req in mt_requests:
        req.join()
        print(req.result)


def main():
    mobile_emulation = {
        "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}
    options = {
        'proxy': get_a_proxy(cc='US')
    }
    chrome_options = Options()
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(seleniumwire_options=options, options=chrome_options)
    return driver


def search_term(term):
    try:
        """GET DRIVER INITIATED"""
        browser = main()

        """INPUT DATA"""
        search_term = term

        """GET GOOGLE SEARCH DONE"""
        browser.get('https://google.com/')
        search_elem = browser.find_element_by_xpath("//input[@type='search']")
        search_elem.send_keys(search_term)
        search_elem.send_keys(Keys.ENTER)

        """GET AD LINKS FROM THE SEARCH"""
        links_ids = get_ads_from_search(browser=browser)
        browser.close()
        return {'status': True, 'links_ids': links_ids, 'message': 'Success'}
    except Exception as e:
        return {'status': False, 'links_ids': [], 'message': str(e)}


def report_master():
    links_ids = client['master']['links'].find()
    reporting_task = []
    for i in links_ids:
        if 'reporting_links' in i:
            for x in i['reporting_links']:
                reporting_task.append(x)
    if len(reporting_task) != 0:
        google_data = []
        links = [i['link'] for i in reporting_task]
        ids = [i['report_id'] for i in reporting_task]
        for i in links_ids:
            google_data.append((urllib.parse.quote_plus(i['link']), urllib.parse.quote_plus(add_message)))
        """REPORT TO GOOGLE WEBSITES"""
        import time

        t = time.time()
        with ThreadPoolExecutor() as executor:
            executor.map(google_reporting_links, links)

        """REPORT TO CLOUDFLARE"""
        cloudflare_links = get_cloudflare_links(links)
        if cloudflare_links:
            print(CloudFlareReport(reporting_url=cloudflare_links,
                                   logs=add_message,
                                   name=name,
                                   email=email).formSubmit())

        """REPORT NAMECHEAP"""
        print(namecheap(name=name,
                        email=email,
                        reporting_url=links,
                        reporting_websites=links,
                        target_websites=links,
                        ticket_subject=subject,
                        ticket_message=add_message))
        """REPORT GOOGLE IDS"""
        google_report_ids(ids=ids)
        print(f"time took : {time.time() - t}")
