#!env/bin/python
"""
Make PNG files from PDF files in the PDF directory.

I tried using make to do this, but it has a number of problems.
Among them:

    (1) I cannot get make to coqllect a list of PDF files in the
        _portfolio directory and make the PNG files
        for all of them. I can just do one at a time.

    (2) Make does not deal well with spaces in filenames, but I
        have to put spaces in these filenames or Hydejack puts
        the underscores on my web page, which is ugly.
"""
import logging
import pathlib
import subprocess

logger = logging.getLogger(__name__)


def make_one_png(pdf_path_string: str, y_offset: int, height: int):
    """
    Make a single PNG file from a single PDF file.

    :param pdf_path_string: Path to the PDF file.
    :param y_offset: How many pixels to offset the PNG image from the
           top of the PDF file.
    :param height: How many pixels high the PNG should be.
    """
    assert pdf_path_string.endswith("pdf")
    pdf_path = pathlib.Path(pdf_path_string)
    png_path = pdf_path.with_suffix('.png')
    png_contents = subprocess.check_output(["pdftoppm", "-png",
                                            "-f", "1",
                                            "-l", "1",
                                            "-y", str(y_offset),
                                            "-H", str(height),
                                            "-singlefile",
                                            str(pdf_path)])
    with open(png_path, 'wb') as png_file:
        png_file.write(png_contents)
    png_file.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting up")
    make_one_png("_portfolio/digital entrepreneurship and "
                 "innovation in central america.pdf", 400, 800)
    make_one_png("_portfolio/scaling up romania.pdf", 0, 800)
    make_one_png("_portfolio/starting up romania.pdf", 0, 800)
