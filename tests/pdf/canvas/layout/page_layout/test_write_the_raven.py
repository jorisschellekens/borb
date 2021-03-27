import logging
import unittest
from pathlib import Path

from ptext.io.read.types import Decimal
from ptext.pdf.canvas.color.color import HexColor
from ptext.pdf.canvas.layout.image import Image
from ptext.pdf.canvas.layout.page_layout import MultiColumnLayout, SingleColumnLayout
from ptext.pdf.canvas.layout.paragraph import (
    Alignment,
    Paragraph,
)
from ptext.pdf.document import Document
from ptext.pdf.page.page import Page
from ptext.pdf.pdf import PDF
from tests.util import get_log_dir, get_output_dir

logging.basicConfig(
    filename=Path(get_log_dir(), "test-write-the-raven.log"), level=logging.DEBUG
)


class TestWriteTheRaven(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path(get_output_dir(), "test-write-the-raven")

    def test_write_document(self):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        # create document
        pdf = Document()

        # add page
        page = Page()
        pdf.append_page(page)

        # first layer, displaying a raven
        layout = SingleColumnLayout(page)
        for _ in range(0, 12):
            layout.add(Paragraph(" ", respect_spaces_in_text=True))
        layout.add(
            Image(
                "https://cdn3.vectorstock.com/i/1000x1000/03/47/black-raven-on-white-background-vector-4780347.jpg"
            )
        )

        # second layer, displaying the poem
        layout = MultiColumnLayout(page, number_of_columns=2)
        layout.add(
            Paragraph(
                "The Raven",
                font_size=Decimal(20),
                font="Helvetica-Oblique",
                font_color=HexColor("708090"),
            )
        )
        layout.add(
            Paragraph(
                """Once upon a midnight dreary, while I pondered, weak and weary,
                                Over many a quaint and curious volume of forgotten lore-
                                While I nodded, nearly napping, suddenly there came a tapping,
                                As of some one gently rapping, rapping at my chamber door.
                                'Tis some visitor,' I muttered, 'tapping at my chamber door-
                                Only this and nothing more.'""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """Ah, distinctly I remember it was in the bleak December;
                                And each separate dying ember wrought its ghost upon the floor.
                                Eagerly I wished the morrow;-vainly I had sought to borrow
                                From my books surcease of sorrow-sorrow for the lost Lenore-
                                For the rare and radiant maiden whom the angels name Lenore-
                                Nameless here for evermore.""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """And the silken, sad, uncertain rustling of each purple curtain
                                Thrilled me-filled me with fantastic terrors never felt before;
                                So that now, to still the beating of my heart, I stood repeating
                                'Tis some visitor entreating entrance at my chamber door-
                                Some late visitor entreating entrance at my chamber door;-
                                This it is and nothing more.'""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """Presently my soul grew stronger; hesitating then no longer,
                                'Sir,' said I, 'or Madam, truly your forgiveness I implore;
                                But the fact is I was napping, and so gently you came rapping,
                                And so faintly you came tapping, tapping at my chamber door,
                                That I scarce was sure I heard you'-here I opened wide the door;-
                                Darkness there and nothing more.""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.switch_to_next_column()
        layout.add(
            Paragraph(
                """Deep into that darkness peering, long I stood there wondering, fearing,
                                Doubting, dreaming dreams no mortal ever dared to dream before;
                                But the silence was unbroken, and the stillness gave no token,
                                And the only word there spoken was the whispered word, 'Lenore?'
                                This I whispered, and an echo murmured back the word, 'Lenore!'-
                                Merely this and nothing more.""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """Back into the chamber turning, all my soul within me burning,
                                Soon again I heard a tapping somewhat louder than before.
                                'Surely,' said I, 'surely that is something at my window lattice;
                                Let me see, then, what thereat is, and this mystery explore-
                                Let my heart be still a moment and this mystery explore;-
                                'Tis the wind and nothing more!'""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """Open here I flung the shutter, when, with many a flirt and flutter,
                                In there stepped a stately Raven of the saintly days of yore;
                                Not the least obeisance made he; not a minute stopped or stayed he;
                                But, with mien of lord or lady, perched above my chamber door-
                                Perched upon a bust of Pallas just above my chamber door-
                                Perched, and sat, and nothing more.""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """Then this ebony bird beguiling my sad fancy into smiling,
                                By the grave and stern decorum of the countenance it wore,
                                'Though thy crest be shorn and shaven, thou,' I said, 'art sure no craven,
                                Ghastly grim and ancient Raven wandering from the Nightly shore-
                                Tell me what thy lordly name is on the Night's Plutonian shore!'
                                Quoth the Raven 'Nevermore.'""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """Much I marvelled this ungainly fowl to hear discourse so plainly,
                                Though its answer little meaning-little relevancy bore;
                                For we cannot help agreeing that no living human being
                                Ever yet was blessed with seeing bird above his chamber door-
                                Bird or beast upon the sculptured bust above his chamber door,
                                With such name as 'Nevermore.'""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        layout.add(
            Paragraph(
                """But the Raven, sitting lonely on the placid bust, spoke only
                    That one word, as if his soul in that one word he did outpour.
                    Nothing farther then he uttered-not a feather then he fluttered-
                    Till I scarcely more than muttered 'Other friends have flown before-
                    On the morrow he will leave me, as my Hopes have flown before.'
                    Then the bird said 'Nevermore.'""",
                horizontal_alignment=Alignment.CENTERED,
                font_size=Decimal(7),
                respect_newlines_in_text=True,
            )
        )
        # determine output location
        out_file = self.output_dir / "output.pdf"

        # attempt to store PDF
        with open(out_file, "wb") as in_file_handle:
            PDF.dumps(in_file_handle, pdf)

        with open(out_file, "rb") as in_file_handle:
            PDF.loads(in_file_handle)
