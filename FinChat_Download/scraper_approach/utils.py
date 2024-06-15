from loggers import Logger
logger = Logger().get_logger('utils')

import requests, json, pydash as py_, traceback
import json, requests, os, re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from lxml import etree
from typing import Any

import configuration

possibleButtonTexts = [
    'Add to Bag','Buy Now','Add to Basket','Add to Bag','Add to Cart','add','Buy it Now','Add to Cart', 'Select size', 
    'Aggiungi al Carrello', 'addToBagButton'
]
buttonXpaths = [
    "//button[contains(text(),'%s')]", "//button[@id='%s']",
    '//span[text()="%s"]', '//span[contains(text(),"%s")]',
    '//a[contains(text(),"%s")]',
    "//input[@value='%s']",
    "//div[contains(text(),'%s')]",
    "//*[text()='%s']", "//*[contains(@value,'%s')]"
]

buttonTexts = []
for text in possibleButtonTexts:
    buttonTexts.append(text)
    buttonTexts.append(text.upper())
    buttonTexts.append(text.lower())
    buttonTexts.append(text.title())
    buttonTexts.append(text.capitalize())


def get_page_content(url: str, request_parameters: dict = None)-> tuple:
    """ 
    Function to hit the FPM module API on GCP. 
    Returns: status(200/404/100/500), html(str/None), availability(1/0), message(str, None), module_used(str/None)
    """
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

    request_parameters = get_module_preferences(domain)
    request_parameters.update(request_parameters)
    logger.info("Using {} parameters for fetching the page content.".format(request_parameters))

    try:
        resp = requests.request(
            'GET',
            "{}/getPageContent?url={}&{}".format(
                configuration.FPM_API, 
                url, 
                '&'.join(["%s=%s" % (key, value) for key, value in request_parameters.items()])
            ),
            timeout=60
        )

        if resp.status_code in [200, 201]:
            res = resp.json()
            logger.info(res['status'])

            if res['status']['code'] in [200, 201]:
                web_content = res['data']['html']
                moduleUsed = res['data']['module_used']
                availability = res['data']['availability']

                if web_content:
                    logger.info(f"fetch_page_content --> {url} Fetched page content with length: {len(web_content)} using {moduleUsed}")
                    print(f"fetch_page_content --> {url} Fetched page content with length: {len(web_content)} using {moduleUsed}")

                    return res['status']['code'], web_content, availability, res['status']['message'], moduleUsed

                return 100, None, 1, res['status']['message'], moduleUsed

            elif res['status']['code'] == 404:
                logger.info("fetch_page_content --> URL %s identified as invalid." % url)
                return 404, None, 0, res['status']['message'], None, None

            elif res['status']['code'] in [-1, 500]:
                logger.info("Couldn't fetch page content for %s, Adding back to the queue." % url)
                return 100, None, res['status']['message'], None, None

        else:
            logger.info("{} --> API Return Code: {}, Content: {}".format(url, resp.status_code, resp.content))

    except Exception as e:
        logger.info("%s --> Exception inside fetch_page_content ==> %s" % (url, e.__str__()))
        print("%s --> Exception inside fetch_page_content ==> %s" % (url, e.__str__()))

    return 500, None, None, None, None

def get_module_preferences(domain: str):
    """ Function to read the domain prefernece from the scrapers_config file. """
    with open(configuration.DOMAIN_MODULE_PREFERENCE_FILE, 'r') as f:
        preferences = json.load(f)
    
    return preferences.get(domain.strip(), {
        "module_preference": "playwright_headless",
        "use_preference_only": True,
        "timeout": 30
    })


