import cProfile
import typing
from pathlib import Path

from borb.pdf.document.document import Document
from borb.pdf.pdf import PDF


def read_document():
    doc: typing.Optional[Document] = None
    with open(Path("/home/joris/Code/pdf-corpus/0364.pdf"), "rb") as pdf_file_handle:
        doc = PDF.loads(pdf_file_handle)


if __name__ == "__main__":
    cProfile.run("read_document()", "profiler_output.pstats")
    # joris@dell:~$ sudo /root/.local/bin/gprof2dot -f pstats /home/joris/PycharmProjects/borb/tests/pdf/trailer/profiler_output.pstats | dot -Tpng -o /home/joris/output.png
