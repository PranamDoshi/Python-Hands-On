import math
import time
import sys
import os

import configuration
from loggers import Logger
logger = Logger().get_logger('seleniu-driverGeneral')


class DriverGeneral:

    def __init__(self):
        # used while loading the page
        self.sleep_time = 2
        self.sleep_max = 5

        self.get_sleep = 5  # sleep after get

        self.on_top_z_index = 10  # element on top considered to be popup while scrolling down
        self.on_top_sleep = 3  # waiting until central element on top will dissapear
        self.on_top_sleep_max = 1  # number of waits

        self.if_scroll = False  # scroll down smoothly after each request
        self.scroll_down = 1000  # scroll down smoothly
        self.scroll_up = 100  # scrolling up after fully scrolling down
        self.scroll_sleep = 2  # sleep after each scroll
        self.scroll_max = 40  # maximal amount of scroll downs
        self.old_height = 0 #XXX: 2019-10-30

        self.click_max = 10  # maximal number of clicking some button
        self.click_max_reached = False  # maximal number of clicking some button

        # closing modal window
        # remove cookies ?
        self.close_buttons = ['continue', 'no', 'start shopping', 'shop now', 'no thanks', 'not right now', 'decline offer', 'only required', 'stay on', 'reject', 'accept', 'allow', 'cookies']
        self.close_exclude_buttons = ['policy', 'use of cookies', 'set cookies']
        self.close_z_index = 100

        #self.info_scroll_num = 0  # how many times current page was scrolled
        #self.info_close_button = None  # button presses to close modal window

    def get_complete(self, url, fun=None):
        self.get(url)
        time.sleep(self.get_sleep)
        self.close_modal_window()
        if self.if_scroll:
            self.scroll_down_smoothly(fun)

    def wait_until_loaded(self):
        logger.info("Inside wait_until_loaded method.......")
        old_height = self.execute_script("return window.newH")

        while True:
            try:
                new_height = self.execute_script("return window.newH")
                if old_height != new_height:
                    logger.info("height has changed...")
                    return True

                else:
                    time.sleep(self.sleep_time)
                    return

            except Exception as e:
                logger.error("Exception in wait_until_loaded method ==> %s"%e.__str__())
                return

    def wait_until_loaded_old(self):
        logger.info("inside wait_until_loaded method ...............")
        old_html = self.getPageHTML()
        sleep_num = 0
        while True:
            sleep_num += 1
            if sleep_num > self.sleep_max:
                logger.info('Page is probably already loaded')
                return True
            time.sleep(self.sleep_time)
            try:
                new_html = self.getPageHTML()
            except:
                logger.info('Caught exception while loading page: %s' % (sys.exc_info()[0]))
                return
                # continue
            if new_html == old_html:
                if sleep_num>1:
                    logger.info('Page is loaded')
                return True
            else:
                logger.info('Page is not loaded yet...')
                old_html = new_html

    def execute_script_until_loaded(self, script, *arg):
        try:
            self.execute_script(script, *arg)
            self.wait_until_loaded()
        except Exception as e:
            #logger.error(e)
            logger.error("Exception in execute_script_until_loaded --> %s"%e.__str__())

    def get_element_xpath(self, element):
        script = '''
        function getPathTo(node) {
            var stack = [];
            while(node.parentNode !== null) {
                var i = 1;
                child = node;
                while( (child = child.previousSibling) != null ){
                    if(node.tagName == child.tagName){
                        i++;
                    }
                }
                str = node.tagName + '[' + i +']'
                stack.unshift(str);
                node = node.parentNode;
            }
            return stack.join('/');
        }
        return getPathTo(arguments[0]);
        '''
        xpath = self.execute_script(script, element)
        return xpath

    def click_element(self, element):
        try:
            self.execute_script("arguments[0].scrollIntoView(true);", element)
            # https://stackoverflow.com/questions/44912203/selenium-web-driver-java-element-is-not-clickable-at-point-36-72-other-el/44916498
            self.execute_script_until_loaded("arguments[0].click();", element)
            logger.info("Clicked on the button ==============> ")
            logger.info(element)

        except Exception as e:
            #logger.error(e)
            logger.error("Exception in click_element --> %s"%e.__str__())

    def click_by_coordinates(self, x, y):
        try:
            script = 'document.elementFromPoint(%d, %d).click();' % (x, y)
            self.execute_script(script)
        except Exception as e:
            # logger.error(e)
            logger.error("Exception in click_by_coordinates --> %s"%e.__str__())

    def remove_element(self, element):
        self.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", element)

    def get_central_element(self):
        width = self.execute_script("return window.innerWidth")
        height = self.execute_script("return window.innerHeight")
        try:
            element = self.execute_script("return document.elementFromPoint(%d, %d)" % (width/2, height/2))
        except Exception as e:
            # logger.error(e)
            logger.error("Exception in get_central_element --> %s"%e.__str__())
        return element

    def if_central_element_on_top(self):
        element = self.get_central_element()
        z_index = self.get_z_index(element)
        if z_index > self.on_top_z_index:
            logger.info('element on top, z-index: %d' % z_index)
        return z_index > self.on_top_z_index

    def wait_central_element_to_disappear(self):
        removed = False
        for _ in range(self.on_top_sleep_max):
            on_top = self.if_central_element_on_top()
            if on_top:
                logger.info('waiting top element to disappear')
                time.sleep(self.on_top_sleep)
            else:
                removed = True
                break
        if not removed:
            logger.info('top element was not removed')
        return removed

    def scroll_down(self):
        old_height = self.execute_script("return document.body.scrollHeight")
        scroll_num = 0
        while True:
            try:
                self.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                self.execute_script_until_loaded("window.scrollBy(0,%d)" % (-self.scroll_up))
                time.sleep(self.scroll_sleep)
                scroll_num += 1
                height = self.execute_script("return document.body.scrollHeight")
                logger.info('scrolled to the bottom %d times, document height %d' % (scroll_num, height))

                if old_height == height:
                    break
                if scroll_num >= self.scroll_max:
                    logger.info('maximum number %d of scrolls reached' % self.scroll_max)
                    break
                old_height = height
            
            except Exception as e:
                break

    def scroll_down_smoothly(self, fun=None):
        logger.info("INSIDE scroll_down_smoothly &&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
        # was_on_top = self.if_central_element_on_top()
        #old_height = 0
        old_height = self.old_height #XXX: 2019-10-30
        scroll_num_total = 0
        previous_pdp_count = 0
        current_pdp_count = 0
        ret_counter = 0
        previous_scroll_num = 0
        # errorsEncounterd = 0
        while True:
            rval = self.execute_script("return window.newH")
            logger.info(rval)
            if rval is not None:
                logger.info("INSIDE while True loop of scroll_down_smoothly")
                height = self.execute_script("return document.body.scrollHeight")
                if old_height > height: #XXX: 2019-10-30
                    diff = height
                else:
                    diff = height - old_height
                if diff == 0:
                    logger.info("DIFF is 0 .... BREAKING")
                    #self.execute_script_until_loaded("window.scrollBy(0,%d)" % self.scroll_down)
                    break
                scroll_num = math.ceil(diff / self.scroll_down)
                logger.info("Previous Scrol Num: " + str(previous_scroll_num))
                logger.info("Scrol Num: " + str(scroll_num))
                logger.info("##################################################################")            #scroll_num = 1
                logger.info("*************** scroll_num value is =====> "+str(scroll_num))
                for scroll_ind in range(scroll_num):
                    rval_old = self.execute_script("return window.newH")
                    logger.info("INSIDE FOR LOOP OF WHILE LOOP....")
                    logger.info("Iteration number : "+str(scroll_ind))
                    self.execute_script_until_loaded("window.scrollBy(0,%d)" % self.scroll_down)
                    # if not was_on_top:
                    #     removed = self.wait_central_element_to_disappear()
                    #     if not removed:
                    #         was_on_top = True
                    rval_new = self.execute_script("return window.newH")
                scroll_num_total += 1
                try:
                    if rval_new is not None: 
                        if rval_new > rval: #page height has changed....extracting the PDPS
                            logger.info("Page height has changed..got the value from JS..extracting the PDPs")
                            if fun:
                                ret = fun()
                                if ret == 0:
                                    logger.info("PDP count has not increased...BREAK")
                            break
                        elif rval == rval_new:
                            logger.info("Page height does not seem to change.....end of scroll")
                            if fun:
                                fun()
                            break

                    else:
                        break
                except Exception as e:
                    logger.error("Exception while scrolling down: %s."%e.__str__())
                    # errorsEncounterd += 1
                    # if errorsEncounterd > 2:
                    break
                    # self.restartDriver()
            else:
                break
            #fun() #2019-11-13 #boohoo
            old_height = height
            self.old_height = height #XXX: 2019-10-30
            logger.info(self.old_height)
            time.sleep(5)

    def keep_clicking(self, xpath, fun=None):
        logger.info("Inside keep_clicking method of scraper_pdp")
        old_height = self.execute_script("return document.body.scrollHeight")
        button_text = None
        click_num = 0
        # errorsEncounterd = 0
        while True:
            try:
                current_button_text = self.clickByXPATH(xpath)
                if current_button_text is None:
                    break

                button_text = current_button_text

                click_num += 1
                height = self.execute_script("return document.body.scrollHeight")
                logger.info('button %s clicked %d times, document height %d' % (button_text, click_num, height))

                logger.info ("Old height--------->"+str(old_height))
                logger.info ("height--------->"+str(height))
                logger.info(str(time.time()))
                if 'next' in xpath.lower() and fun is not None:
                    logger.info("Extracting PDPs from the page...........called from keep_clicking method")
                    ret = fun()
                else:
                    logger.info("This is load more case....not invoking pdp extraction now....")
                logger.info(str(time.time()))
                if click_num >= self.click_max:
                    logger.info('maximum number %d of clicks reached' % self.click_max)
                    self.click_max_reached = True
                    break
                old_height = height
            
            except Exception as e:
                # errorsEncounterd += 1
                logger.error("Exception inside keep_clicking: %s."%e.__str__())
                # if errorsEncounterd > 2:
                break
                # self.restartDriver()

        #self.updateInfo('button %s clicked %d times' % (button_text, click_num))
        if click_num > 0:
            logger.info('button %s clicked %d times' % (button_text, click_num))

    def click_to_remove_modal_window_by_coords(self, x, y):
        try:
            element = self.execute_script("return document.elementFromPoint(%d, %d)" % (x, y))
        except Exception as e:
            # logger.error(e)
            logger.error("Exception in click_to_remove_modal_window_by_coords --> %s"%e.__str__())
            element = None
        if element is not None:
            #self.hover(element)
            cursor = self.getValueOfCSSProperty(element, 'cursor')  # TODO: abstract from Selenium
            if cursor != 'pointer':
                self.click_by_coordinates(x, y)

    def click_to_remove_modal_window(self):
        self.click_to_remove_modal_window_by_coords(1, 1)
        height = self.execute_script("return window.innerHeight")
        self.click_to_remove_modal_window_by_coords(1, height - 1)
        self.wait_until_loaded()

    def close_modal_window(self):
        self.click_to_remove_modal_window()

        #self.remove_divs_by_z_index(1)
        clicked = self.click_modal_window(self.close_z_index, self.close_buttons, self.close_exclude_buttons)

        if clicked:
            self.click_to_remove_modal_window()
