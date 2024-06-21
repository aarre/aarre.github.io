#!/usr/bin/python

import os
import pathlib
import subprocess
import sys

if __name__ == "__main__":

    pdf_filename = sys.argv[1]
    assert pdf_filename.endswith("pdf")
    png_filename = pathlib.Path(pdf_filename).with_suffix('.png')
    output = subprocess.check_output(["pdftoppm", "-png", "-f", "1", "-l", "1", "-singlefile", pdf_filename])
    with open(png_filename, 'wb') as f:
        f.write(output)
    f.close()

