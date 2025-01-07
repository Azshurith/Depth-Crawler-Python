import os
import queue
# from Controllers.CrawlController import CrawlController
from Utils.Logger import Logger

class CrawlManager:
    def __init__(self, config):
        self.config = config  # Configuration object for crawling
        self.logger = Logger(os.path.splitext(os.path.basename(__file__))[0])
        self.visited_urls = set()  # Tracks visited URLs globally
        self.url_queue = queue.Queue()  # Queue to manage URLs and their depths
        self.controllers = []  # List of active CrawlController instances

    def add_to_queue(self, url, depth):
        """
        Add a URL and its depth to the queue if it hasn't been visited yet.
        """
        if url not in self.visited_urls and depth <= self.config["max_depth"]:
            self.visited_urls.add(url)
            self.url_queue.put((url, depth))
            self.logger.info(f"Queued URL: {url} at depth {depth}")

    def start_crawling(self, start_url):
        """
        Initiates the crawling process with a given start URL.
        """
        self.add_to_queue(start_url, 0)  # Start from depth 0
        self.logger.info(f"Starting crawl from: {start_url}")

        while not self.url_queue.empty():
            url, depth = self.url_queue.get()
            self.logger.info(f"Processing URL: {url} at depth {depth}")
            # controller = CrawlController(url, depth, self.config, self.logger)
            # self.controllers.append(controller)
            # controller.crawl(self)

        self.logger.info("Crawling process completed.")
