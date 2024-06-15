from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright, Playwright, ElementHandle, Page, Response, Request, Route
from playwright_stealth import stealth_sync, stealth_async, StealthConfig
import psutil, asyncio, time, json, re, os, random, traceback, subprocess, math
from collections import defaultdict
from amazoncaptcha import AmazonCaptcha

import configuration
from loggers import Logger
logger = Logger().get_logger('playwright')

from utils import PDP_URL
from exceptions import FailedOpenNewPage, FailedOpenNewBrowser, PageIsClosed, RetryGotoURL, RetryGetPageContent
from tenacity import retry, retry_if_exception_type, wait_exponential, wait_random, stop_after_attempt


class playwrightModule:
    """ Pupeeteer class to fetch page content using pypeteer. """

    def __init__(self, headless=True, browser='chrome', use_proxy=False):
        self.headless = headless

        # self.page=None
        self.__browserType = browser
        self.__browser = None
        self.__browserProcessID = None
        self.use_proxy = use_proxy

        # self.userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36"
        # self.userAgent = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

        self.sleepTime = 2

        self.closeTexts = ['continue', 'no', 'start shopping', 'shop now', 'no thanks', 'not right now', 'decline offer', 'only required', 'stay on', 'reject', 'accept', 'allow', 'cookies']
        self.closeTextsToExclude = ['policy', 'use of cookies', 'set cookies']
        self.close_z_index = 100
        self.scroll_down = 5000

        self.previouslyClickedElements = defaultdict(list) # A dict of lists with sublists containning (elementHandle, elementInnerHTML, Order in the self.closeTexts list)

        # self.loop = None

        # Launch browser
        # browserTask = asyncio.create_task(self.launchBrowser())
        # browserTask.set_name('launchBrowser')
        # browserTask_shielded = asyncio.shield(browserTask)
        # loop = asyncio.new_event_loop()
        # loop.run_until_complete()

        self.mainPage = None
        self.runner = asyncio.Runner()

    def processPageTitle(self, title):
        """ Function to process the page title and remove/replace unwanted charaters. """
        try:
            unwantedCharacters = ['|', '/', '\\', '&', '*', '~', '`', '^', '.', ':', '=', ',', '?', '*']
            if title is not None:
                for char in unwantedCharacters:
                    if char in title:
                        title = title.replace(char, '_')

        except Exception as e:
            logger.error("Exception inside processPageTitle ==> %s" % e.__str__())
        
        return title

    def getUserAgent(self):
        """ Function to get the user Agent of given object. """
        userAgent = None
        if self.__browser is not None:
            userAgent = self.__browser.userAgent()
            return userAgent
        
        return userAgent

    def getNextUserAgent(self)-> tuple:
        """ Function to get random userAgent with appropriate OS name. """
        # logger.info("Using Chrome version: %s" % configuration.CHROME_VERSION)
        OS_names = ['Linux', 'Mac OS', 'Win64', 'CrOS', 'WOW64']

        userAgentIndex = random.randint(0, len(configuration.userAgents[self.__browserType])-1)
        userAgent = configuration.userAgents[self.__browserType][userAgentIndex]
        for os_name in OS_names:
            if os_name in userAgent:
                return userAgent, os_name

        return userAgent, OS_names[0]
    
    def getPageContent(self, URL: PDP_URL, keepAlive=False):
        """ Function to fetch content for given URL. """
        try:
            pageContent, message = None, ""
            pageContent, message = self.runner.run(self.getPageContentCoroutine(URL, keepAlive))

        except Exception as e:
            logger.error(f"Exception inside getPageContent ==> {str(e)}")
            message = str(e)

        return pageContent, message

    @retry(
        retry=retry_if_exception_type((RetryGetPageContent)),
        reraise=True,
        wait=wait_exponential(multiplier=1, max=5) + wait_random(0, 3),
        stop=stop_after_attempt(1)
    )
    async def getPageContentCoroutine(self, URL: PDP_URL, keepAlive=False):
        """ Coroutine to fetch the page content. """
        try:
            self.playwrightObj = await async_playwright().start()

            url = URL.getURL()
            _, self.urlDomain = URL.getURLComponent('domain')

            noLoadScreenshot, playwright_loadEvent = URL.getParam('save_screenshot_if_could_not_load'), URL.getParam('page_load_event_playwright')
            timeout, takeScreenShot, clickButtons = URL.getParam('timeout'), URL.getParam('get_screenshot'), URL.getParam('click_buttons')
            scroll_to_end = URL.getParam('scroll_to_end')

            pageContent = None
            if not self.checkIfBrowserIsOpened():
                await self.launchBrowser()

                if not self.checkIfBrowserIsOpened():
                    # if not keepAlive:
                    # self.relaunchBrowser()
                    await self.launchBrowser()
                    # self.closeBrowser()

                if not self.checkIfBrowserIsOpened():
                    return pageContent, "Could not start the browser instance!!"

            # pageClosed = self.checkIfPageIsClosed(page)
            # if pageClosed:
            try:
                if self.mainPage is None:
                    self.mainPage = await self.openNewPage()

                    if self.mainPage is None:
                        # self.relaunchBrowser()
                        # self.mainPage = self.openNewPage()
                        logger.error("Some error occured while opening the page.")
                        # if self.mainPage is None:
                        if not keepAlive:
                            # self.relaunchBrowser()
                            await self.closeBrowser()
                        return pageContent, "Error while opening a new page."

            except Exception as e:
                raise FailedOpenNewPage("Playwright failed to open a new page with %s error." % str(e))

            try:
                loaded = await self.gotoURL(url, self.mainPage, playwright_loadEvent, timeout=timeout)

            except PageIsClosed as e:
                logger.info(f"PageIsCloed: {str(e)} ==> Reopening the page")
                self.mainPage = await self.openNewPage()

                if self.mainPage is None:
                    # self.relaunchBrowser()
                    # self.mainPage = self.openNewPage()
                    logger.error("Some error occured while Re-opening the page.")
                    # if self.mainPage is None:
                    if not keepAlive:
                        # self.relaunchBrowser()
                        await self.closeBrowser()

                    return pageContent, "Error while opening a new page."

                else:
                    loaded = await self.gotoURL(url, self.mainPage, playwright_loadEvent, timeout=timeout)

            if loaded == -1:
                # logger.info("URL not loaded retrying once...")
                # self.reloadPage(page)

                # # Pass in retry=True this time so that, the page will be till waiting for documentloaded event is fired instead of networkidle0.
                # loaded = self.gotoURL(page, url)

                # if loaded == -1:
                logger.info("%s -- Couldn't load the URL!!!" % url)
                if noLoadScreenshot:
                    try:
                        pageTitle = self.processPageTitle(URL.getURLComponent('path')[-1])
                        if '.' in pageTitle:
                            pageTitle = pageTitle.split('.')[0]
                        if pageTitle is None:
                            pageTitle = '_'

                        await self.screenshot(self.mainPage, "%s/%s_%s_playwright%sScreenshot.png"%(configuration.parent_path, self.urlDomain, pageTitle, 'Headless' if self.headless else 'Headed'))

                    except Exception as e:
                        logger.error("%s --> Exception while taking a screenshot beacuse of faild to load page. ==> %s" % (url, e.__str__()))

                if not keepAlive:
                    # self.relaunchBrowser()
                    await self.closeBrowser()
                return pageContent, "Could not load the webpage."

            if clickButtons:
                for clickButton in clickButtons:
                    try:
                        if isinstance(clickButtons, str):
                            clickButton = json.loads(clickButton)

                        if not clickButton.get('locator', False):
                            logger.info(f"No click locator found for {clickButton}")
                            continue

                        await self.click_button_by_locator(self.mainPage, clickButton['locator'])
                        time.sleep(int(clickButton.get('wait_after', 2)))

                    except Exception as e:
                        logger.error(f"Exception while processing {clickButton} {traceback.format_exc()}")

            if scroll_to_end:
                await self.scroll_down_smoothly(self.mainPage)
            # pageTitle = self.getPageTitle(page)
            pageContent = await self.getPageHTML(self.mainPage, url)

            if takeScreenShot and configuration.ALLOW_SCREENSHOTS:
                pageTitle = await self.getPageTitle(self.mainPage)
                pageTitle = self.processPageTitle(pageTitle)
                if pageTitle is None:
                    pageTitle = '_'

                await self.screenshot(self.mainPage, "%s/%s_%s_playwright%sScreenshot.png"%(configuration.LOGS_FOLDER, self.urlDomain, pageTitle, 'Headless' if self.headless else 'Headed'))

            # pageClosed = self.checkIfPageIsClosed(self.mainPage)
            # if not pageClosed:
            # self.close_page(self.mainPage)

            if not keepAlive:
            #     # self.relaunchBrowser()
                await self.closeBrowser()

            return pageContent, 'SUCCESS'

        except Exception as e:
            logger.error("%s -- Exception inside getPageContentCoroutine ==> %s" % (url, e.__str__()))

            if not keepAlive:
            #     self.relaunchBrowser()
                await self.closeBrowser()

            return pageContent, 'Error while processing the request: %s' % str(e)

    async def getPageContent_batched(self, URLs: list[PDP_URL]):
        """ Coroutine to fetch the page content. """
        try:
            if not self.checkIfBrowserIsOpened():
                self.launchBrowser()

                if not self.checkIfBrowserIsOpened():
                    self.launchBrowser()

                if not self.checkIfBrowserIsOpened():
                    return

            try:
                if self.mainPage is None:
                    self.mainPage = self.openNewPage()

                    if self.mainPage is None:
                        # self.relaunchBrowser()
                        self.mainPage = self.openNewPage()

                        if self.mainPage is None:
                            self.closeBrowser()

            except Exception as e:
                raise FailedOpenNewPage("Playwright failed to open a new page with %s error." % str(e))

            # Use Strealth plugin to hide all Playwright activities
            # stealth_sync(
            #     self.mainPage,
            #     user_agent=self.userAgent
            # )

            for index, (url, URL) in enumerate(URLs.items()):
                try:
                    # url = URL.getURL()
                    playwright_loadEvent, timeout, rateLimit = URL.getParam('page_load_event_playwright'), URL.getParam('timeout'), URL.getParam('rate_limit')
                    _, self.urlDomain = URL.getURLComponent('domain')

                    logger.info("Batched: Working on {}/{} - {} url. Using '{}' playwright_loadEvent and '{}' timeout.".format(index+1, len(URLs), url, playwright_loadEvent, timeout))

                    loaded = self.gotoURL(url, self.mainPage, playwright_loadEvent if playwright_loadEvent in {'load', 'networkidle2', 'networkidle0', 'domcontentloaded'} else 'load', timeout=timeout)
                    if loaded == -1:
                        logger.info("Page not loaded, opening a new page and reloading the URL.")
                        self.mainPage = self.openNewPage()
                        loaded = self.gotoURL(url, self.mainPage, playwright_loadEvent if playwright_loadEvent in {'load', 'networkidle2', 'networkidle0', 'domcontentloaded'} else 'load', timeout=timeout)

                        if loaded == -1:
                            continue

                    # pageTitle = self.getPageTitle(page)
                    pageContent = self.getPageHTML(self.mainPage, url)
                    URLs[url].setParam('html', pageContent)

                    if URL.getParam('get_screenshot') and configuration.ALLOW_SCREENSHOTS:
                        pageTitle = await self.getPageTitle(self.mainPage)
                        pageTitle = self.processPageTitle(pageTitle)
                        if pageTitle is None:
                            pageTitle = '_'


                        self.screenshot(self.mainPage, "%s/%s_%s_playwright%sScreenshot.png"%(configuration.parent_path, self.urlDomain, pageTitle, 'Headless' if self.headless else 'Headed'))

                except Exception as e:
                    logger.error("Exception inside getPageContent_batched-for loop ==> %s" % str(e))

                logger.info("URL: {}, Fetched Content legnth: {}.".format(url, len(pageContent) if pageContent is not None else 0))
                logger.info("Batched: Sleeping for {} seconds to rate limit.".format(rateLimit))
                if index < len(URLs) - 1:
                    time.sleep(rateLimit)

        except Exception as e:
            logger.error("%s -- Exception inside getPageContent_batched ==> %s" % (url, e.__str__()))

        finally:
            self.closeBrowser()

    def getRandomProxyPort(self):
        port = random.randint(10000, 11000)
        logger.info(f"Using {port} for proxy!")
        return port

    async def launchBrowser(self):
        """ Function to launch the browser instance. """
        try:
            if self.__browserType == 'chrome':
                logger.info("Launching a Chrome %s browser..."%'headless' if self.headless else 'headed')
                self.userAgent, _ = self.getNextUserAgent()
                logger.info("Using %s user Agent" % self.userAgent)

                browser_args = [
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    f"--window-size={configuration.DISPLAY_SIZE_STRING}",
                    "--user-agent=%s"%self.userAgent,
                    "--disable-features=IsolateOrigins,site-per-process",
                    '--disable-gpu',
                    '--blink-settings=imagesEnabled=true',
                    '--enable-javascript',
                    '--incognito',
                    '--aggressive-cache-discard',
                    '--disable-cache',
                    '--disable-application-cache',
                    '--disable-offline-load-stale-cache',
                    '--disable-gpu-shader-disk-cache',
                    '--media-cache-size=0',
                    '--disk-cache-size=0',
                    '--mute-audio',
                    '--disable-default-apps',
                    '--no-default-browser-check',
                    '--disable-background-timer-throttling',
                    '--block-new-web-contents',
                    '--disable-dev-shm-usage'
                ]

                # browser_type = playwright.chromium if self.headless else playwright.chromium.launcher
                self.__browser = await self.playwrightObj.chromium.launch(
                    headless=self.headless,
                    channel='chrome',
                    # ignore_default_args=True,
                    args=browser_args,
                    executable_path=configuration.CHROME,
                    slow_mo=0,
                    handle_sigint=False,
                    handle_sigterm=False,
                    handle_sighup=False,
                    proxy={
                        "server": f"{configuration.PROXY_HOST}:{configuration.PROXY_PORT}",
                        "username": configuration.PROXY_USER,
                        "password": configuration.PROXY_PASSWORD
                    } if self.use_proxy else None
                )
                logger.info(self.__browser)
                # self.__browserProcessID = self.__browser.process.pid
                # logger.info(f"Created a Chrome browser process: {self.__browserProcessID}")

            # elif self.__browserType == 'firefox':
            #     logger.info("Launching a Firefox %s browser..."%'headless' if self.headless else 'headed')
            #     self.userAgent, _ = self.getNextUserAgent()
            #     logger.info("Using %s user Agent" % self.userAgent)

            #     # browser_type = playwright.chromium if self.headless else playwright.chromium.launcher
            #     self.__browser = await self.playwrightObj.firefox.launch(
            #         headless=self.headless,
            #         channel='firefox-stable',
            #         args=[
            #             "--no-sandbox",
            #             "--disable-setuid-sandbox",
            #             f"--window-size={configuration.DISPLAY_SIZE_STRING}",
            #             "--user-agent=%s" % self.userAgent,
            #             "--disable-features=IsolateOrigins,site-per-process",
            #             "--disable-gpu",
            #             "--blink-settings=imagesEnabled=true",
            #             "--enable-javascript",
            #             "--private-window",  # Use private browsing mode (incognito)
            #             "--mute-audio",
            #             "--disable-extensions",
            #             "--disable-default-apps",
            #             "--no-default-browser-check",
            #             "--disable-background-timer-throttling",
            #             "--disable-new-tab-first-run",
            #             "--disable-session-crashed-bubble",
            #             "--disable-offline-load-stale-cache",
            #             "--disable-background-networking",
            #             "--disable-backgrounding-occluded-windows",
            #             "--disable-background-timer-throttling",
            #             "--disable-backgrounding-occluded-windows",
            #             "--disable-breakpad",
            #             "--disable-client-side-phishing-detection",
            #             "--disable-component-update",
            #             "--disable-default-apps",
            #             "--disable-domain-reliability",
            #             "--disable-extensions",
            #             "--disable-features=TranslateUI",
            #             "--disable-hang-monitor",
            #             "--disable-infobars",
            #             "--disable-notifications",
            #             "--disable-popup-blocking",
            #             "--disable-print-preview",
            #             "--disable-prompt-on-repost",
            #             "--disable-renderer-backgrounding",
            #             "--disable-sync",
            #             "--disable-translate",
            #             "--disable-windows10-custom-titlebar",
            #             "--disk-cache-size=0",
            #             "--media-cache-size=0",
            #             "--disable-dev-shm-usage"
            #         ],
            #         # executable_path=configuration.FIREFOX,
            #         slow_mo=0,
            #         handle_sigint=False,
            #         handle_sigterm=False,
            #         handle_sighup=False,
            #     )

            #     # self.__browserProcessID = self.__browser.process.pid
            #     logger.info("Created a Firefox browser process: %d" % self.__browserProcessID)

            else:
                raise FailedOpenNewBrowser("Playwright could open a new browser. Browser Type: {}".format(self.__browserType))

        except Exception as e:
            logger.error("Exception inside launchBrowser ==> %s"%e.__str__(), exc_info=True)

        return

    def checkIfBrowserIsOpened(self):
        """ Function to check if the browser was opened or not. """
        return self.__browser is not None

    def checkIfNeedToWaitMore(self, htmlText):
        """ Function to check if given html text is of loaded page or some other redirected page. """
        siteLoadingText = [
            r"checking if the site connection is secure"
        ]

        for text in siteLoadingText:
            regex = re.compile(r"%s" % text, re.I)
            matchFound = regex.search(htmlText)
            if matchFound is not None:
                # logger.info(f"Match found at {matchFound}.")
                return True, matchFound

        return False, None

    async def closeBrowser(self):
        """ Coroutine to close the Playwright instance. """
        try:
            logger.info("Playwright (%s) ==> Closing the browser..." % 'headless' if self.headless else 'headed')
            if self.__browser:
                logger.info("Closing browser instance...")
                try:
                    await self.__browser.close()

                except Exception as e:
                    logger.error("Exception when closing browser. ==> %s"%e.__str__())

                if self.__browserProcessID is not None:
                    browserProcess = psutil.Process(self.__browserProcessID)
                    if psutil.pid_exists(self.__browserProcessID):
                        browserProcessChildren = browserProcess.children(recursive=True)

                        for childProces in browserProcessChildren:

                            if psutil.pid_exists(childProces.pid):
                                logger.info("Killing browser child process %d"%childProces.pid)
                                childProces.kill()

                        try:
                        # if psutil.pid_exists(self.__browserProcessID):
                            logger.info("Killing browser process: %d"%self.__browserProcessID)
                            browserProcess.kill()

                        except Exception as e:
                            pass

        except Exception as e:
            logger.error("Exception inside closeBrowser ==> %s"%e.__str__())
            if self.__browserProcessID is not None and psutil.pid_exists(self.__browserProcessID):
                logger.info("Killing browser process: %d"%self.__browserProcessID)
                browserProcess.kill()

        finally:
            self.__browser = None
            self.__browserProcessID = None
            self.mainPage = None

    # async def route_intercept(route: Route):
    #     logger.info(route.request.url)
    #     if route.request.resource_type == "image":
    #         logger.info(f"Blocking the image request to: {route.request.url}")
    #         return route.abort()
    #     if re.findall(r"(\.png|\.jpg|\.jpeg|\.gif)", route.request.url):
    #         logger.info(f"Blocking the image request to: {route.request.url}")
    #         return route.abort()

    #     return route.continue_()

    async def relaunchBrowser(self):
        """ Coroutine to relaunch the browser instance. """
        try:
            logger.info("Playwright (%s) ==> Relauching the browser..." % 'headless' if self.headless else 'headed')
            await self.closeBrowser()

        except Exception as e:
            logger.error("Exception inside relaunchBrowser ==> %s"%e.__str__())

        finally:
            await self.launchBrowser()

    async def openNewPage(self):
        """ Coroutine to open a new page. """
        try:
            page, browserOpen = None, self.checkIfBrowserIsOpened()
            if browserOpen:
                logger.info("Opening a new page...")
                page = await self.__browser.new_page()

                # page.setCacheEnabled(False)

                # self.addPlugins(page)

                # Use Strealth plugin to hide all Playwright activities
                # stealth_sync(page)
                await stealth_async(page, config=StealthConfig(
                    nav_user_agent=self.userAgent
                ))
                page.on("request", lambda request: asyncio.ensure_future(self.request_actions(request)))
                page.on("response", lambda response: asyncio.ensure_future(self.response_actions(response)))
                await page.route(re.compile(r"(\.png)|(\.jpg)|(\.jpeg)|(\.gif)|(\.js)"), lambda route: route.abort())

            # page.setDefaultNavigationTimeout(60*1000)

        except Exception as e:
            logger.error("Exception inside openNewPage ==> %s"%e.__str__(), exc_info=True)

        return page
    
    async def request_actions(self, request: Request)-> None:
        # if request.url.startswith("https://www.amazon.com"):
        logger.info(f"Request ==> {request.method}-{request.url} ==> {(await request.all_headers())}")

    async def response_actions(self, response: Response)-> None:
        if response.status == 407 and response.request.url.startswith("https://www.amazon.com"):
            logger.info(f"Received {response.status} from {response.request.url}, retrying!")
            await self.relaunchBrowser()
            # raise RuntimeError(f"Couldn't authenticate with the API!")
            raise RetryGotoURL(f"Received {response.status}")

    async def close_page(self, page):
        try:
            pageClosed = self.checkIfPageIsClosed(page)
            logger.info("Page is Closed?: {}".format(pageClosed))
            if not pageClosed:
                logger.info("Closing the page...")
                await page.close()

        except Exception as e:
            logger.error("Exception inside close_page ==> %s" % (e.__str__()))

    # async def addPlugins(self, page, count: int = 3):
    #     " To add random plugins to the page. "
    #     logger.info("Adding some random plugins to the Playwright Page. ")
    #     plugins_array = ','.join(str(i) for i in range(count))
    #     await page.evaluateOnNewDocument(
    #         'Object.defineProperty('
    #         'Object.getPrototypeOf(navigator),'
    #         '"plugins",'
    #         '{get() {return [' + plugins_array + ']}})'
    #     )

    async def reloadPage(self, page):
        """ Coroutine to reload the given page. """
        pageClosed = self.checkIfPageIsClosed(page)
        if not pageClosed:
            logger.info("Reloading the page...")
            await page.reload()

    def checkIfPageIsClosed(self, page):
        """ Coroutine to check if given page is closed or not. """
        if page is not None:
            return page.is_closed()

        return True
    
    async def click_element(self, element_handler: ElementHandle, **kwargs)-> bool:
        """ Function to click the give element_handler. """
        try:
            logger.info(f"Clicking the element: {element_handler} Args: {kwargs}")
            await element_handler.scroll_into_view_if_needed()
            await element_handler.click(**kwargs)

        except Exception as e:
            logger.error(f"Exception inside clickElement ==> {traceback.format_exc()}")
            return False

        return True

    @retry(
        retry=retry_if_exception_type((RetryGotoURL)),
        reraise=True,
        wait=wait_exponential(multiplier=1, max=5) + wait_random(0, 3),
        stop=stop_after_attempt(2)
    )
    async def gotoURL(self, url, page: Page = None, playwright_loadEvent='load', timeout=configuration.DEFAULT_TIMEOUT):
        """ Coroutine to go to a URL on given Page. """
        try:
            if page is None:
                page = self.mainPage

            pageClosed = self.checkIfPageIsClosed(page)
            logger.info("Page is Closed?: {}".format(pageClosed))
            if not pageClosed:
                logger.info("%s --> Opening the URL...Waiting for %s event..." % (url, playwright_loadEvent))
                await page.goto(
                    url, 
                    timeout=timeout * 1000,
                    wait_until=playwright_loadEvent
                )
                # hasClicked = self.closeModalWindow(page)
                # time.sleep(2)
                # if hasClicked:
                #     self.wait_until_loaded(page)

                    # Some sites may give a follow-up pop up eg. Mango
                    # hasClicked = self.closeModalWindow(page)
                    # if hasClicked:
                    #     self.wait_until_loaded(page)

                if 'amazon.com' in page.url:
                    page_main_section = await self.find_element(page, "#dp-container", strict=True)
                    if not page_main_section:
                        # time.sleep(60)
                        image_link = await self.find_element(page, "body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-row.a-spacing-large > div > div > div.a-row.a-text-center > img", strict=True)
                        logger.info(image_link)
                        if image_link:
                            image_link = await image_link.get_attribute('src')
                            logger.info(image_link)
                            captcha = AmazonCaptcha.fromlink(image_link)
                            logger.info(captcha)
                            captcha = AmazonCaptcha.solve(captcha)
                            logger.info(captcha)

                            if captcha:
                                captcha_insert = await self.find_element(page, "#captchacharacters", strict=True)
                                logger.info(captcha_insert)

                                if captcha_insert:
                                    await captcha_insert.type(captcha)

                                    submit: ElementHandle = await self.find_element(page, "body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-section.a-spacing-extra-large > div > span > span > button", strict=True)
                                    if submit:
                                        await submit.click()
                                        await self.wait_until_loaded(page)

                if 'macys.com' in page.url:
                    country_selector = await self.find_elements(page, "#href_changeCountry")
                    if country_selector:
                        country_selector = country_selector[0]
                        await self.click_element(country_selector)
                        await page.get_by_label("Choose your location").select_option("US")

                        submit_changes = await self.find_elements(page, "#saveChanges")
                        if submit_changes:
                            submit_changes = submit_changes[0]
                            await self.click_element(submit_changes)

                        await page.goto(
                            url, 
                            timeout=timeout * 1000,
                            wait_until=playwright_loadEvent
                        )

                if 'walmart.com' in page.url:
                    await self.wait_until_loaded(page)
                    main_section = await self.find_element(page, "#maincontent > section > main", strict=True)
                    if not main_section:
                        await self.relaunchBrowser()
                        logger.error(f"Didn't find the main section in page! Relaunched the Browser")
                        await asyncio.sleep(2)
                        raise RetryGetPageContent(f"Didn't find the main section in page! Relaunched the Browser")

                    #cjyDFYcLvZORFJr

                return 1

            else:
                logger.error("Page was unexpectedly closed...")
                # self.mainPage = self.openNewPage()
                raise PageIsClosed("Page was unexpectedly closed in playwright.")

        except PageIsClosed as e:
            self.mainPage = None
            raise

        except Exception as e:
            logger.error(f"Exception inside gotoURL ==> {traceback.format_exc()}")
            return -1

    async def getPageHTML(self, page, url=''):
        """ Coroutine to get the page source code. """
        try:
            pageContent, pageClosed = None, self.checkIfPageIsClosed(page)
            if not pageClosed:
                logger.info("%s --> Fetching the page content..." % url)
                pageContent = await page.content()

            doWait, matchElement = self.checkIfNeedToWaitMore(pageContent)
            if doWait:
                logger.info("%s --> Fetched Content length is only %d. (After waiting more) Fetching the page content..." % (url, len(pageContent)))
                logger.info(f"{url} --> wait more Match found at {matchElement}")
                time.sleep(3)
                pageContent = await page.content()

        except Exception as e:
            logger.error("%s --> Exception inside getPageHTML ==> %s" % (url, e.__str__()))

        return pageContent

    async def checkIfURLWasOpened(self, page, url):
        """ Coroutine to check if a URL was opened or not. """
        logger.info("URL on given page is %s == %s"%(page.url.strip(), url))
        return await page.url.strip() == url

    async def find_elements_by_xpath(self, page, xPath):
        """ Coroutine to find the elements evaluating to given xPath on the passed page. """
        try:
            elements = None
            elements = await page.xpath(xPath)

        except Exception as e:
            logger.error("Exception inside find_elements_by_xpath ==> %s"%e.__str__())

        return elements

    async def evaluateQuery(self, page, query, *args):
        """ Coroutine to evaluate given query on passed page. """
        try:
            result = None
            result = await page.evaluate(query, *args)

            if isinstance(result, str):
                result = result.strip()
        
        except Exception as e:
            logger.error("Exception inside evaluateQuery ==> %s"%e.__str__())
        
        return result

    async def extractTextFromElement(self, page, element):
        """ Coroutine to extract the text from given element. """
        try:
            text = None
            text = await self.evaluateQuery(page, '(element) => element.textContent', element)

        except Exception as e:
            logger.error("Exception inside extractTextFromElement ==> %s"%e.__str__())
        
        return text

    async def extractInnerHTMLFromElement(self, page, element):
        """ Coroutine to extract the text from given element. """
        try:
            innerHTML = None
            innerHTML = await self.evaluateQuery(page, '(element) => element.innerHTML', element)

        except Exception as e:
            logger.error("Exception inside extractTextFromElement ==> %s"%e.__str__())

        return innerHTML

    async def screenshot(self, page, filePath, fullPage=True):
        """ Coroutine to take a screenshot of the page. """
        try:
            if configuration.ALLOW_SCREENSHOTS:
                pageClosed = self.checkIfPageIsClosed(page)
                if not pageClosed and filePath is not None:
                    fileName = filePath.split('/')[-1]
                    await page.screenshot(
                        path=filePath,
                        full_page=fullPage
                    )

        except Exception as e:
            logger.error("Exception inside screenshot ==> %s"%e.__str__())    

    async def click_button_by_locator(self, page, locator: str):
        """ Clicks on a button by the locator. """
        try:
            pageClosed = self.checkIfPageIsClosed(page)
            if not pageClosed:
                logger.info(f"Clicking on {locator}")
                await page.locator(locator).click()

        except Exception as e:
            logger.error(f"Exception while clicking on the button: {traceback.format_exc()}")

    async def find_element(self, page, selector_query: str, strict:bool=False)-> ElementHandle:
        """ Function to find the element evaluating to given JS Selector on the passed page. """
        pageClosed = self.checkIfPageIsClosed(page)
        if not pageClosed:
            logger.info(f"Finding the element at {selector_query}")
            return await page.query_selector(selector_query, strict=strict)

    async def find_elements(self, page, selector_query: str)-> list[ElementHandle]:
        """ Function to find the elements evaluating to given JS Selector on the passed page. """
        try:
            pageClosed = self.checkIfPageIsClosed(page)
            if not pageClosed:
                logger.info(f"Finding the element at {selector_query}")
                return await page.query_selector_all(selector_query)
                # return self.execute_script("(selector_query) => document.querySelectorAll(selector_query);", selector_query)

        except Exception as e:
            logger.error(f"Exception in find_elements ==> {traceback.format_exc()}")

        return []

    async def get_z_index(self, page, element):
        """ 
        Coroutine to get the z-index of given element for passed page. 
        TODO: This function is not working as expected. Do not Use.
        """
        try:
            logger.info("Inside get_z_index...")
            z_index = await self.evaluateQuery(page, "(element) => element.getProperty('zIndex')", element)
            # z_index = element.
            logger.info(z_index)

            if z_index is None:
                return -1

            if z_index in ['initial', '']:
                return -1

            elif z_index.strip() in ['auto', 'inherit']:
                parent = await element.xpath('..')
                if parent:
                    parent_z_index = await self.get_z_index(page, parent[0])
                    return parent_z_index

                return -1
            
            else:
                return int(z_index)

        except Exception as e:
            logger.error("Exception inside get_z_index ==> %s"%e.__str__())
            return -1

    async def isDisplayed(self, element):
        """ Coroutine to check if given element is displayed. """
        elementIsDisplayed = False
        try:
            elementIsDisplayed = await element.isIntersectingViewport()

        except Exception as e:
            logger.error("Exception inside isDisplayed ==> %s"%e.__str__())

        return elementIsDisplayed

    async def getPageTitle(self, page):
        """ Coroutine to get the page title of the page. """
        pageClosed = self.checkIfPageIsClosed(page)
        if not pageClosed:
            return await page.title()

    async def wait_until_loaded(self, page):
        """ Coroutine to wait to till the page is loaded. """
        logger.info("Inside wait_until_loaded method...")
        old_height = await self.evaluateQuery(page, 'window.screen.height')
        logger.info("Current Height is %d"%int(old_height))
        iteration, maxWaitIteration = 0, 3

        # while iteration < maxWaitIteration:
        while True:
            try:
                new_height = await self.evaluateQuery(page, 'window.screen.height')
                logger.info("New Height is %d"%int(new_height))

                if new_height != old_height:
                    logger.info("Page height has changed.")
                    return True
                
                else:
                    time.sleep(self.sleepTime)
                    return

                # iteration += 1

            except Exception as e:
                logger.error("Exception inside wait_until_loaded ==> %s"%e.__str__())
                time.sleep(self.sleepTime)
                return

    async def clickElement(self, element):
        """ Coroutine to click the give element. """
        try:
            await element.click()
        
        except Exception as e:
            logger.error("Exception inside clickElement ==> %s"%e.__str__())
            return False
        
        return True

    async def closeModalWindow(self, page):
        """ Coroutine to close a modal window if detencted. """
        try:
            logger.info("Inside closeModalWindow...")
            element_to_click = []
            if self.previouslyClickedElements.get(self.urlDomain, False):
                minOrder = 9999
                for element, elementInnerHTML, elementOrderInCloseTexts in self.previouslyClickedElements[self.urlDomain]:
                    if await self.isDisplayed(element):
                        if elementOrderInCloseTexts < minOrder:
                            element_to_click = [element, elementInnerHTML, elementOrderInCloseTexts]

            if element_to_click:
                logger.info("Picked element from cache, Clicking %s..."%element_to_click[1])

                clicked = self.clickElement(element_to_click[0])

                if clicked:
                    self.previouslyClickedElements[self.urlDomain].append(element_to_click)
                    logger.info("Modal window was closed by pressing %s."%element_to_click[1])
                    return True

            buttonElements = await self.find_elements_by_xpath(page, '//button')
            logger.info("Found %d button Elements"%len(buttonElements))
            anchorElements = await self.find_elements_by_xpath(page, '//a')
            logger.info("Found %d anchor Elements"%len(anchorElements))
            inputElements = await self.find_elements_by_xpath(page, '//input')
            logger.info("Found %d input Elements"%len(inputElements))

            clickElements = buttonElements + anchorElements

            def checkIfTextIn(text):
                """ Function to check if close text is in given text. """
                for name in self.closeTextsToExclude:
                    if name in text:
                        # logger.info("%s not in %s"%(name, text))
                        return False, -1

                for idx, name in enumerate(self.closeTexts):
                    regex = re.compile(r"(\s+%s\s+|\s+%s(.|,|!)*$|^%s\s+)"%(name, name, name), re.I)
                    if regex.search(text.strip()) is not None:
                        # logger.info("%s in %s"%(name, text))
                        return True, idx

                return False, -1

            filtered_elements = []
            filtered_elements_texts = []
            filtered_elements_order_in_closeTexts = []
            for element in clickElements:

                if not await self.isDisplayed(element):
                    continue

                innerHTML = await self.extractInnerHTMLFromElement(page, element)
                isMatchingElement, matchingTextIndex = checkIfTextIn(innerHTML.lower())
                
                if not isMatchingElement:
                    continue

                logger.info("%s matched with %s."%(innerHTML, self.closeTexts[matchingTextIndex]))

                filtered_elements.append(element)
                filtered_elements_texts.append(innerHTML)
                filtered_elements_order_in_closeTexts.append(matchingTextIndex)

            for element in inputElements:

                if not await self.isDisplayed(element):
                    continue
                
                elementType = await self.evaluateQuery(page, "(element) => element.getAttribute('type')", element)
                if elementType is None or elementType.lower() != 'submit':
                    continue
                elementValue = await self.evaluateQuery(page, "(element) => element.getAttribute('value')", element)
                isMatchingElement, matchingTextIndex = checkIfTextIn(elementValue.lower())

                if not isMatchingElement:
                    continue

                logger.info("%s matched with %s."%(innerHTML, self.closeTexts[matchingTextIndex]))

                filtered_elements.append(element)
                filtered_elements_texts.append(elementValue)
                filtered_elements_order_in_closeTexts.append(matchingTextIndex)

            if not filtered_elements:
                return False
            
            minOrder = 9999
            for elem, text, order in zip(filtered_elements, filtered_elements_texts, filtered_elements_order_in_closeTexts):
                if order < minOrder:
                    minOrder = order

                    element_to_click = [elem, text, order]

            logger.info("Clicking %s..."%element_to_click[1])
            
            clicked = await self.clickElement(element_to_click[0])

            if clicked:
                self.previouslyClickedElements[self.urlDomain].append(element_to_click)
                logger.info("Modal window was closed by pressing %s."%element_to_click[1])
                return True

        except Exception as e:
            logger.error("Exception inside closeModalWindow ==> %s"%e.__str__())
            return False
        
    async def execute_script_until_loaded(self, page, script, *arg):
        try:
            await self.evaluateQuery(page, script, *arg)
            await self.wait_until_loaded(page)

        except Exception as e:
            logger.error(f"Exception in execute_script_until_loaded: {traceback.format_exc()}")

    async def scroll_down_smoothly(self, page, func=None):
        logger.info("INSIDE scroll_down_smoothly &&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        # was_on_top = self.if_central_element_on_top() # TODO
        old_height = 0
        previous_scroll_num = 0

        while True:
            height = await self.evaluateQuery(page, "document.body.scrollHeight")

            if height is not None:
                logger.info("INSIDE while True loop of scroll_down_smoothly")
                logger.info("Old Height: {}, New Height: {}".format(old_height, height))

                if old_height > height:
                    diff = height
                else:
                    diff = height - old_height
                if diff == 0:
                    logger.info("DIFF is 0 .... BREAKING")
                    #self.execute_script_until_loaded("window.scrollBy(0,%d)" % self.scroll_down)
                    break

                logger.info("Pending height to scroll: {}".format(diff))
                scroll_num = math.ceil(diff / self.scroll_down)

                logger.info("Previous Scrol Num: " + str(previous_scroll_num))
                previous_scroll_num = scroll_num
                logger.info("*************** New scroll_num value is =====> "+str(scroll_num))

                for scroll_ind in range(scroll_num):
                    logger.info("INSIDE FOR LOOP OF WHILE LOOP....")
                    logger.info("Iteration number : "+str(scroll_ind))
                    await self.execute_script_until_loaded(page, "window.scrollBy(0,%d)" % self.scroll_down)
                    # time.sleep(self.scroll_sleep)

                    # TODO
                    # if not was_on_top:
                    #     removed = self.wait_central_element_to_disappear()
                    #     if not removed:
                    #         was_on_top = True

                new_height = await self.evaluateQuery(page, "document.body.scrollHeight")
                try:
                    if new_height is not None: 
                        if new_height > height: #page height has changed....extracting the PDPS
                            logger.info("Page height has changed..got the value from JS..extracting the PDPs")
                            if func:
                                ret = func()
                                if ret == 0:
                                    logger.info("PDP count has not increased...BREAK")
                                    break

                        elif height == new_height:
                            logger.info("Page height does not seem to change.....end of scroll")
                            if func:
                                func()
                            break

                    else:
                        logger.info("New height is null. Re-trying scrolling.")
                        # break

                except Exception as e:
                    logger.error(f"Exception while scrolling down: {traceback.format_exc()}")
                    break

            else:
                logger.info("New height is null. Re-trying scrolling.")
                # break

            #fun() #2019-11-13 #boohoo
            # Get the scrolled Height.
            old_height = await self.evaluateQuery(page, "window.scrollY")
            time.sleep(2)


if __name__ == "__main__":

    obj = playwrightModule(browser='chrome', headless=False)
    # obj.launchBrowser()
    # page = obj.openNewPage()
    # _ = obj.gotoURL(page, "https://www.myntra.com/clothing-set/ariel/ariel-infants-cotton-fleece-t-shirt-with-pyjamas/21676664/buy")
    # obj.screenshot(page, "/home/pranam/Desktop/playwright_screenshot.png")
    # obj.closeBrowser()
    url = PDP_URL('https://www.lifestylestores.com/in/en/SHOP-Global-Desi-Yellow-GLOBAL-DESI-Women-Embroidered-Tie-Up-Neck-Top/p/1000012411917-Yellow-Mustard', timeout=30)

    _, message = obj.getPageContent(url, keepAlive=True)
    logger.info(message)

    # url = PDP_URL('https://www.myntra.com/clothing-set/ariel/ariel-infants-cotton-fleece-t-shirt-with-pyjamas/21676664/buy', timeout=30)
    _, message = obj.getPageContent(url, keepAlive=True)
    logger.info(message)

    # logger.info(out)
    # with sync_playwright() as playwright:

    # playwright = sync_playwright().start()
    # chrome = playwright.chromium.launch(
    #     headless=False,
    #     channel='chrome',
    #     # ignore_default_args=True,
    #     args=[
    #         "--no-sandbox",
    #         "--disable-setuid-sandbox",
    #         "--window-size=1400,900",
    #         # "--user-agent=%s"%self.userAgent,
    #         "--disable-features=IsolateOrigins,site-per-process",
    #         '--disable-gpu',
    #         '--blink-settings=imagesEnabled=true',
    #         '--enable-javascript',
    #         '--incognito',
    #         '--aggressive-cache-discard',
    #         '--disable-cache',
    #         '--disable-application-cache',
    #         '--disable-offline-load-stale-cache',
    #         '--disable-gpu-shader-disk-cache',
    #         '--media-cache-size=0',
    #         '--disk-cache-size=0',
    #         '--mute-audio',
    #         '--disable-default-apps',
    #         '--no-default-browser-check',
    #         '--disable-background-timer-throttling',
    #         '--block-new-web-contents',
    #         '--disable-dev-shm-usage'
    #     ],
    #     executable_path=configuration.CHROME,
    #     slow_mo=0,
    #     handle_sigint=False,
    #     handle_sigterm=False,
    #     handle_sighup=False
    # )
    # page = chrome.new_page()
    # page.goto("https://google.com")
    # chrome.close()
