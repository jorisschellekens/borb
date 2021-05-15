import cProfile

import typing
from pathlib import Path

from ptext.pdf.pdf import PDF

from ptext.pdf.document import Document


def read_document():
    doc: typing.Optional[Document] = None
    with open(
        Path("/home/joris/Code/pdf-corpus/0063_page_0.pdf"), "rb"
    ) as pdf_file_handle:
        doc = PDF.loads(pdf_file_handle)


if __name__ == "__main__":
    cProfile.run("read_document()", "profiler_output.pstats")
    # joris@dell:~$ sudo /root/.local/bin/gprof2dot -f pstats /home/joris/PycharmProjects/ptext/tests/pdf/trailer/profiler_output.pstats | dot -Tpng -o /home/joris/output.png
