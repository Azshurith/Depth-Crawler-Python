import os
import tkinter as tk
from tkinter import filedialog, messagebox
from Utils.CSVReader import CSVReader
from Utils.Logger import Logger

class MainClass:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Importer")
        self.root.geometry("400x250")

        # Instantiate the CsvReader
        self.csv_reader = CSVReader()

        # Instantiate the Logger
        self.logger = Logger(os.path.splitext(os.path.basename(__file__))[0])

        self.data = None  # Store the imported data

        # Create UI elements
        self.label = tk.Label(root, text="Welcome to CSV Importer", font=("Arial", 16))
        self.label.pack(pady=10)

        self.import_button = tk.Button(root, text="Import CSV", command=self.import_csv, font=("Arial", 12))
        self.import_button.pack(pady=10)

        self.start_button = tk.Button(root, text="Start", command=self.start_process, font=("Arial", 12))
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Arial", 12))
        self.quit_button.pack(pady=10)

    def import_csv(self):
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
        self.logger.info("Start button clicked. Process started successfully.")
        messagebox.showinfo("Start Process", "The process has started!")
        print("Start button clicked. Process started successfully.")

def main():
    # Initialize the main window
    root = tk.Tk()
    app = MainClass(root)
    root.mainloop()

if __name__ == "__main__":
    main()
