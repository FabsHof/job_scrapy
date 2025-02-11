import scrapy
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

RESULTS_SELECTOR = 'ul#ergebnisliste-liste-1 li'
EXPAND_BUTTON_SELECTOR = 'button#ergebnisliste-ladeweitere-button'

class JobSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["arbeitsagentur.de"]

    def start_requests(self):
        urls = ["https://www.arbeitsagentur.de/jobsuche/suche?angebotsart=1&was=Data%20Engineer%2Fin&wo=ulm&umkreis=100"]
        for url in urls:
            yield SeleniumRequest(
                url=url, 
                callback=self.parse,
                wait_time=10,
                wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, RESULTS_SELECTOR)),
            )

    def parse(self, response):
        # TODO: As long as the "Lade weitere" button is present, click it
        # and wait for the results to load. Then, extract the job data.
        # driver = response.meta['driver']
        # while driver.find_elements(By.CSS_SELECTOR, EXPAND_BUTTON_SELECTOR):
        #     driver.find_element(By.CSS_SELECTOR, EXPAND_BUTTON_SELECTOR).click()
        #     WebDriverWait(driver, 10).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, RESULTS_SELECTOR))
        #     )


        jobs = response.css(RESULTS_SELECTOR)

        for job in jobs:
            title = job.css('span.mitte-links-titel::text').get(default='').strip()
            url = job.css('a::attr(href)').get()
            employer = job.css('div.mitte-links-arbeitgeber::text').get(default='').strip()
            location = job.css('span.mitte-links-ort::text').get(default='').strip()
            published_at = job.css('span.unten-datum::text').get(default='').strip()
            yield {
                'name': title,
                'url': url,
                'employer': employer,
                'location': location,
                'published_at': published_at,
            }