class PDP_URL:
    """ PDP URL class used to pass to different modules.  """

    def __init__(self, url: str, **kwargs):
        self.setURL(url)

        self.params = {}
        if kwargs:
            for key, value in kwargs.items():
                self.setParam(key, value)

        self.parseURL()

    def __str__(self):
        return f"URL: {self.getURL()}, Parameters: {self.params}"

    def getURL(self):
        """ Function to get the URL. """
        return self.__url
    
    def setURL(self, url):
        """ Function to set the URL. """
        # TODO: verify the link
        self.__url = url

    def getParam(self, parameter, default=None):
        """ To get a parameter's value for given PDP. """
        return self.params.get(parameter, default)

    def setParam(self, parameter: str, value: any):
        """ To set a parameter for given PDP. """
        if (parameter is not None) and (value is not None):
            self.params[parameter] = value

    def parseURL(self):
        """ Function to parse the URL and extract its components. """
        self.parsedURL = urlparse(self.getURL())
    
    def getURLComponent(self, component):
        """ 
        Function to get one component from the below for the URL object. 
        scheme, netloc, path, query, fragment
        """
        components = ['scheme', 'netloc', 'path', 'query', 'fragment']
        if component.lower() in components:
            return None, self.parsedURL[components.index(component)]

        if component.lower() == 'domain':
            completeDomain = "{url.scheme}://{url.netloc}/".format(url=self.parsedURL)
            words = self.parsedURL[components.index('netloc')].split('.')
            if len(words) > 2:
                domainName = words[1]
            
            else:
                domainName = words[0]
        
            return completeDomain, domainName

    def checkHTML(self, module, htmlText, thresholdForRequests=configuration.DEFAULT_REQUESTS_THRESHOLD):
        """ 
        Function to check if given htmlText is good enough. 
        returns 'not enough content' if the HTML length is less than 100000.
        returns 'valid' if the HTML is usable else 'invalid'.
        """
        if htmlText.strip() == 'invalid_url':
            return 'invalid_url'

        invalidURLTexts = [
            r"we seem to have misplaced this page",
            r"(it's|its) not you, (it's|its) us",
            r"we (couldn't|can't|can not|could not) find the page you're looking for",
            r"we apologize for (the|any) inconveinience",
            r"the page you requested (does not|doesn't) exist",
            r"the page you are looking for (does not|doesn't) exist",
            r"(404|page) not (found|available)",
            r"page (can't|cannot|couldn't|could not) be found",
            r"we (couldn't|can't|can not|could not) find what you (are|were) looking for",
            r"the product (you are|you're|you were) is no longer available",
            r"the page you are (searching|looking) for is unavailable",
            r"be the first to know" # If the sites is down.
        ]
        # r"\d+\s*(results|products|styles found)",

        accessDeniedOrBlockedTexts = [
            r"please verify you are a human",
            r"access to this page has been denied",
            r"we believe you are using automation (tool|tools) to browse the website",
            r"(we've|we have) noticed some unusual activity",
            r"enable javaScript and cookies to continue"
        ]
        # r"for technical reasons, your request could not be handled properly at this time",
        # TODO: Check if the html Text is string, and convert to string if byte like object.

        HTML_LENGTH = len(htmlText)
        # if module == 'requests':
        #     if HTML_LENGTH < 300000:
        #         logger.info("%s --> Fetched using requests module, content size less then 300000. Identified invalid." % self.getURL())
        #         return 'invalid'

        #     return 'valid'\
        if module == 'requests' and HTML_LENGTH < thresholdForRequests:
            logger.info("%s --> Using Requests, page content size less than %d. Page cotent identified as invalid." % (self.getURL(), thresholdForRequests))
            return 'not_enough_content'

        # if module != 'requests' and HTML_LENGTH < 100000:
        #     logger.info("%s --> Content size less than 100000. Page content identified as invalid." % self.getURL())
        #     return 'not_enough_content'

        try:
            for text in accessDeniedOrBlockedTexts:
                regex = re.compile(r"%s"%text, re.I)
                matchFound = regex.search(htmlText)
                if matchFound is not None and HTML_LENGTH < 500000:
                    logger.info("%s --> %s matched with htmlText. Page access might have been denied or blocked. Suggest retrying with headed instance."%(self.getURL(), text))
                    logger.info(f"{self.getURL()} --> {matchFound}")
                    return 'invalid'

            for text in invalidURLTexts:
                regex = re.compile(r"%s"%text, re.I)
                matchFound = regex.search(htmlText)
                if matchFound is not None and HTML_LENGTH < 500000:
                    logger.info("%s --> %s matched with htmlText. URL is invalid."%(self.getURL(), text))
                    logger.info(f"{self.getURL()} --> {matchFound}")
                    return 'invalid_url'

        except Exception as e:
            logger.info("%s --> Exception inside PDP_URL.checkHTML ==> %s" % (self.getURL(), e.__str__()))

        return 'valid'

    def findAvailability(self, htmlText):
        """ 
        Function to check the product availability. 
        Returns a tuple with Flags: (Button Found?, Product is in Pre-order state?, If there were any errors?)
        True, False, False --> Meaning that product is available.
        _, _, True --. Meaning that there was some error when checking the availability.
        True, True, False --> Meaning that product is not available at the moment and is in pre-order state.
        """

        try:
            soup = BeautifulSoup(htmlText, 'html.parser')
            dom = etree.HTML(str(soup))

            # if 'www.manyavar.com' in self.getURL():
            #     if not dom.xpath("//img[@class='wishlistImg']"):
            #         logger.info("%s --> URL is from Manyavar. Wishlisting image at //img[@class='wishlistImg'] was not found on the page.")
            #         return False, False, False

            for xPath in buttonXpaths:
                for text in buttonTexts:
                    if 'indianterrain.com' in self.getURL() and ((xPath % text).lower() in ["//a[contains(text(), 'add to cart')]"]):
                        continue

                    if 'ordinaree.com' in self.getURL() and ((xPath % text).lower() in ["//span[contains(text(), 'add to cart')]", "//span[contains(text(), 'sold out')]"]):
                        continue

                    buttonElements = dom.xpath(xPath % text)

                    if not buttonElements:
                        continue
                    
                    else:
                        logger.info("%s --> Found %d matching element for %s" % (self.getURL(), len(buttonElements), xPath % text))

                        if text.lower() in ['pre-order now', 'pre order now']:
                            return True, True, False
                        
                        return True, False, False

        except Exception as e:
            logger.error("Exception inside PDP_URL.findAvailability ==> %s" % e.__str__())

            return True, False, True

        logger.info("%s --> No purchase button found on the page." % self.getURL())
        return False, False, False


