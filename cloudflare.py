from selenium import webdriver


class CloudFlareReport:
    def __init__(self,
                 reporting_url: list,
                 logs: str,
                 name: str,
                 email: str,
                 title='This website is a phishing website',
                 company_name='',
                 telephone='',
                 video_id='',
                 comments='Please stop these kind of Abusing/Phishing websites around the internet, Thank you!'
                 ):
        self.URL = 'https://www.cloudflare.com/abuse/form'
        self.copt = webdriver.ChromeOptions()
        self.copt.headless = True
        self.browser = webdriver.Chrome(options=self.copt)
        self.browser.get(self.URL)
        self.xpathDropDown = '/html/body/div[1]/div[2]/div[3]/div[2]/div/div[2]/div/div/div[1]'
        self.xpathPhishing = '/html/body/div[5]/ul/li[7]/a/span'
        self.xpathName = '//*[@id="Name"]'
        self.xpathEmail = '//*[@id="Email"]'
        self.xpathConfirmEmail = '//*[@id="EmailConfirm"]'
        self.xpathTitle = '//*[@id="Title"]'
        self.xpathCompanyName = '//*[@id="Company"]'
        self.xpathTelephone = '//*[@id="Tele"]'
        self.xpathEvidenceURL = '//*[@id="URLs"]'
        self.xpathLogs = '//*[@id="Infringement"]'
        self.xpathVideoID = '//*[@id="VideoIDs"]'
        self.xpathComments = '//*[@id="Comments"]'
        self.xpathSubmit = '//*[@id="abuse-submit"]'

        self.name = name
        self.email = email
        self.title = title
        self.companyName = company_name
        self.telephone = telephone
        self.evidenceURL = '\n'.join(reporting_url)
        self.logs = logs
        self.videoID = video_id
        self.comments = comments

    def formSubmit(self):
        try:
            self.browser.find_element_by_xpath(self.xpathDropDown).click()
            self.browser.find_element_by_xpath(self.xpathPhishing).click()

            # Filling Form Details
            self.browser.find_element_by_xpath(self.xpathName).send_keys(self.name)
            self.browser.find_element_by_xpath(self.xpathEmail).send_keys(self.email)
            self.browser.find_element_by_xpath(self.xpathConfirmEmail).send_keys(self.email)
            self.browser.find_element_by_xpath(self.xpathTitle).send_keys(self.title)
            self.browser.find_element_by_xpath(self.xpathCompanyName).send_keys(self.companyName)
            self.browser.find_element_by_xpath(self.xpathTelephone).send_keys(self.telephone)
            self.browser.find_element_by_xpath(self.xpathEvidenceURL).send_keys(self.evidenceURL)
            self.browser.find_element_by_xpath(self.xpathLogs).send_keys(self.logs)
            self.browser.find_element_by_xpath(self.xpathVideoID).send_keys(self.videoID)
            self.browser.find_element_by_xpath(self.xpathComments).send_keys(self.comments)

            self.browser.find_element_by_xpath(self.xpathSubmit).click()

            print("Reported !!")
            return {'status': True, 'message': 'Success', 'urls': self.evidenceURL}
        except Exception as e:
            return {{'status': False, 'message': str(e), 'urls': self.evidenceURL}}
