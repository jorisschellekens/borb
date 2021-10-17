import json
import typing
import unittest
from pathlib import Path

from borb.toolkit.text.bigram_part_of_speech_tagger import BigramPartOfSpeechTagger

unittest.TestLoader.sortTestMethodsUsing = None


class TestPartOfSpeechTagger(unittest.TestCase):
    def test_part_of_speech_tagger_001(self):
        t: BigramPartOfSpeechTagger = BigramPartOfSpeechTagger()

        # load
        pos_path: Path = Path(__file__).parent / "bigram_part_of_speech_tagger_en.json"
        with open(pos_path, "r") as json_file_handle:
            t.from_json(json.loads(json_file_handle.read()))

        # tag
        toks: typing.List[str] = [
            "A",
            "big",
            "yellow",
            "taxi",
            "took",
            "my",
            "girl",
            "away",
            ".",
        ]
        tags: typing.List[str] = t.tag_list_str(toks)
        assert tags == ["at", "jj", "jj", "nn", "vbd", "pp$", "nn", "rb", "."]

    def test_part_of_speech_tagger_002(self):
        t: BigramPartOfSpeechTagger = BigramPartOfSpeechTagger()

        # load
        pos_path: Path = Path(__file__).parent / "bigram_part_of_speech_tagger_en.json"
        with open(pos_path, "r") as json_file_handle:
            t.from_json(json.loads(json_file_handle.read()))

        # tag
        toks: typing.List[str] = [
            "Pity",
            "the",
            "living",
            ",",
            "and",
            ",",
            "above",
            "all",
            "those",
            "who",
            "live",
            "without",
            "love",
            ".",
        ]
        tags: typing.List[str] = t.tag_list_str(toks)
        assert tags == [
            "vb",
            "at",
            "nn",
            ",",
            "cc",
            ",",
            "in",
            "abn",
            "dts",
            "wps",
            "vb",
            "in",
            "nn",
            ".",
        ]

    def test_part_of_speech_tagger_003(self):
        t: BigramPartOfSpeechTagger = BigramPartOfSpeechTagger()

        # load
        pos_path: Path = Path(__file__).parent / "bigram_part_of_speech_tagger_en.json"
        with open(pos_path, "r") as json_file_handle:
            t.from_json(json.loads(json_file_handle.read()))

        # tag
        tokens_and_tags: typing.List[typing.Tuple[str, str]] = t.tag_str(
            "Pity the living, and, above all those who live without love."
        )
        tags: typing.List[str] = [x[1] for x in tokens_and_tags]
        assert tags == [
            "vb",
            "at",
            "nn",
            ",",
            "cc",
            ",",
            "in",
            "abn",
            "dts",
            "wps",
            "vb",
            "in",
            "nn",
            ".",
        ]


if __name__ == "__main__":
    unittest.main()