def get_domain(url: str)-> tuple[str]:
    """ 
    To get domain with and without URL scheme. 
    Eg., For url = "https://www.nike.com/in/t/air-max-pulse-shoes-V9B1C5/FD6409-002
    returns: ('https://www.nike.com/', 'www.nike.com')
    """
    parsed_url = urlparse(url)
    return "{url.scheme}://{url.netloc}/".format(url=parsed_url), parsed_url.netloc

def get_site_names(domain: str):
    """
    To find list of possible domain names which can be used in the HTML Text.
    Eg., For www.nike.com --> ['www.nike.com', 'nike.com', 'nike']
    """
    domain = domain.lower()
    site_names = set()
    site_names.add(domain)

    try:
        if domain:
            parts = domain.split(".")
            num_parts = len(parts)
            if num_parts == 2:
                site_names.add(parts[0])
            elif num_parts > 2:

                if parts[-2] == "co":
                    site_names.add("%s.%s.%s" % (parts[-3], parts[-2], parts[-1]))
                    site_names.add(parts[-3] + ".com")
                    site_names.add(parts[-3])

                elif parts[-1] == "com":
                    site_names.add("%s.%s" % (parts[-2], parts[-1]))
                    site_names.add(parts[-2])

                else:
                    site_names.add("%s.%s" % (parts[-2], parts[-1]))
                    site_names.add(parts[-2] + ".com")
                    site_names.add(parts[-2])

        site_names = list(site_names)
        site_names.sort(key=lambda x: -1 * len(x))

    except Exception as e:
        logger.error("Exception inside get_site_names ==> %s" % str(e))

    return site_names

def post_to_ms_teams(messages: list[Any], do_mention = False, title = "Storage box alerts"):
    if os.environ.get('block_alerts', 'no').strip().lower() == 'yes':
        return
    try:
        logger.info("Posting alerts to teams.")
        alertBody = [{
            "type": "TextBlock",
            "text": "{}".format(title),
            "weight": "bolder",
            "wrap": True
        }]
        for message in messages:
            if isinstance(message, str):
                alertBody.append({
                    "type": "TextBlock",
                    "text": message,
                    "width": "stretch",
                    "height": "auto",
                    "wrap": True
                })

            elif isinstance(message, dict):
                alertBody.append({
                    "type": "FactSet",
                    "facts": [
                        {"title": key, "value": json.dumps(value), "width": "stretch"} for key, value in message.items()
                    ]
                })

        if do_mention:
            mention_strings = ["<at>{}</at>".format(user['name']) for user in configuration.PEOPLE_TO_MENTION]
            alertBody.append({
                "type": "TextBlock",
                "text": "{} Please take the necessary steps at the earliest.".format(','.join(mention_strings)),
                "width": "stretch",
                "height": "auto",
                "wrap": True
            })

        data = {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "content": {
                        "type": "AdaptiveCard",
                        "body": alertBody,
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "version": "1.2",
                        "msteams": {
                            "width": "Full"
                        }
                    }
                }
            ]
        }
        if do_mention:
            data['attachments'][0]['content']['msteams']["entities"] = [
                {
                    "type": "mention",
                    "text": "<at>{}</at>".format(user['name']),
                    "mentioned": {
                        "id": "{}".format(user['email']),
                        "name": "{}".format(user['name'])
                    }
                } for user in configuration.PEOPLE_TO_MENTION
            ]

        # logger.info(json.dumps(data, indent=2))
        response = requests.request('POST', configuration.USC_ALERTS_WEBHOOK, data=json.dumps(data, indent=2), timeout=30)
        logger.info(response.content)

        if response.status_code == 200:
            logger.info("Alert Posted.")

    except Exception as e:
        logger.error("Exception inside post_an_alert_to_teams ==> {}".format(e))