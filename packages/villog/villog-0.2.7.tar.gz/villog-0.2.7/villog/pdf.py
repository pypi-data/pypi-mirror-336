'''
    This module is responsible for generating PDF files from HTML and CSS files.
'''

from weasyprint import HTML, CSS

def generate(html_string: str,
             output_path: str,
             css_string: str | None = None) -> None:
    '''
        Generate a PDF file from a HTML and CSS file.

        Parameters:
            html_path (str): HTML string.
            output_path (str): Output path.
            css_path (str): CSS string.
    '''
    HTML(string = html_string).write_pdf(output_path,
                                         stylesheets = [CSS(string = css_string or "")]) # pylint: disable = line-too-long
