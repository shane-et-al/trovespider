import scrapy
from bs4 import BeautifulSoup

class TroveSpider(scrapy.Spider):
    name = "trove"

    def start_requests(self):
        urls = [
            'https://thetrove.net/Books/index.html',
            'https://thetrove.net/Magazines/index.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        path = BeautifulSoup(response.css(
            '.breadcrumbs_main').get()).get_text().strip().split(" / ")
        for file in response.css('.file a'):
            if file.attrib['href'] is not None:
                yield {"path": path, "title": file.css("::text").get(),
                       "url": response.urljoin(file.attrib['href'])}
        for dir in response.css('.dir a'):
            if dir.attrib['href'] is not None:
                if dir.attrib['href'].startswith("../"):
                    continue
                yield scrapy.Request(response.urljoin(dir.attrib['href']), callback=self.parse)
