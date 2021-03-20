from twocaptcha import TwoCaptcha
from config import username, password
import requests
from urllib.parse import urlparse


def get_token(sitekey, url):
    solver = TwoCaptcha(apiKey='a464e17395843472cfcf29502f14be1f')
    while True:
        try:
            TOKEN = solver.recaptcha(sitekey=sitekey, url=url)['code']
            break
        except Exception as e:
            print('Failed to acquire token, Retrying !!')
            pass

    return TOKEN


def get_a_proxy(cc=None):
    if cc:
        entry = f"http://{username}-cc-{cc}:{password}@pr.oxylabs.io:7777"
    else:
        entry = f"http://{username}:{password}@pr.oxylabs.io:7777"
    return {
        'http': entry,
        'https': entry
    }


def get_sel_proxy_zip(url: str):
    backgroundjs = """
        var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
            scheme: "http",
            host: "",
            port: parseInt(PROXY_PORT)
            },
            bypassList: ["foobar.com"]
            }
            };
            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
            function callbackFn(details) {
            return {
            authCredentials: {
            username: "PROXY_USERNAME",
            password: "PROXY_PASSWORD"
            }
            };
            }
            
            chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
            );
    """


def fetch_dns(url: str) -> dict:
    url = urlparse("http://"+url).netloc
    if 'www.' in url:
        url = url.replace('www.', '').lstrip()
    try:
        call_url = 'https://rdap.verisign.com/com/v1/domain/{}'.format(url)
        dns_info = requests.get(url=call_url).json()
        return {'status': True, 'message': 'Success', 'url': url, 'dns_info': dns_info}
    except Exception as e:
        return {'status': False, 'message': str(e), 'url': url, 'dns_info': {}}


def get_cloudflare_links(links: list) -> list:
    cloudf_links = []
    for link in links:
        dns_info = fetch_dns(link)['dns_info']
        if dns_info:
            if 'cloudflare' in dns_info['nameservers'][0]['ldhName'].lower():
                cloudf_links.append(link)

    return cloudf_links
