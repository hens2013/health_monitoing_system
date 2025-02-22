from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(200, 10, "Health Report", ln=True, align="C")

    def add_section(self, title, text):
        text = text.replace("🚨", "Warning:")
        self.set_font("Arial", "B", 14)
        self.cell(200, 10, title, ln=True, align="L")
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)
        self.ln(5)


