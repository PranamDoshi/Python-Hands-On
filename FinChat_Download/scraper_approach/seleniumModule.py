from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as firefoxOptions
from selenium.common.exceptions import StaleElementReferenceException, InvalidSelectorException, NoAlertPresentException, WebDriverException, InvalidArgumentException, JavascriptException
# import undetected_chromedriver as uc

import psutil, time, re, os, random, subprocess, traceback, json

import configuration
from loggers import Logger
logger = Logger().get_logger('selenium')

from utils import PDP_URL
from driverGeneral import DriverGeneral

class Driver(DriverGeneral):
    """ Selenium Webdriver. """

    def __init__(self, browser='chrome', headless=True, load_images = True):
        self.browser = browser
        self.headless = headless
        self.__driver = None
        self.__driverProcessID = None

        # logging = logging.getlogging('selenium_Driver')
        # logging = logging.loggingAdapter(logging, {'processID': os.getpid()})

        self.port = None
        self.load_images = load_images
        # self.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
        self.flagsToAdd = [
            f'--window-size={configuration.DISPLAY_SIZE_STRING}',
            '--disable-gpu',
            '--enable-javascript',
            '--aggressive-cache-discard',
            '--disable-cache',
            '--disable-application-cache',
            '--disable-offline-load-stale-cache',
            '--disable-gpu-shader-disk-cache',
            '--media-cache-size=0',
            '--disk-cache-size=0',
            '--mute-audio',
            '--disable-extensions',
            '--disable-default-apps',
            '--no-default-browser-check',
            '--disable-background-timer-throttling',
            '--block-new-web-contents',
            '--disable-dev-shm-usage'
        ]
        # self.userAgent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

        DriverGeneral.__init__(self)

    def getNextUserAgent(self)-> tuple:
        """ Function to get random userAgent with appropriate OS name. """
        logger.info("Using Chrome version: %s" % configuration.CHROME_VERSION)
        OS_names = ['Linux', 'Mac OS', 'Win64', 'CrOS', 'WOW64']

        userAgentIndex = random.randint(0, len(configuration.userAgents[self.browser])-1)
        userAgent = configuration.userAgents[self.browser][userAgentIndex]
        for os_name in OS_names:
            if os_name in userAgent:
                return userAgent, os_name

        return userAgent, OS_names[0]

    def initializeDriver(self):
        """ Method to initialize the driver. """
        try:
            # if self.browser.lower() == 'firefox':
            #     logger.info("Selenium ==> Indializing the driver - firefox...")

            #     firefox_profile = webdriver.FirefoxProfile()
            #     firefox_profile.set_preference("intl.accept_languages", "en")
            #     if not self.load_images:
            #         firefox_profile.set_preference('permissions.default.image', 2)
            #         firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

            #     if self.port is not None:
            #         firefox_profile.set_preference("network.proxy.http_port", self.port)

            #     options = firefoxOptions()
            #     if self.headless:
            #         options.add_argument("--headless")

            #     self.__driver = webdriver.Firefox(firefox_profile=firefox_profile, firefox_options=options,executable_path=configuration.FIREFOXDRIVER)
            #     self.__driverProcessID = self.__driver.service.process.pid
            #     logger.info("Started the Firefox driver process %d"%self.__driverProcessID)

            if self.browser.lower() == 'chrome':
                logger.info("Selenium ==> Indializing the driver - chrome...")

                self.userAgent, _ = self.getNextUserAgent()
                logger.info("Using %s user Agent" % self.userAgent)
                chromeOptions = webdriver.ChromeOptions()
                chromeOptions.add_argument("--disable-notifications")
                chromeOptions.add_argument('--lang=en-us')
                chromeOptions.add_argument('--user-agent=%s'%self.userAgent)
                chromeOptions.add_argument('--no-sandbox')
                chromeOptions.add_argument('--disable-dev-shm-usage')
                chromeOptions.add_argument('--enable-javascript')
                chromeOptions.add_argument('--incognito')
                #chromeOptions.add_arguments("disable-geolocation")
                for flag in self.flagsToAdd:
                    chromeOptions.add_argument(flag)

                prefs = {'intl.accept_languages': 'en,en_US'}
                if not self.load_images:
                    prefs["profile.managed_default_content_settings.images"] = 2
                chromeOptions.add_experimental_option('prefs', prefs)
                if not self.load_images:
                    prefs = {"profile.managed_default_content_settings.images": 2}
                    chromeOptions.add_experimental_option("prefs", prefs)

                if self.headless:
                    chromeOptions.add_argument('headless')

                if self.port is None:
                    self.__driver = webdriver.Chrome(executable_path=configuration.CHROMEDRIVER, options=chromeOptions)
                    # self.__driver = uc.Chrome(browser_executable_path=configuration.CHROME, options=chromeOptions)
                else:
                    self.__driver = webdriver.Chrome(executable_path=configuration.CHROMEDRIVER, options=chromeOptions, port=self.port)
                    # self.__driver = uc.Chrome(browser_executable_path=configuration.CHROME, options=chromeOptions, port=self.port)

                self.__driverProcessID = self.__driver.service.process.pid
                logger.info(f"Started the chromedriver process {self.__driverProcessID}.")

            else:
                logger.info("%s Browser not supported."%self.browser)
        
        except Exception as e:
            logger.error("Exception inside intializeDriver --> %s"%e.__str__(), exc_info=True)
            self.__driver = None
            self.__driverProcessID = None

    def closeDriver(self):
        """ Function to close the selenium driver. """
        try:
            logger.info("Selenium ==> Closing the driver...")
            if self.__driver is not None:
                try:
                    self.__driver.quit()

                except Exception as e:
                    pass

            if self.__driverProcessID is not None and psutil.pid_exists(self.__driverProcessID):
                psutilProcess = psutil.Process(self.__driverProcessID)
                psutilProcessChildren = psutilProcess.children(recursive=True)

                for process in psutilProcessChildren:
                    
                    if psutil.pid_exists(process.pid):
                        logger.info("Killing driver child process - %d"%process.pid)
                        process.kill()

                try:
                    logger.info("Killing driver process: %d"%self.__driverProcessID)
                    psutil.Process(self.__driverProcessID).kill()
                
                except Exception as e:
                    pass

        except Exception as e:
            logger.error("Exception while closing driver: %s"%e.__str__())

            if self.__driverProcessID is not None and psutil.pid_exists(self.__driverProcessID):
                logger.info("Killing driver process: %d"%self.__driverProcessID)
                psutil.Process(self.__driverProcessID).kill()

        finally:
            self.__driverProcessID = None
            self.__driver = None

    def restartDriver(self):
        """ Function to restart the selenium driver. """
        try:
            logger.info("Selenium ==> Restarting the driver...")
            self.closeDriver()

        except Exception as e:
            logger.error("Exception while restartting the drivers: %s"%e.__str__())

        finally:
            self.initializeDriver()

    def checkIfBrowsersIsOpened(self):
        """ Function to check if the browser was opened or not. """
        return self.__driver is not None

    def goToURL(self, url, waitUntil=configuration.DEFAULT_TIMEOUT):
        """ Function to open the page. """
        # self.__driver.switch_to.new_window('tab')
        self.__driver.set_page_load_timeout(waitUntil)
        self.__driver.get(url)
        # time.sleep(self.get_sleep)

        ex_scr = '''
            let oldH = 0; window.newH = 0;
            console.log("setInterval ****************")  
            setInterval(function(){
                let newH = document.getElementsByTagName('body')[0].scrollHeight;
                if(oldH != newH){ oldH = newH; window.newH = newH; console.log(window.newH);}
            }, 500)
        '''
        self.execute_script(ex_scr)
        #rval = self.execute_script(''' return window.newH ''')
        self.bypass_alert()
        # self.wait_until_loaded()
        # hasClicked = self.close_modal_window()
        # time.sleep(2)
        # if hasClicked:
        #     self.wait_until_loaded()

            # Some sites may give a follow-up pop up eg. Mango
            # hasClicked = self.close_modal_window()
            # if hasClicked:
            #     self.wait_until_loaded()

        # if 'finchat.io' in url:
        #     login_button = self.find_elements_by_xpath("//button[child::div[child::span[contains(text(), 'Login')]]]")
        #     if login_button:
        #         self.click_element(login_button[0])
        #         email_input = self.find_elements_by_xpath("//form//input[@placeholder='your@email.com']")
        #         if email_input:
        #             email_input[0].send_keys("pranamdoshi@gmail.com")

        #             input_parent = self.find_elements_by_xpath_relativeToelement(email_input[0], "..")
        #             logger.info(f"input_parent: {input_parent}")
        #             if input_parent:
        #                 submit_button = self.find_elements_by_xpath_relativeToelement(input_parent[0], ".//button")
        #                 logger.info(f"submit_button: {submit_button}")
        #                 if submit_button:
        #                     submit_button[0].click()
        #                     time.sleep(30)

        #                     self.goToURL(url, waitUntil=waitUntil)

        #     time.sleep(60)

    def screenshot(self, filePath):
        """ Function to take screenshot of the page. """
        if configuration.ALLOW_SCREENSHOTS:
            fileName = filePath.split('/')[-1]
            self.__driver.get_screenshot_as_file(filePath)

    def getPageTitle(self):
        """ Function to get page title. """
        return self.processPageTitle(self.__driver.title)

    def getPageHTML(self):
        """ Function to get page source. """
        return self.__driver.page_source
    
    def checkIfNeedToWaitMore(self, htmlText):
        """ Function to check if given html text is of loaded page or some other redirected page. """
        siteLoadingText = [
            r"checking if the site connection is secure"
        ]

        for text in siteLoadingText:
            regex = re.compile(r"%s" % text, re.I)
            matchFound = regex.search(htmlText)
            if matchFound is not None:
                return True, matchFound

        return False, None

    def getCurrentURL(self):
        """ Function to get the current page URL. """
        return self.__driver.current_url

    def getInnerHTML(self, element):
        """ Function to get the innert HTML of an element. """
        return self.getAttribute(element, "innerHTML")

    def getValueOfCSSProperty(self, element, attr):
        """ Function to get the css property of given element. """
        return element.value_of_css_property(attr)

    def getAttribute(self, element, attr):
        """ Function to get the given attribute value passed element. """
        try:
            return element.get_attribute(attr)

        except StaleElementReferenceException as e:
            logger.error('Exception inside getAttribute: %s' % e.__str__())
            return None

    def isDisplayed(self, element):
        """ Function to check if an element is displayed on the page or not. """
        try:
            return element.is_displayed()

        except StaleElementReferenceException as e:
            return False
        
        except JavascriptException as e:
            return False

    def find_elements_by_tag_name(self, tag_name):
        """ Function to search elements by Tag Name. """
        return self.__driver.find_elements(By.TAG_NAME, tag_name)

    def find_elements_by_xpath(self, xpath):
        """ Function to search elements by xPath. """
        return self.__driver.find_elements(By.XPATH, xpath)
    
    def find_elements_by_xpath_relativeToelement(self, element, xpath):
        """ Function to find to elements by xPath for given element. """
        try:
            return element.find_elements(By.XPATH, xpath)

        except Exception as e:
            logger.error("Exception inside find_elements_by_xpath_relativeToelement ==> %s" % e.__str__())
        
        return []

    def execute_script(self, script, *arg):
        """ Function to execute a script using Selenium Driver. """
        return self.__driver.execute_script(script, *arg)

    def clickByXPATH(self, xpath):
        """ Function to click on a element at given xPath. """
        wait = WebDriverWait(self.__driver, 10)
        try:
            element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            # element = wait.until(EC.visibility_of((By.XPATH, xpath)))

        except Exception as e:
            logger.error('Exception while waiting for the element to be clickable...Inside click_by_xpath')
            return None

        if element is None:
            return None
        logger.info('clicking %s...' % element.text)
        self.click_element(element)

        return element.text

    def bypass_alert(self):
        """ Function to accept the alert if it arises. """
        acceptCount = 0
        while True:
            try:
                acceptCount += 1
                alert = self.__driver.switch_to.alert
                alert.accept()
                logger.info('Alert accepted')

                if acceptCount == 5:
                    break

            except NoAlertPresentException as e:
                break

    def click_anchor(self, anchor):
        """ Function to click on an anchor element. """
        self.execute_script("arguments[0].scrollIntoView(true);", anchor)
        anchor.click()
        self.wait_until_loaded()

    def hover(self, element):
        """ Function to move mouse cursor to the given element. """
        hover_chain = ActionChains(self.__driver).move_to_element(element)
        hover_chain.perform()
        self.wait_until_loaded()

    def get_z_index(self, element):
        """ Function to find the css z-index property of given element. """
        try:
            z_index = self.getValueOfCSSProperty(element, "z-index")

            # Return the property of a parent element if the property is 'auto' for this element.
            if z_index == 'auto':
                try:
                    parent = element.find_element(By.XPATH, "..")
                    return self.get_z_index(parent)
                except InvalidSelectorException:
                    return -1
            else:
                return int(z_index)
        except StaleElementReferenceException as e:
            logger.error('Exception inside get_z_index: %s' % e.__str__())
            # self.screenshot('page_tiffany_get_z_index.png')
            return -1

    def remove_divs_by_z_index(self, min_z_index):
        """ Function to remove div tags with higher z-index then the given minimum value. """
        elements = self.find_elements_by_tag_name('div')  # TODO: change to all tag names
        sorted_elements = sorted(elements, key=self.get_z_index, reverse=True)

        for element in sorted_elements:
            try:
                z_num = self.get_z_index(element)
                if z_num <= min_z_index:
                    break
                z_index = self.getValueOfCSSProperty(element, "z-index")
                inner = self.getInnerHTML(element)
                logger.info('removing element with z-index %s, %s' % (z_index, inner))
                self.remove_element(element)

            except StaleElementReferenceException as _:
                pass

    def processPageTitle(self, title):
        """ Function to process the page title and remove/replace unwanted charaters. """
        try:
            unwantedCharacters = ['|', '/', '\\', '&', '*', '~', '`', '^', '.', ':', '=', ',']
            if title is not None:
                for char in unwantedCharacters:
                    if char in title:
                        title = title.replace(char, '_')

        except Exception as e:
            logger.error("Exception inside processPageTitle ==> %s" % e.__str__())
        
        return title

    def click_modal_window(self, min_z_index, names, exclude_names):
        """ Function to find the element to click on and click it. """
        buttons = self.find_elements_by_tag_name('button')
        anchors = self.find_elements_by_tag_name('a')
        inputs = self.find_elements_by_tag_name('input')

        elements = buttons + anchors

        def checkIfNameIn(text):
            """ Function to check if a name from names list is in the inner HTML. """
            for name in exclude_names:
                if name in text:
                    return False
            
            for name in names:
                if name in text:
                    return True
            
            return False

        filtered_elements = []
        for element in elements:
            if not self.isDisplayed(element):
                continue
            inner = self.getInnerHTML(element).lower()
            passed = checkIfNameIn(inner)
            if not passed:
                continue
            z_index = self.getValueOfCSSProperty(element, "z-index")
            z_index_inherited = self.get_z_index(element)
            #print('%s %s %s' % (z_index_inherited, z_index, inner))
            if z_index_inherited <= min_z_index:
                continue
            filtered_elements.append(element)
            # logger.info(z_index)
            # logger.info(z_index_inherited)

        inputs_filtered = []

        for element in inputs:
            if not self.isDisplayed(element):
                continue
            type = self.getAttribute(element, "type")
            if type is None or type.lower()!='submit':
                continue
            value = self.getAttribute(element, "value")

            passed = checkIfNameIn(value)
            if not passed:
                continue
            z_index = self.getValueOfCSSProperty(element, "z-index")
            z_index_inherited = self.get_z_index(element)
            #print('%s %s %s' % (z_index_inherited, z_index, inner))
            if z_index_inherited <= min_z_index:
                continue
            inputs_filtered.append(element)

        filtered_elements += inputs_filtered

        if len(filtered_elements) == 0:
            return False

        max_element = max(filtered_elements, key=lambda element: self.get_z_index(element))
        max_val = self.get_z_index(max_element)
        elements_to_click = [element for element in filtered_elements if self.get_z_index(element) == max_val]

        def names_order(element, names):
            """ Function to get the  """
            inner = self.getInnerHTML(element).lower()
            for idx, name in enumerate(names):
                if name in inner:
                    return idx
            return -1

        element_to_click = min(elements_to_click, key=lambda element: names_order(element, names))

        inner = self.getInnerHTML(element_to_click)
        logger.info('Pressing %s, %s' % (element_to_click.tag_name, inner))
        #self.hover(element_to_click)
        self.click_element(element_to_click)
        try:
            self.click_element(element_to_click)

        except StaleElementReferenceException as e:
            logger.error(e)

        if inner is not None:
            #self.info_close_button = re.sub('\s+', ' ', inner).strip()
            inner = re.sub('\s+', ' ', inner).strip()
            logger.info("Modal window was closed by clicking %s" % inner)

        return True


