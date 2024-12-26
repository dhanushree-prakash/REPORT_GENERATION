import pandas as pd
from fpdf import FPDF
import os

# File path (use one of the options to avoid path issues)
data_file = r"C:\Users\dhanu\REPORT_GENERATION\data.csv"  # Example with raw string

# Check if the file exists and is not empty
if not os.path.exists(data_file):
    print(f"Error: File '{data_file}' not found. Please ensure it exists in the directory.")
    exit()

if os.stat(data_file).st_size == 0:
    print(f"Error: File '{data_file}' is empty. Please add valid data.")
    exit()

# Load the data with tab delimiter
try:
    data = pd.read_csv(data_file, delimiter='\t')
    if data.empty:
        print("Error: The CSV file has no valid data.")
        exit()
except pd.errors.EmptyDataError:
    print("Error: The file is improperly formatted or missing headers.")
    exit()
except Exception as e:
    print(f"Unexpected error occurred while reading the file: {e}")
    exit()

print("Data loaded successfully:")
print(data.head())

# Filter numeric columns (in this case, 'salary')
numeric_data = data.select_dtypes(include=['number'])

# Generate insights
insights = ""

# Calculate and append the average salary
if 'salary' in numeric_data.columns:
    insights += f"Average salary: {numeric_data['salary'].mean()}\n"
else:
    insights += "No numeric data found for salary.\n"

# Class to create the PDF report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Automated Report Generation', align='C', ln=True)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, ln=True)
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln(5)

    def table(self, data):
        self.set_font('Arial', 'B', 12)
        # Column headers
        col_widths = [40, 40, 40]  # Adjust the column widths
        headers = ['Name', 'Department', 'Salary']
        for col, header in zip(col_widths, headers):
            self.cell(col, 10, header, border=1, align='C')
        self.ln()

        # Table content
        self.set_font('Arial', '', 12)
        for row in data.itertuples(index=False):
            self.cell(col_widths[0], 10, str(row[0]), border=1, align='C')
            self.cell(col_widths[1], 10, str(row[1]), border=1, align='C')
            self.cell(col_widths[2], 10, str(row[2]), border=1, align='C')
            self.ln()

# Create the PDF object
pdf = PDF()
pdf.add_page()

# Title for the Report
pdf.chapter_title("Data Analysis Report")

# Add the insights generated
pdf.chapter_body(insights)

# Analyze the data - For example, let's summarize the first few rows of data
summary = "Summary of the Data:\n"
summary += data.head().to_string(index=False)

# Add the data summary to the PDF as a table
pdf.chapter_title("Data Summary")
pdf.table(data.head())

# Saving the PDF
output_pdf = "Generated_Report.pdf"
pdf.output(output_pdf)

print(f"Report generated successfully and saved as '{output_pdf}'.")
