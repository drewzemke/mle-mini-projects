import scrapy


class AuthorsSpider(scrapy.Spider):
    name = 'authors'

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        author_page_links = response.css('.author + a')
        yield from response.follow_all(author_page_links, self.parse_author)

        next_page_links = response.css('li.next a')
        yield from response.follow_all(next_page_links, self.parse)

    def parse_author(self, response):
        yield {
            'name': response.css('h3.author-title::text').get(default='').strip(),
            'birthdate': response.css('.author-born-date::text').get(default='').strip(),
            'bio': response.css('.author-description::text').get(default='').strip(),
        }
