import os
import requests
from pyppeteer import launch
from Utils.Logger import Logger

class CrawlController:
    def __init__(self, url, depth, config):
        """
        Initializes the CrawlController with the necessary configurations.

        :param url: The URL to crawl.
        :param depth: The depth at which the URL is being crawled.
        :param config: Configuration object for the crawl (e.g., max_depth, timeout).
        :param logger: Logger instance for logging messages.
        """
        self.url = url
        self.depth = depth
        self.config = config
        self.logger = Logger(os.path.splitext(os.path.basename(__file__))[0])

    async def crawl(self, manager):
        """
        Perform crawling for the given URL using puppeteer.

        :param manager: The CrawlManager instance managing this controller.
        """
        self.logger.info(f"Starting crawl for URL: {self.url} at depth {self.depth}")

        try:
            # Launch the browser
            browser = await launch(headless=True, args=["--no-sandbox"])
            page = await browser.newPage()

            # Set the timeout for page loading
            await page.setDefaultNavigationTimeout(self.config.get("timeout", 30) * 1000)

            # Navigate to the URL
            await page.goto(self.url)
            self.logger.info(f"Successfully navigated to {self.url}")

            # Extract content or links
            content = await self.extract_content(page)
            self.logger.info(f"Extracted content from {self.url}")

            # Optionally, add links to the manager's queue for further crawling
            if self.depth < self.config.get("max_depth", 3):
                links = await self.extract_links(page)
                for link in links:
                    manager.add_to_queue(link, self.depth + 1)

            # Close the page and browser
            await page.close()
            await browser.close()

        except Exception as e:
            self.logger.error(f"Error while crawling {self.url}: {e}")

    async def extract_content(self, page):
        """
        Extracts content from the page. Modify this logic to suit your use case.

        :param page: The pyppeteer Page instance to extract content from.
        :return: The extracted content (e.g., text, tags).
        """
        return await page.evaluate("""
            () => {
                const results = [];
                const elements = document.querySelectorAll('*');
                elements.forEach(element => {
                    const text = element.textContent.trim();
                    if (text) {
                        results.push({ tag: element.tagName.toLowerCase(), text });
                    }
                });
                return results;
            }
        """)

    async def extract_links(self, page):
        """
        Extracts links from the page. Modify this logic to suit your use case.

        :param page: The pyppeteer Page instance to extract links from.
        :return: A list of extracted links.
        """
        return await page.evaluate("""
            () => Array.from(document.querySelectorAll('a[href]'))
                .map(a => a.href)
                .filter(href => href.startsWith('http'))
        """)
