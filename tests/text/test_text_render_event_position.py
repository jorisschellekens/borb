import json
import logging
import re
import unittest
from pathlib import Path

from ptext.pdf.canvas.event.event_listener import EventListener, Event
from ptext.pdf.canvas.event.text_render_event import TextRenderEvent
from ptext.pdf.pdf import PDF
from tests.test import Test

logging.basicConfig(
    filename="../text/test-text-render-event-position.log", level=logging.DEBUG
)


class TextRenderInfoMeasurandListener(EventListener):
    def __init__(self):
        self.measurands = []

    def event_occurred(self, event: Event):
        if isinstance(event, TextRenderEvent):
            assert isinstance(event, TextRenderEvent)
            self.measurands.append(
                {
                    "text": event.get_text(),
                    "x0": float(event.get_baseline().x0),
                    "x1": float(event.get_baseline().x1),
                    "y": float(event.get_baseline().y0),
                    "length": float(event.get_baseline().length()),
                }
            )


class TestTextRenderEventPosition(Test):
    """
    This test attempts to extract the text of each PDF in the corpus
    """

    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.output_dir = Path("../text/test-text-render-event-position")
        self.max_distance = 2

    def test_exact_document(self):
        self.test_document(Path("/home/joris/Code/pdf-corpus/0322_page_0.pdf"))

    def test_corpus(self):
        super(TestTextRenderEventPosition, self).test_corpus()

    def test_document(self, file):

        # create output directory if it does not exist yet
        if not self.output_dir.exists():
            self.output_dir.mkdir()

        with open(file, "rb") as pdf_file_handle:
            l = TextRenderInfoMeasurandListener()

            # read document
            doc = PDF.loads(pdf_file_handle, [l])

            # export json
            output_file = self.output_dir / (file.stem + "_text_rendering.json")
            with open(output_file, "w") as txt_file_handle:
                txt_file_handle.write(json.dumps(l.measurands, indent=4))

        # load ground truth
        ground_truth_results = []
        with open(
            Path(self.input_dir / (file.stem + "_text_rendering.json")), "r"
        ) as json_file_handle:
            ground_truth_results = json.loads(json_file_handle.read())

        # compare
        pos_in_test_array = 0
        pos_in_gt_array = 0
        while pos_in_test_array < len(l.measurands) and pos_in_gt_array < len(
            ground_truth_results
        ):
            while pos_in_test_array < len(l.measurands) and re.match(
                "[^a-zA-Z ]+", l.measurands[pos_in_test_array]["text"]
            ):
                pos_in_test_array += 1
            while pos_in_gt_array < len(ground_truth_results) and re.match(
                "[^a-zA-Z ]+", ground_truth_results[pos_in_gt_array]["text"]
            ):
                pos_in_gt_array += 1
            # check text
            if (
                l.measurands[pos_in_test_array]["text"]
                != ground_truth_results[pos_in_gt_array]["text"]
            ):
                print("text inequality %d %d !!" % (pos_in_gt_array, pos_in_test_array))
                return False

            x_delta = abs(
                int(l.measurands[pos_in_test_array]["x0"])
                - int(ground_truth_results[pos_in_gt_array]["x0"])
            )
            if x_delta > self.max_distance:
                print("x0 inequality %d %d !!" % (pos_in_gt_array, pos_in_test_array))
                print(
                    "\tground truth: %f" % ground_truth_results[pos_in_gt_array]["x0"]
                )
                print("\ttest        : %f" % l.measurands[pos_in_test_array]["x0"])
                return False

            x_delta = abs(
                int(l.measurands[pos_in_test_array]["y"])
                - int(ground_truth_results[pos_in_gt_array]["y"])
            )
            if x_delta > self.max_distance:
                print("x1 inequality %d %d !!" % (pos_in_gt_array, pos_in_test_array))
                print(
                    "\tground truth: %f" % ground_truth_results[pos_in_gt_array]["x1"]
                )
                print("\ttest        : %f" % l.measurands[pos_in_test_array]["x1"])
                return False

            y_delta = abs(
                int(l.measurands[pos_in_test_array]["y"])
                - int(ground_truth_results[pos_in_gt_array]["y"])
            )
            if y_delta > self.max_distance:
                print("y inequality %d %d !!" % (pos_in_gt_array, pos_in_test_array))
                print("\tground truth: %f" % ground_truth_results[pos_in_gt_array]["y"])
                print("\ttest        : %f" % l.measurands[pos_in_test_array]["y"])
                return False

            print(
                "%s %d %d %d"
                % (
                    l.measurands[pos_in_test_array]["text"],
                    l.measurands[pos_in_test_array]["x0"],
                    l.measurands[pos_in_test_array]["x1"],
                    l.measurands[pos_in_test_array]["y"],
                )
            )
            pos_in_test_array += 1
            pos_in_gt_array += 1

        return True


if __name__ == "__main__":
    unittest.main()
