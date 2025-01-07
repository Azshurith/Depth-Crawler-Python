import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Utils.CSVReader import CSVReader
from Utils.Logger import Logger


class MainClass:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Importer with Configuration")
        self.root.geometry("400x400")

        # Instantiate the Logger
        self.logger = Logger(os.path.splitext(os.path.basename(__file__))[0])

        # Instantiate the CsvReader (later initialized with config)
        self.csv_reader = None

        # Store config object
        self.config = {}

        self.data = None  # Store the imported data

        # Create UI elements
        self.label = tk.Label(root, text="Welcome to CSV Importer", font=("Arial", 16))
        self.label.pack(pady=10)

        # Max Depth Input
        self.depth_max_label = tk.Label(root, text="Max Depth:", font=("Arial", 12))
        self.depth_max_label.pack(pady=5)
        self.depth_max_entry = tk.Entry(root, font=("Arial", 12))
        self.depth_max_entry.pack(pady=5)

        # Timeout Input
        self.load_timeout_label = tk.Label(root, text="Loading Timeout (seconds):", font=("Arial", 12))
        self.load_timeout_label.pack(pady=5)
        self.load_timeout_entry = tk.Entry(root, font=("Arial", 12))
        self.load_timeout_entry.pack(pady=5)

        # Checkboxes
        self.include_external_sites_var = tk.BooleanVar()
        self.enable_whitelist_url_var = tk.BooleanVar()
        self.enable_trim_url_var = tk.BooleanVar()
        self.enable_blacklist_url_var = tk.BooleanVar()

        self.include_external_sites_checkbox = tk.Checkbutton(
            root, text="Include External Sites", variable=self.include_external_sites_var, font=("Arial", 12)
        )
        self.include_external_sites_checkbox.pack(pady=5)

        self.enable_whitelist_url_checkbox = tk.Checkbutton(
            root, text="Enable Whitelist URL", variable=self.enable_whitelist_url_var, font=("Arial", 12)
        )
        self.enable_whitelist_url_checkbox.pack(pady=5)

        self.enable_trim_url_checkbox = tk.Checkbutton(
            root, text="Enable Trim URL", variable=self.enable_trim_url_var, font=("Arial", 12)
        )
        self.enable_trim_url_checkbox.pack(pady=5)

        self.enable_blacklist_url_checkbox = tk.Checkbutton(
            root, text="Enable Blacklist URL", variable=self.enable_blacklist_url_var, font=("Arial", 12)
        )
        self.enable_blacklist_url_checkbox.pack(pady=5)

        self.import_button = tk.Button(root, text="Import CSV", command=self.import_csv, font=("Arial", 12))
        self.import_button.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_process, font=("Arial", 12))
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Arial", 12))
        self.quit_button.pack(pady=10)

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
            return  # Exit if config creation fails

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
        messagebox.showinfo("Start Process", "The process has started!")
        print("Start button clicked. Process started successfully.")

def main():
    # Initialize the main window
    root = tk.Tk()
    app = MainClass(root)
    root.mainloop()


if __name__ == "__main__":
    main()
