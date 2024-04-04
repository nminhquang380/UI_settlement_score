import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import preprocessing
import statistics
import visualisation
class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Analysis Application")
        self.geometry("400x200")

        self.file_path = None
        self.data = None

        self.create_widgets()

    def create_widgets(self):
        self.upload_button = tk.Button(self, text="Upload CSV File", command=self.upload_file)
        self.upload_button.pack(pady=10)

        self.analyze_button = tk.Button(self, text="Analyse Data", command=self.analyze_data, state=tk.DISABLED)
        self.analyze_button.pack(pady=10)

    def upload_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])

        if self.file_path:
            self.data = pd.read_csv(self.file_path)
            self.analyze_button.config(state=tk.NORMAL)

    def analyze_data(self):
        if self.data is None:
            messagebox.showerror("Error", "No data loaded!")
            return

        # Perform preprocessing
        preprocessed_data = preprocessing.preprocess(self.data)

        # Calculate statistics
        stats_result = statistics.calculate_statistics(preprocessed_data)

        # Visualise data
        visualisation.visualize(preprocessed_data)

        # Generate report
        report = f"Preprocessed Data:\n{preprocessed_data}\n\nStatistics:\n{stats_result}"

        # Save report to a file
        report_file = "analysis_report.txt"
        with open(report_file, "w") as f:
            f.write(report)

        messagebox.showinfo("Analysis Complete", f"Analysis report saved to {report_file}")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