class seleniumModule:
    """ Selenium class to fetch page Content. """

    def __init__(self, headless=True, browser='chrome', load_images=True):
        self.driver = Driver(browser, headless, load_images)

        # logging = logging.getlogging('selenium')
        # logging = logging
        # logging = logging.loggingAdapter(logging, {'processID': os.getpid()})

        self.MAX_BROWSER_RESTARTS = 0

    def getPageContent(self, URL: PDP_URL, keepAlive=False):
        """ Function to fetch the page content. """
        try:
            pageContent, message = None, ""
            url = URL.getURL()
            waitUntil, takeScreenShot = URL.getParam('timeout'), URL.getParam('get_screenshot')
            clickButtons, scroll_to_end = URL.getParam('click_buttons'), URL.getParam('scroll_to_end')
            logger.info(clickButtons)

            # Check if the browser was opened or not.
            if not self.driver.checkIfBrowsersIsOpened():
                # if retry < self.MAX_BROWSER_RESTARTS:
                #     self.driver.restartDriver()
                #     logger.info("%s -- Retrying after relaunching the driver." % url)
                #     return self.getPageContent(keepAlive, retry+1)

                # return pageContent
                self.driver.initializeDriver()

                if not self.driver.checkIfBrowsersIsOpened():
                    # self.driver.restartDriver()
                    self.driver.initializeDriver()
                    # self.close()

                    return pageContent, "Could not launch browser!"

            self.driver.goToURL(url, waitUntil=waitUntil)

            if clickButtons:
                for clickButton in clickButtons:
                    logger.info(clickButton)
                    try:
                        if isinstance(clickButtons, str):
                            clickButton = json.loads(clickButton)

                        if not clickButton.get('xpath', False):
                            logger.info(f"No click xpath found for {clickButton}")
                            continue

                        if clickButton.get('ifnotexist', False):
                            logger.info(f"Checking if an element exists at {clickButton['ifnotexist']} before clicking the button.")
                            elementExists = self.driver.find_elements_by_xpath(clickButton['ifnotexist'])
                            logger.info(f"Matched Elements: {elementExists}")
                            if not elementExists:
                                logger.info(f"No elements found, finding the element to click at {clickButton['xpath']}")
                                clickElement = self.driver.find_elements_by_xpath(clickButton['xpath'])
                                logger.info(f"Matched Elements: {clickElement}")
                                if clickElement:
                                    self.driver.click_element(clickElement[0])
                                    time.sleep(int(clickButton.get('wait_after', 2)))

                            else:
                                logger.info(f"The elements exist at the given xpath. Not clicking the button!!!")

                        else:
                            clickElement = self.driver.find_elements_by_xpath(clickButton['xpath'])
                            logger.info(f"Matched Elements: {clickElement}")
                            if clickElement:
                                self.driver.click_element(clickElement[0])
                                time.sleep(int(clickButton.get('wait_after', 2)))

                    except Exception as e:
                        logger.error(f"Exception while processing {clickButton} {traceback.format_exc()}")

            if scroll_to_end:
                self.driver.scroll_down_smoothly()
            pageContent = self.driver.getPageHTML()
            doWait, matchElement = self.driver.checkIfNeedToWaitMore(pageContent)
            if doWait:
                logger.info("%s --> Fetched Content length is only %d. (After waiting more) Fetching the page content..." % (url, len(pageContent)))
                logger.info(f"{url} --> wait more Match found at {matchElement}")
                time.sleep(5)
            pageContent = self.driver.getPageHTML()            

            if takeScreenShot and configuration.ALLOW_SCREENSHOTS:
                _, urlDomain = URL.getURLComponent('domain')
                pageTitle = self.driver.getPageTitle()
                if pageTitle is None:
                    pageTitle = '_'

                self.driver.screenshot("%s/%s_%s_selenium_%s_Screenshot.png"%(configuration.parent_path, urlDomain, pageTitle, 'Headless' if self.driver.headless else 'Headed'))

            if not keepAlive:
            #     # self.driver.restartDriver()
                self.close()
            
            message = 'SUCCESS'

        except WebDriverException as e:
            logger.error("%s -- Exception with the webdriver inside getPageContent --> %s" % (url, e.__str__()))
            # if retry < self.MAX_BROWSER_RESTARTS:
            #     self.driver.restartDriver()
            #     logger.info("%s -- Retrying after relaunching the driver." % url)
            #     return self.getPageContent(keepAlive, retry+1)
            if not self.driver.headless:
                self.close()
            # elif not keepAlive:
            self.driver.restartDriver()
                # self.close()

        except Exception as e:
            logger.error("%s -- Exception inside getPageContent --> %s" % (url, e.__str__()))

            if not keepAlive:
            #     # self.driver.restartDriver()
                self.close()
            
            message = str(e)

        return pageContent, message
    
    def getPageContent_batched(self, URLs: list[PDP_URL])-> list:
        """ To get page content batches. A browser is opened and closed at the start and end of each batch. """
        try:
            self.driver.initializeDriver()
            if not self.driver.checkIfBrowsersIsOpened():
                # self.driver.restartDriver()
                self.driver.initializeDriver()

                if not self.driver.checkIfBrowsersIsOpened():
                    return

            for index, (url, URL) in enumerate(URLs.items()):
                try:
                    pageContent = None
                    waitUntil, takeScreenShot, rateLimit = URL.getParam('timeout'), URL.getParam('get_screenshot'), URL.getParam('rate_limit')
                    logger.info("Batched: Working on {}/{} - {} url. Using {} timeout.".format(index+1, len(URLs), url, waitUntil))

                    self.driver.goToURL(url, waitUntil=waitUntil)
                    pageContent = self.driver.getPageHTML()

                    doWait, matchElement = self.driver.checkIfNeedToWaitMore(pageContent)
                    if doWait:
                        logger.info("Batched: %s --> Fetched Content length is only %d. (After waiting more) Fetching the page content..." % (url, len(pageContent)))
                        logger.info(f"Batched: {url} --> wait more Match found at {matchElement}")
                        time.sleep(5)
                        pageContent = self.driver.getPageHTML()

                    URLs[url].setParam('html', pageContent)

                    if takeScreenShot and configuration.ALLOW_SCREENSHOTS:
                        _, urlDomain = URL.getURLComponent('domain')
                        pageTitle = self.driver.getPageTitle()
                        if pageTitle is None:
                            pageTitle = '_'

                        self.driver.screenshot("%s/%s_%s_selenium_%s_Screenshot.png"%(configuration.parent_path, urlDomain, pageTitle, 'Headless' if self.driver.headless else 'Headed'))

                except WebDriverException as e:
                    logger.error("Batched: Webdriver exception inside getPageContent_batched-for loop ==> %s" % str(e))
                    self.driver.restartDriver()

                except Exception as e:
                    logger.error("Batched: Exception inside getPageContent_batched-for loop ==> %s" % str(e))

                logger.info("URL: {}, Fetched Content legnth: {}.".format(url, len(pageContent) if pageContent is not None else 0))
                logger.info("Batched: Sleeping for {} seconds to rate limit.".format(rateLimit))
                if index < len(URLs) - 1:
                    time.sleep(rateLimit)

        except Exception as e:
            logger.error("Batched: Exception inside getPageContent_batched ==> %s" % str(e), exc_info=True)

        finally:
            self.close()

    def getPageContent_ExistingBrowser(self, retry=0):
        """ Function to fetch the page content of urls in bacthes. """
        pass

    def close(self):
        """ Function to close the driver. """
        try:
            self.driver.closeDriver()
        
        except Exception as e:
            logger.error("Exception inside seleniumModule.close method ==> %s" % e.__str__())

    def preprocessing_for_finchat(self):
        """
        Prepares the page for required data.
        """
        inr_currency = self.driver.find_elements_by_xpath("//label[contains(text(), 'INR') and not(@data-active)]")
        if inr_currency:
            # self.driver.click_element(inr_currency[0])
            inr_currency[0].click()
        self.wait_loading_finchat("//table")
        value_in_K = self.driver.find_elements_by_xpath("//label[text()='K' and not(@data-active)]")
        if value_in_K:
            # self.driver.click_element(value_in_K[0])
            value_in_K[0].click()
        self.wait_loading_finchat("//table")

    def wait_loading_finchat(self, xpath: str):
        """
        Waits till the table is not loaded on the page.
        """
        counter = 0
        while counter < 10:
            counter += 1
            time.sleep(2)
            table_element = self.driver.find_elements_by_xpath(xpath)
            if table_element:
                break

    def parse_and_scrape_finchat(self, company_name: str, callback_function):
        """
        Parses all the sections and subsections for given company and creates a csv file for each.
        """
        def find_section_name_from_tab_id(section_id: str)-> str:
            """ 
            Finds the tab name from button tag id.
            Eg., mantine-jrbj3hbve-tab-Balance Sheet ==> Balance Sheet ==> returns Balance-Sheet
            """
            return re.sub(r"\s+", "-", section_id.split('tab-')[1])

        try:
            URL = PDP_URL(f"https://finchat.io/company/{company_name}", timeout=120)

            html, message = self.getPageContent(URL, keepAlive=True)
            if html:
                self.preprocessing_for_finchat()

                sections = self.driver.find_elements_by_xpath("//div[contains(@class, 'mantine-Card-root')]//div[contains(@class, 'mantine-Tabs-root')]//button[contains(@class, 'mantine-Tabs-tab')]")
                logger.info(sections)

                for section in sections:
                    section_name = find_section_name_from_tab_id(section.get_attribute('id'))
                    if section.get_attribute('aria-selected') != 'true':
                        # self.driver.click_element(section)
                        section.click()
                        self.wait_loading_finchat(f"//button[contains(@id, 'tab-{section_name}') and @aria-selected='true']")

                    sub_sections = self.driver.find_elements_by_xpath("//div[contains(@class, 'mantine-Card-root')]//div[contains(@class, 'mantine-Paper-root')]/div[contains(@class, 'mantine-Tabs-root')]//button[contains(@class, 'mantine-Tabs-tab')]")
                    if not sub_sections:
                        sub_sections = ['main']

                    for sub_section in sub_sections:
                        if (not isinstance(sub_section, str)) and sub_section.get_attribute('aria-selected') != 'true':
                            # self.driver.click_element(sub_section)
                            sub_section.click()
                            self.wait_loading_finchat(f"//button[contains(@id, 'tab-{sub_section_name}') and @aria-selected='true']")

                        if not isinstance(sub_section, str):
                            sub_section_name = find_section_name_from_tab_id(sub_section.get_attribute('id'))
                        else:
                            sub_section_name = 'main'

                        for data_duration in ['Annual', 'Quarterly', 'Semi', 'Trailing']:
                            logger.info(f"Working on {section_name}_{sub_section_name}_{data_duration}")
                            data_duration_selector = self.driver.find_elements_by_xpath(f"//label[text()='{data_duration}']")
                            if data_duration_selector and (not data_duration_selector[0].get_attribute('data-active')):
                                # self.driver.click_element(data_duration_selector[0])
                                data_duration_selector[0].click()
                                self.wait_loading_finchat("//table")

                            html = self.driver.getPageHTML()
                            callback_function(html, company_name, f"{section_name}_{sub_section_name}_{data_duration}")

            else:
                logger.info(f"Couldn't load page for {company_name}, Message from FPM: {message}")

        except Exception as e:
            logger.error(f"Exception inside parse_and_scrape_finchat ==> {traceback.format_exc()}")
