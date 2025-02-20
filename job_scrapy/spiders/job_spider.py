import scrapy
from scrapy_selenium import SeleniumRequest
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.selector import close_cookie_banner
from job_scrapy.items import JobScrapyItem

COOKIE_BANNER_SELECTOR = 'bahf-cookie-disclaimer-dpl3'
EXPAND_BUTTON_SELECTOR = 'ergebnisliste-ladeweitere-button'
MODE_SWITCH_SELECTOR = 'ansicht-auswahl-tabbar-item-1'
RESULT_LIST_SELECTOR = 'ergebnisliste-liste'

class JobSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["arbeitsagentur.de"]

    def __init__(self, query=None, location=None, diameter=200, *args, **kwargs):
        super(JobSpider, self).__init__(*args, **kwargs)
        assert query is not None, 'query parameter is required'
        assert location is not None, 'location parameter is required'
        assert diameter is not None, 'diameter parameter is required'
        assert diameter in [0, 10, 15, 25, 50, 100, 200], 'diameter must be one of 0, 10, 15, 25, 50, 100, 200'
        self.diameter = diameter
        self.query = urllib.parse.quote_plus(query)
        self.location = urllib.parse.quote_plus(location)

    def start_requests(self):
        urls = [f'https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=1&was={self.query}&wo={self.location}&umkreis={self.diameter}']
        for url in urls:
            yield SeleniumRequest(
                url=url, 
                callback=self.parse,
                wait_time=5,
                wait_until=EC.presence_of_element_located((By.ID, f'{RESULT_LIST_SELECTOR}-1')),
                screenshot=True,
                errback=self.log_error
            )

    def parse(self, response: scrapy.http.Response):
        driver = response.meta['driver']
        wait = WebDriverWait(driver, 6)

        # Save a screenshot of the page
        screenshot = response.meta['screenshot']
        with open(f'data/screenshot-{self.name}.png', 'wb') as f:
            f.write(screenshot)

        # close the cookie banner (in shadow dom)
        close_cookie_banner(driver, wait, COOKIE_BANNER_SELECTOR)

        # Switch to the detailed view
        wait.until(EC.visibility_of_element_located((By.ID, MODE_SWITCH_SELECTOR)))
        switch_mode_button = driver.find_element(By.ID, MODE_SWITCH_SELECTOR)
        if switch_mode_button:
            switch_mode_button.click()
        else:
            print('>>> Switch mode button not found')

        # TODO: Fix the loop to get all job results.
        limit = 1
        index = 1
        while index <= limit:
            # except for the first page, click the expand button to load more results if the button is present.
            if (index != 1):
                expand_button = driver.find_element(By.ID, EXPAND_BUTTON_SELECTOR)
                # if there is an expand button, click it and wait for the current page to be present.
                if expand_button:
                    # Scroll the expand button into view
                    driver.execute_script("arguments[0].scrollIntoView();", expand_button)
                    wait.until(EC.visibility_of_element_located((By.ID, EXPAND_BUTTON_SELECTOR)))
                    expand_button.click()
                    wait.until(EC.visibility_of_element_located((By.ID, f'{RESULT_LIST_SELECTOR}-{index}')))

            # get results container for current page. If no results container is found, break the loop.
            results_container = response.css(f'#{RESULT_LIST_SELECTOR}-{index}')
            if not results_container:
                index = limit + 1
                break
            else:
                index += 1

            # get all jobs and create a JobScrapyItem for each job
            job_containers = results_container.css('li')
            for job_container in job_containers:
                job_item = JobScrapyItem()
                job_item['url'] = job_container.css('a').attrib['href'].strip()
                job_item['title'] = job_container.css('.mitte-links .mitte-links-titel::text').get(default='').strip()
                job_item['employer'] = job_container.css('.mitte-links .mitte-links-arbeitgeber::text').get(default='').strip()
                job_item['location'] = job_container.css('.mitte-links .mitte-links-ort::text').get(default='').strip()
                job_item['search_params'] = {
                    'query': self.query,
                    'location': self.location,
                    'diameter': self.diameter
                }
                yield job_item

    def log_error(self, failure):
        self.logger.error(repr(failure))
