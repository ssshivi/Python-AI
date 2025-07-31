from fpdf import FPDF

# Create a sample PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200, 10, txt="Electricity Bill", ln=True, align='C')
pdf.ln(10)

pdf.cell(200, 10, txt="Account Number: 9876543210", ln=True)
pdf.cell(200, 10, txt="Billing Period: July 2025", ln=True)
pdf.cell(200, 10, txt="Due Date: 05-Aug-2025", ln=True)
pdf.cell(200, 10, txt="Total Amount: $156.75", ln=True)

pdf.output("sample.pdf")
print("✅ sample.pdf created successfully!")
