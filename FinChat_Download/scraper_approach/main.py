from loggers import Logger
logger = Logger().get_logger('main')

from lxml import etree, html as lxml_html
import csv, json
from pathlib import Path

from async_playwrightModule import playwrightModule
from seleniumModule import seleniumModule
from utils import PDP_URL
import configuration

playwright_obj = playwrightModule(headless=False)
selenium_obj = seleniumModule(headless=False)

Path(configuration.OUTPUT_FOLDER).mkdir(exist_ok=True, parents=True)

def read_csv_from_html(html: str, company_name: str, file_name: str)-> None:
    DOM = etree.HTML(html)

    table_root = DOM.xpath("//table[contains(@class, 'mantine-Table-root')]")

    if not table_root:
        return
    
    table_root = table_root[0]
    csv_rows = []

    table_columns = table_root.xpath(".//thead//th//div[contains(@class, 'mantine-TableHeadCell-Content-Wrapper')]/@title")
    logger.info(f"Found table columns: {table_columns}")
    csv_rows.append(table_columns)

    table_rows = table_root.xpath(".//tbody//tr")
    logger.info(f"Found {len(table_rows)} table rows.")
    for row in table_rows:

        row_column_values = row.xpath(".//td//*[self::p or self::span]/text() | .//td//a/@target")
        logger.info(row_column_values)
        csv_rows.append(row_column_values)

    output_filepath = f"{configuration.OUTPUT_FOLDER}/{company_name}"
    Path(output_filepath).mkdir(exist_ok=True, parents=True)

    with open(f"{output_filepath}/{file_name}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(csv_rows)

if __name__ == "__main__":

    # URL = PDP_URL("https://finchat.io/company/NSEI-RELIANCE/?statement=balance-sheet", timeout=120, page_load_event_playwright='networkidle')

    # html, message = selenium_obj.getPageContent(URL, keepAlive=False)

    # if html:
    #     read_csv_from_html(html)

    # else:
    #     logger.info(f"Couldn't fetch the page content. Message from FPM: {message}")
    selenium_obj.parse_and_scrape_finchat('NSEI-RELIANCE', read_csv_from_html)
