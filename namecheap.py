import requests
from helpers import get_token, get_a_proxy


def namecheap(name: str,
              email: str,
              reporting_websites: list,
              reporting_url: list,
              target_websites: list,
              ticket_subject: str,
              ticket_message: str,
              ):
    url = "https://support.namecheap.com/index.php?/Tickets/Submit/Confirmation"
    reporting_url = '\n'.join(reporting_url)
    payload = "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data; " \
              f"name=\"ticketfullname\"\n\n{name}\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data; " \
              f"name=\"ticketemail\"\n\n{email}\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data;" \
              f"name=\"vgg5i03ghl9x\"\n\n{','.join(reporting_websites)}\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data; " \
              f"name=\"q3d2kveur6xe\"\n\n{reporting_url}\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data; " \
              f"name=\"hibxb9ynzcyk\"\n\n{','.join(target_websites)}\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data;" \
              f"name=\"ticketsubject\"\n\n{ticket_subject}\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data; " \
              f"name=\"ticketmessage\"\n\n{ticket_message}\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data; " \
              "name=\"registrationconsent\"\n\non\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data; " \
              "name=\"g-recaptcha-response\"\n\n" \
              f"{get_token(sitekey='6Lc_ilIUAAAAANld5QNB-AiX_HdommM2dxwxku3Q', url='https://support.namecheap.com/index.php?/Tickets/Submit/Confirmation')}\n\n" \
              "-----------------------------402749634836707718932953940759\n" \
              "Content-Disposition: form-data;" \
              " name=\"departmentid\"\n\n237\n-----------------------------402749634836707718932953940759--\n"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'multipart/form-data; boundary=---------------------------402749634836707718932953940759',
        'Origin': 'https://support.namecheap.com',
        'Connection': 'keep-alive',
        'Referer': 'https://support.namecheap.com/index.php?/Tickets/Submit/RenderForm',
        'Upgrade-Insecure-Requests': '1',
        'Cookie': 'visid_incap_900755=hAJqgXUES4mhcuxb6i9hy1jzNmAAAAAAQkIPAAAAAAA1KRoBlIpwdBmfztqsPgFd; SWIFT_client=%7B%22templategroupid%22%3A%221%22%7D'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, proxies=get_a_proxy())
        if response.status_code == 200:
            return {'status': True, 'message': 'Success', 'urls': reporting_url, 'namecheap': 'Support'}
    except Exception as e:
        return {'status': False, 'message': str(e), 'urls': reporting_url, 'namecheap': 'Support'}
