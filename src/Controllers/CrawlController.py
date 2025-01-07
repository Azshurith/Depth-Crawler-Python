# import requests
# from bs4 import BeautifulSoup
# from Utils.Logger import Logger


# class CrawlController:
#     def __init__(self, url, depth, config, logger=None):
#         self.url = url
#         self.depth = depth
#         self.config = config
#         self.logger = logger or Logger("CrawlController")

#     def crawl(self, manager):
#         """
#         Perform crawling for the current URL and queue discovered links.
#         """
#         try:
#             self.logger.info(f"Starting crawl for {self.url} at depth {self.depth}")
#             response = requests.get(self.url, timeout=self.config["timeout"])
#             response.raise_for_status()

#             # Process the page content
#             soup = BeautifulSoup(response.content, "html.parser")
#             self.logger.info(f"Successfully fetched {self.url}")

#             # Extract content or perform any data capture here
#             self.extract_content(soup)

#             # Queue links for further crawling if depth limit isn't reached
#             if self.depth < self.config["max_depth"]:
#                 links = self.extract_links(soup)
#                 for link in links:
#                     manager.add_to_queue(link, self.depth + 1)

#         except requests.RequestException as e:
#             self.logger.error(f"Error crawling {self.url}: {e}")

#     def extract_content(self, soup):
#         """
#         Extract and process content from the page.
#         """
#         self.logger.info(f"Extracting content from {self.url}")
#         # Example: Extract all paragraph text
#         paragraphs = soup.find_all("p")
#         for p in paragraphs:
#             text = p.get_text(strip=True)
#             self.logger.info(f"Extracted: {text}")

#     def extract_links(self, soup):
#         """
#         Extract all valid links from the page.
#         """
#         self.logger.info(f"Extracting links from {self.url}")
#         links = set()
#         for a_tag in soup.find_all("a", href=True):
#             href = a_tag["href"]
#             if self.is_valid_url(href):
#                 links.add(href)
#         self.logger.info(f"Found {len(links)} links on {self.url}")
#         return links

#     def is_valid_url(self, url):
#         """
#         Validate the URL format and whether it's allowed for crawling.
#         """
#         # Example: Validate against a whitelist or blacklist
#         return url.startswith("http")
