import os
import asyncio
from Controllers.CrawlController import CrawlController
from Utils.Logger import Logger

class CrawlManager:
    def __init__(self, config):
        """
        Initializes the CrawlManager with the provided configuration.

        :param config: Configuration object containing crawl settings.
        """
        self.config = config
        self.logger = Logger(os.path.splitext(os.path.basename(__file__))[0])
        self.controllers = []

    def create_controllers(self, rows):
        """
        Create a CrawlController for each row and store it in the controllers list.

        :param rows: List of dictionaries representing rows (e.g., from a CSV file).
        """
        for row in rows:
            url = row.get("url")
            if not url:
                self.logger.warning("Row is missing 'url'. Skipping...")
                continue

            # Initialize a CrawlController for the URL
            controller = CrawlController(url, depth=0, config=self.config)
            self.controllers.append(controller)
            self.logger.info(f"Created CrawlController for URL: {url}")

    async def start_crawling(self, rows):
        """
        Initiates the crawling process for the imported rows.

        :param rows: List of dictionaries representing rows (e.g., from a CSV file).
        """
        self.logger.info("Starting crawl process.")
        self.create_controllers(rows)

        # Run all crawlers asynchronously
        await asyncio.gather(*(controller.crawl(self) for controller in self.controllers))

        self.logger.info("Crawling process completed.")
