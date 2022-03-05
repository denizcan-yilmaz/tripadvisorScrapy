import scrapy
from scrapy.http import Request

class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com.tr']
    start_urls = ['https://www.tripadvisor.com.tr/Hotels-g298656-Ankara-Hotels.html']

    def parse(self, response):
        hotels = response.xpath('//*[@class="listing_title"]')

        for hotel in hotels:

            hotelURL = hotel.xpath('.//a/@href').extract()[0]
            hotelURL = response.urljoin(hotelURL)
            yield Request(hotelURL, callback=self.parse_hotels)
   
        url = response.xpath('//a[@class="nav next ui_button primary"]/@onclick').extract()[0]  
        nextPage = url.split(",")[-1][2:-3] 
        nextPage = response.urljoin(nextPage)
        if nextPage:
            yield Request(nextPage, callback = self.parse)

    def parse_hotels(self, response):
        hotelName = response.xpath('//*[@id="HEADING"]/text()').extract()[0]

        hotelAddress = response.xpath('//*[@class = "ceIOZ yYjkv"]/text()').extract()[0]        

        comments = response.xpath('//*[@data-test-target = "reviews-tab"]//*[@class = "cWwQK MC R2 Gi z Z BB dXjiy"]')

        for comment in comments:
            date = comment.xpath('.//*[@class="euPKI _R Me S4 H3"]/text()').extract()[0]

            stars = comment.xpath('.//span[contains(@class,"ui_bubble_rating")]/@class').extract_first()[-2]   

            revTitle = comment.xpath('.//*[@class="fCitC"]/span/span/text()').extract()[0]    

            rev = comment.xpath('.//*[@class="XllAv H4 _a"]/span/text()').extract()  


            yield {
                    'hotelName': hotelName,
                    'hotelAddress': hotelAddress,
                    'date': date,
                    'stars': stars,
                    'revTitle': revTitle,
                    'rev': rev 
                }

            nextPageURL = response.xpath('//*[@class="ui_button nav next primary "]/@href').extract()[0] 
            nextPageURL = response.urljoin(nextPageURL)
            if nextPageURL:
                yield Request(nextPageURL, callback=self.parse_hotels)