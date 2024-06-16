import subprocess
from pathlib import Path
parent_path = Path(Path(__file__).parent).as_posix()

FPM_API = "https://usc-fpm.streamoid.com/v1/usc"
GET_PAGE_CONTENT_ENDPOINT = f"{FPM_API}/getPageContent"

LOGS_FOLDER = f"{parent_path}/logs"
DOMAIN_MODULE_PREFERENCE_FILE = f"{parent_path}/fpm_domain_configs.json"

ALLOW_SCREENSHOTS, ALLOW_ALERTS = 1, 1
DEFAULT_PAGE_LOAD_EVENT, DEFAULT_TIMEOUT, DEFAULT_REQUESTS_THRESHOLD, DEFAULT_RATE_LIMIT, DEFAULT_MAX_IMAGE_DOWNLOAD_RETRIES = 'load', 30, 250000, 1, 3

CHROME_VERSION = subprocess.getoutput('google-chrome --version')
CHROME_VERSION = CHROME_VERSION.strip().split(' ')[-1]

userAgents = {
    'chrome': [
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s  Safari/537.36" % CHROME_VERSION,
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/%s Safari/537.36" % CHROME_VERSION
    ]
}

DISPLAY_SIZE_STRING = '1400x900'
DISPLAY_SIZE_TUPLE = tuple(map(int, DISPLAY_SIZE_STRING.split('x')))
DISPLAY_VISIBLE = 0

CHROMEDRIVER = '/home/pranam/chromedriver'
CHROME = '/opt/google/chrome/chrome'

USC_ALERTS_WEBHOOK = 'https://streamoid1.webhook.office.com/webhookb2/26ce32b3-2a90-4375-af38-d885eaaec6fe@d916e493-4a5b-403f-9cf0-93dd590d9318/IncomingWebhook/03d5484f5d3e4855bb0122cf6684b278/a12d9294-541e-432d-86c1-62bf308fa1c3'
PEOPLE_TO_MENTION = [
    {
        "name": "Pranam Doshi",
        "email": "pranam@streamoid.com"
    }
]

OUTPUT_FOLDER = f"{parent_path}/StocksData"
