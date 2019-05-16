import io
from fpdf import FPDF

from .base import FileResultMessageBase


class PDFResultMessage(FileResultMessageBase):

    def get_filename(self):
        return "tax_results.pdf"

    def get_document(self, data):
        pdf = FPDF(
            unit="mm",
            format="A4",
            orientation="P",
        )
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(
            w=200,
            h=10,
            ln=1,
            align="C",
            txt="TAX CALCULATION RESULTS",
        )

        spacing = 2
        col_width = pdf.w / 2.2
        row_height = pdf.font_size

        for label, value in data.items():

            sign = " %" if label == "Ruling Real Percentage" else " EUR"
            value = f"{value:.2f}{sign}"

            pdf.cell(col_width, row_height * spacing, txt=label, border=1)
            pdf.cell(col_width, row_height * spacing, txt=value, border=1)
            pdf.ln(row_height * spacing)

        obj = io.BytesIO(pdf.output(dest="S").encode("latin-1"))
        return obj
