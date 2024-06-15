class FailedOpenNewPage(Exception):
    """ Exception denoting that the page was not loaded. """

    def __init__(self, message: str) -> None:
        super().__init__("Could open a new Page. Reason: {}".format(message))


class FailedOpenNewBrowser(Exception):
    """ Exception denoting that the browser was not opened. """  

    def __init__(self, message: str) -> None:
        super().__init__("Could open a new Browser. Reason: {}".format(message))


class PageIsClosed(Exception):
    """ Exception denoting that the page is closed. """
    def __init__(self, message: str) -> None:
        super().__init__("Page is closed! Please Re-open. Reason: {}".format(message))

class RetryGotoURL(Exception):
    """ Exception requesting retry again opening the url. """
    def __init__(self, message: str) -> None:
        super().__init__("Reload the page and reopen the url!. Message: {}".format(message))

class RetryGetPageContent(Exception):
    """ Exception requesting to retry the get page content function. """
    def __init__(self, message: str) -> None:
        super().__init__("Reload the page and reopen the url!. Message: {}".format(message))
