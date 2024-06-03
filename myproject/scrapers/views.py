from django.http import JsonResponse
from django.views.generic import View
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy import signals
from scrapers.spiders.desktopbg_spider import ComputerSpider
from scrapy.signalmanager import dispatcher
import sqlite3


class ComputerList(View):
    def get(self, request):
        processor = request.GET.get('processor', '')
        gpu = request.GET.get('gpu', '')
        motherboard = request.GET.get('motherboard', '')
        ram = request.GET.get('ram', '')

        conn = sqlite3.connect('desktop_data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM products WHERE 1=1"
        if processor:
            query += f" AND processor LIKE '%{processor}%'"
        if gpu:
            query += f" AND gpu LIKE '%{gpu}%'"
        if motherboard:
            query += f" AND motherboard LIKE '%{motherboard}%'"
        if ram:
            query += f" AND ram LIKE '%{ram}%'"

        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        data = []
        for row in results:
            data.append({
                'processor': row[1],
                'gpu': row[2],
                'motherboard': row[3],
                'ram': row[4],
            })

        return JsonResponse(data, safe=False)


class ScrapingView(View):
    def get(self, request):
        data = []
        success = {'status': None}

        def item_scraped(item, response, spider):
            data.append(dict(item))

        def spider_closed(spider, reason):
            if reason == 'finished':
                success['status'] = 'success'
            else:
                success['status'] = 'failed'

        dispatcher.connect(item_scraped, signal=signals.item_scraped)
        dispatcher.connect(spider_closed, signal=signals.spider_closed)

        settings = get_project_settings()

        configure_logging(settings)

        process = CrawlerProcess(settings)

        process.crawl(ComputerSpider)
        process.start()

        if success['status'] == 'success':
            return JsonResponse({'message': 'Scraping completed successfully!'}, safe=False)
        else:
            return JsonResponse({'message': 'Scraping failed!'}, safe=False)
