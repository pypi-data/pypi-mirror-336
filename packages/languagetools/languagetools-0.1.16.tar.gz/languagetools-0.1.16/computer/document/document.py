"""
- Use CSS page-break-after: always; for page breaks.
- Set explicit height (e.g., height: 297mm; for A4) for full-page content.
- Example HTML structure for multi-page:

    <div style="page-break-after: always;">
        <!-- Content for page 1 -->
    </div>
    <div style="page-break-after: always;">
        <!-- Content for page 2 -->
    </div>
"""

from weasyprint import HTML
from weasyprint import CSS
from .template import template
import subprocess
from pdf2docx import Converter

class Document:
    def __init__(self, computer):
        self.computer = computer
        self.installed_dependencies = False

    def template(self):
        if not self.installed_dependencies:
            # Download required packages
            install_command = "sudo apt-get install -y fonts-freefont-ttf pandoc texlive-base texlive-latex-recommended texlive-fonts-recommended texlive-publishers biber"
            subprocess.run(install_command.split())
            self.installed_dependencies = True
        
        template()

    def pdf_to_docx(self, pdf_file, docx_file):
        # convert pdf to docx
        cv = Converter(pdf_file)
        cv.convert(docx_file)      # all pages by default
        cv.close()
        return docx_file

    def html_to_pdf(self, html_file, pdf_file):
        try:
            # Convert HTML to PDF using WeasyPrint
            print("Converting HTML to PDF...")
            HTML(filename=html_file).write_pdf(
                pdf_file,
                presentational_hints=True,  # Enables background graphics and other CSS hints
                stylesheets=[CSS(string='@page { margin: 0; }')]  # Create CSS object from string
            )
            print(f"PDF saved as {pdf_file}")

        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise