# import scrapy

# class HackerNewsSpider(scrapy.Spider):
#     name = "hacker_news"
#     start_urls = [
#         "https://news.ycombinator.com/"
#     ]
#     def parse(self, response):
#         for article in response.css("tr.athing"):
#             yield {
#                 "title": article.css("a.storylink::text").get(),
#                 "url": article.css("a.storylink::attr(href)").get(),
#                 "votes": int(article.css("span.score::text").re_first(r"\d+"))
#             }
#         next_page = response.css("a.morelink::attr(href)").get()
#         if next_page is not None:
#             yield response.follow(next_page, self.parse)

import scrapy
import sqlite3
import logging

class ComputerSpider(scrapy.Spider):
    name = "desktop"
    allowed_domains = ["desktop.bg"]
    start_urls = ["https://desktop.bg/"]

    def __init__(self):
        self.conn = sqlite3.connect('desktop_data.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS products
                         (url TEXT PRIMARY KEY, processor TEXT, gpu TEXT, motherboard TEXT, ram TEXT)''')
        self.conn.commit()

    def closed(self, reason):
        self.conn.close()

    def parse(self, response):
        computers_all = response.css('div[data-menu="menu-Computer"] ul.brands li:nth-child(1) a::attr(href)').get()
        computers_all_whole_link = 'https://desktop.bg' + computers_all
        yield response.follow(computers_all_whole_link, callback=self.parse_computers_page)

    def parse_computers_page(self, response):
        product_titles = response.css('h2[itemprop="name"]::text').getall()
        product_prices = response.css('span.price span[itemprop="price"]::text').getall()
        product_urls = response.css('article[itemtype="http://schema.org/product"] > a::attr(href)').getall()
        for title, price, url in zip(product_titles, product_prices, product_urls):
            yield response.follow(url, callback=self.parse_product_page)

    def parse_product_page(self, response):
        url = response.url
        processor = response.xpath('//th[contains(text(), "Процесор")]/following-sibling::td//text()').get()
        gpu = response.xpath('//th[contains(text(), "Видеокарта")]/following-sibling::td//text()').get()
        motherboard = response.xpath('//th[contains(text(), "Дънна платка")]/following-sibling::td//text()').get()
        ram_option = response.xpath('//tr[@id="DesktopRam"]/td//div[@class="default-option options"]/label/span/text()').getall()
        ram = ''.join(ram_option).strip() if ram_option else None

        # Check if the product already exists in the database
        self.c.execute("SELECT * FROM products WHERE url=?", (url,))
        existing_product = self.c.fetchone()

        if not existing_product:
            try:
                self.c.execute("INSERT INTO products (url, processor, gpu, motherboard, ram) VALUES (?, ?, ?, ?, ?)",
                               (url,
                                processor.strip() if processor else None,
                                gpu.strip() if gpu else None,
                                motherboard.strip() if motherboard else None,
                                ram if ram_option else None))
                self.conn.commit()
                logging.info("Data inserted into SQLite successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error inserting data into SQLite: {str(e)}")

        yield {
            'url': url,
            'processor': processor.strip() if processor else None,
            'gpu': gpu.strip() if gpu else None,
            'motherboard': motherboard.strip() if motherboard else None,
            'ram': ram if ram_option else None,
        }
