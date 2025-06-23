import os
import asyncio
import tkinter as tk
from tkinter import filedialog, messagebox
from Managers.CrawlManager import CrawlManager
from Utils.CSVReader import CSVReader
from Utils.Logger import Logger

class MainClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Crawler Configuration")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        # Instantiate the Logger
        self.logger = Logger(os.path.splitext(os.path.basename(__file__))[0])

        # Store configurations and data
        self.csv_reader = None
        self.crawl_manager = None
        self.config = {}
        self.data = None

        # Configure Styles
        header_font = ("Arial", 16, "bold")
        label_font = ("Arial", 12)
        entry_font = ("Arial", 12)

        # Header Section
        header_frame = tk.Frame(root)
        header_frame.pack(pady=10)
        tk.Label(header_frame, text="Web Crawler Configuration", font=header_font).pack()

        # Configuration Section
        config_frame = tk.LabelFrame(root, text="Crawl Configuration", font=label_font, padx=10, pady=10)
        config_frame.pack(fill="both", expand="yes", padx=20, pady=10)

        # Max Depth
        tk.Label(config_frame, text="Max Depth:", font=label_font).grid(row=0, column=0, sticky="w", pady=5)
        self.depth_max_entry = tk.Entry(config_frame, font=entry_font, width=25)
        self.depth_max_entry.grid(row=0, column=1, padx=10, pady=5)

        # Timeout
        tk.Label(config_frame, text="Timeout (seconds):", font=label_font).grid(row=1, column=0, sticky="w", pady=5)
        self.load_timeout_entry = tk.Entry(config_frame, font=entry_font, width=25)
        self.load_timeout_entry.grid(row=1, column=1, padx=10, pady=5)

        # Options Section
        options_frame = tk.LabelFrame(root, text="Crawl Options", font=label_font, padx=10, pady=10)
        options_frame.pack(fill="both", expand="yes", padx=20, pady=10)

        self.include_external_sites_var = tk.BooleanVar()
        self.enable_whitelist_url_var = tk.BooleanVar()
        self.enable_trim_url_var = tk.BooleanVar()
        self.enable_blacklist_url_var = tk.BooleanVar()

        tk.Checkbutton(options_frame, text="Include External Sites", variable=self.include_external_sites_var, font=label_font).pack(anchor="w", pady=5)
        tk.Checkbutton(options_frame, text="Enable Whitelist URL", variable=self.enable_whitelist_url_var, font=label_font).pack(anchor="w", pady=5)
        tk.Checkbutton(options_frame, text="Enable Trim URL", variable=self.enable_trim_url_var, font=label_font).pack(anchor="w", pady=5)
        tk.Checkbutton(options_frame, text="Enable Blacklist URL", variable=self.enable_blacklist_url_var, font=label_font).pack(anchor="w", pady=5)

        # Buttons Section
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Import CSV", command=self.import_csv, font=label_font, width=15, bg="lightblue").grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Start", command=self.start_process, font=label_font, width=15, bg="lightgreen").grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Quit", command=root.quit, font=label_font, width=15, bg="lightcoral").grid(row=0, column=2, padx=10)

    def create_config(self):
        """
        Create a configuration object based on user input.
        """
        depth_max = self.depth_max_entry.get()
        load_timeout = self.load_timeout_entry.get()

        if not depth_max.isdigit() or not load_timeout.isdigit():
            messagebox.showerror("Error", "Max Depth and Timeout must be valid numbers.")
            self.logger.error("Invalid input for Max Depth or Timeout.")
            return None

        return {
            "depth_max": int(depth_max),
            "load_timeout": int(load_timeout),
            "include_external_sites": self.include_external_sites_var.get(),
            "enable_whitelist_url": self.enable_whitelist_url_var.get(),
            "enable_trim_url": self.enable_trim_url_var.get(),
            "enable_blacklist_url": self.enable_blacklist_url_var.get()
        }

    def import_csv(self):
        # Create config from inputs
        self.config = self.create_config()
        if not self.config:
            return

        # Initialize CSVReader with the config object
        self.csv_reader = CSVReader(config=self.config)

        # Open file dialog to select a CSV file
        file_path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )

        if file_path:
            try:
                # Use the CSVReader to read the file
                self.data = self.csv_reader.read(file_path)

                # Log success
                self.logger.info(f"CSV imported successfully with {len(self.data)} rows.")

                # Display success message
                messagebox.showinfo("Success", f"CSV imported successfully with {len(self.data)} rows!")
                
                # Print the data to the console for debugging
                print("CSV Content (First 5 rows):")
                for row in self.data[:5]:
                    print(row)

            except Exception as e:
                self.logger.error(f"Failed to import CSV: {e}")
                messagebox.showerror("Error", f"Failed to import CSV:\n{str(e)}")

    def start_process(self):
        """
        Function for the Start button. Validates if a CSV has been imported before proceeding.
        """
        if not self.data:  # Check if CSV data is available
            self.logger.error("Start button clicked without importing a CSV file.")
            messagebox.showerror("Error", "No CSV file imported. Please import a CSV file first.")
            return

        # Log and proceed with the process
        self.logger.info("Start button clicked. Starting process.")
        self.crawl_manager = CrawlManager(self.config)

        # Run the asynchronous start_crawling method
        asyncio.run(self.crawl_manager.start_crawling(self.data))
        messagebox.showinfo("Start Process", "The process has started!")

def main():
    # Initialize the main window
    root = tk.Tk()
    app = MainClass(root)
    root.mainloop()


if __name__ == "__main__":
    main()
