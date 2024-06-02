from django.http import JsonResponse
from django.views.generic import View
from scrapy.crawler import CrawlerProcess
from scrapers.spiders.desktopbg_spider import ComputerSpider
import sqlite3

class ComputerListView(View):
    def get(self, request):
        processor = request.GET.get('processor', '')
        gpu = request.GET.get('gpu', '')
        motherboard = request.GET.get('motherboard', '')
        ram = request.GET.get('ram', '')

        conn = sqlite3.connect('desktop_data.db')
        c = conn.cursor()

        query = "SELECT * FROM products WHERE 1=1"
        if processor:
            query += f" AND processor LIKE '%{processor}%'"
        if gpu:
            query += f" AND gpu LIKE '%{gpu}%'"
        if motherboard:
            query += f" AND motherboard LIKE '%{motherboard}%'"
        if ram:
            query += f" AND ram LIKE '%{ram}%'"

        c.execute(query)
        results = c.fetchall()
        conn.close()

        data = []
        for row in results:
            data.append({
                'url': row[0],
                'processor': row[1],
                'gpu': row[2],
                'motherboard': row[3],
                'ram': row[4],
            })

        return JsonResponse(data, safe=False)

def scrape_desktop_bg(request):
    process = CrawlerProcess(settings={
        "FEEDS": {
            "items.json": {"format": "json"},
        },
    })
    process.crawl(ComputerSpider)
    process.start()
    with open("items.json", "r") as f:
        data = f.read() 
    return JsonResponse(data, safe=False)
