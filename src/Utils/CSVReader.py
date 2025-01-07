import os
import csv
from typing import List, Dict, Any
from Utils.Logger import Logger

class CSVReader:
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the CSVReader with a configuration object.

        :param config: Dictionary containing configuration options.
        """
        self.logger = Logger(os.path.splitext(os.path.basename(__file__))[0])
        self.config = config  # Store the configuration object

    def read(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Reads a CSV file and returns structured data as a list of dictionaries.

        :param file_path: Path to the CSV file.
        :return: List of structured data parsed from the CSV.
        """
        data = []

        try:
            with open(file_path, mode="r", encoding="utf-8-sig") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["URL # Number"].strip() and row["URL"].strip():
                        site = {
                            "id": row["URL # Number"],
                            "url": row["URL"],
                            "words_white_listed": [],
                            "tags_white_listed": [],
                            "tags_black_listed": [],
                            "urls_white_listed": [],
                            "urls_black_listed": [],
                            "urls_trim": [],
                            "proxies": [],
                            "depth_max": self.config.get("depth_max"), 
                            "load_timeout": self.config.get("load_timeout"),
                            "include_external_sites": self.config.get("include_external_sites"),
                            "enable_whitelist_url": self.config.get("enable_whitelist_url"),
                            "enable_trim_url": self.config.get("enable_trim_url"),
                            "enable_blacklist_url": self.config.get("enable_blacklist_url"),
                        }
                        data.append(site)

                # Reset file pointer to the start
                file.seek(0)
                
                # Additional processing for other fields
                for row in reader:
                    site_id = row["URL # Number 2"].strip()
                    for site in data:
                        if row["White Listed Words"].strip() and row["White Listed Words"] != "White Listed Words" and site["id"] == site_id:
                            site["words_white_listed"].append(row["White Listed Words"].strip())
                        if row["White Listed Tags"].strip() and row["White Listed Tags"] != "White Listed Tags":
                            site["tags_white_listed"].append(row["White Listed Tags"].strip())
                        if row["Black Listed Tags"].strip() and row["Black Listed Tags"] != "Black Listed Tags":
                            site["tags_black_listed"].append(row["Black Listed Tags"].strip())
                        if row["White Listed URLs"].strip() and row["White Listed URLs"] != "White Listed URLs":
                            site["urls_white_listed"].append(row["White Listed URLs"].strip())
                        if row["Black Listed URLs"].strip() and row["Black Listed URLs"] != "Black Listed URLs":
                            site["urls_black_listed"].append(row["Black Listed URLs"].strip())
                        if row["Trim URLs"].strip() and row["Trim URLs"] != "Trim URLs":
                            site["urls_trim"].append(row["Trim URLs"].strip())
                        if row["Proxies"].strip() and row["Proxies"] != "Proxies":
                            site["proxies"].append(row["Proxies"].strip())

            self.logger.info("CSV file successfully processed.")
        except Exception as e:
            self.logger.error(f"Failed to read CSV: {e}")
            raise

        return data

    def append_to_csv(self, file_path: str, data: Dict[str, Any]):
        """
        Appends data to a CSV file, creating it if it doesn't exist.

        :param file_path: Path to the CSV file.
        :param data: Data to append as a dictionary.
        """
        header = ["from", "page", "depth", "tag", "string"]
        sanitized_string = (
            data["string"]
            .replace("\n", " ")
            .replace("\r", " ")
            .replace("  ", " ")
            .strip()
        )

        line = [
            data.get("from", ""),
            data.get("page", ""),
            data.get("depth", ""),
            data.get("tag", ""),
            sanitized_string.replace('"', '""')
        ]

        try:
            file_exists = os.path.exists(file_path)

            with open(file_path, mode="a", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(header)
                writer.writerow(line)

            self.logger.info("Data successfully appended to CSV.")
        except Exception as e:
            self.logger.error(f"Failed to append to CSV: {e}")
            raise
