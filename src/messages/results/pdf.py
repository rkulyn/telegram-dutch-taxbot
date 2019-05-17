import io
import numbers
from fpdf import FPDF

from .base import FileResultMessageBase


class PDFResultMessage(FileResultMessageBase):
    """
    Build and sent result as PDF file.

    """
    def get_filename(self):
        return "tax_results.pdf"

    @staticmethod
    def build_title(document):
        """
        Build title for given file.

        Args:
            document (file-like object): Current file.

        Returns: None.

        """
        document.cell(
            200, 10,
            ln=1, align="C",
            txt="TAX CALCULATION RESULTS"
        )

    @staticmethod
    def build_sign(document):
        """
        Build signature text line for given file.

        Args:
            document (file-like object): Current file.

        Returns: None.

        """
        document.cell(
            200, 10,
            ln=1, align="C",
            txt="Created by Dutch Tax Bot (c)"
        )

    def get_document(self, data):
        """
        Build PDF file.

        Args:
            data (dict): Data to build document.

        Returns:
            (file-like object): File.

        """
        pdf = FPDF(
            unit="mm",
            format="A4",
            orientation="P",
            # Portrait
        )
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        self.build_title(pdf)
        self.build_sign(pdf)

        spacing = 2
        # All width with small
        # left and right margins
        col_width = pdf.w / 2.2
        # Define row size = font size
        row_height = pdf.font_size

        for label, value in data.items():

            # Round numbers to 2 digit fraction.
            value = f"{value:.2f}" if isinstance(value, numbers.Number) else value

            pdf.cell(col_width, row_height * spacing, txt=label, border=1)
            pdf.cell(col_width, row_height * spacing, txt=value, border=1)
            pdf.ln(row_height * spacing)

        # Encode output for Python 3
        obj = io.BytesIO(pdf.output(dest="S").encode("latin-1"))
        return obj
