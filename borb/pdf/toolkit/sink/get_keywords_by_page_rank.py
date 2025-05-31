#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Extracts keywords from a PDF document on a per-page basis using the TextRank algorithm.

This class extends `GetText` to process text data extracted from a PDF file and identify key terms based on
their importance using the PageRank algorithm. A co-occurrence graph is built where words are connected
based on their proximity within a given window. The highest-ranked words are selected as keywords,
with common stopwords being excluded to improve relevance.
"""
import typing

from borb.pdf.toolkit.sink.get_text import GetText


class GetKeywordsByPageRank(GetText):
    """
    Extracts keywords from a PDF document on a per-page basis using the TextRank algorithm.

    This class extends `GetText` to process text data extracted from a PDF file and identify key terms based on
    their importance using the PageRank algorithm. A co-occurrence graph is built where words are connected
    based on their proximity within a given window. The highest-ranked words are selected as keywords,
    with common stopwords being excluded to improve relevance.
    """

    # fmt: off
    ENGLISH_STOPWORDS: typing.Set[str] = {'con', 'yes', 'bj', 'generally', 'means', 'nobody', 'c', 'ill', 'known', 'sure', 'anybody', 'give', 'state', 'int', 'hadnt', 'whered', 'hes', 'facts', 'itself', 'mrs', 'backward', 'ca', 'al', 'ni', 'fifth', 'probably', 'far', 'cs', 'whichever', 'darent', 'ch', 'working', 'nz', 'of', 'front', 'tends', 'evenly', 'fk', 'through', 'case', 'appear', 'doesn', 'mx', 'area', 'happens', 'weve', 'pf', 'become', 'old', 'got', 'mug', 'run', 'sec', 'ups', 'gd', 'shell', 'entirely', 'ever', 'longer', 'vi', 'effect', 'instead', 'specify', 'herse', 'men', 'sensible', 'show', 'been', 've', 'dare', 'namely', 'thereve', 'two', 'indicates', 'om', 'faces', 'un', 'shes', 'your', 'w', 'she', 'which', 'yourself', 'es', 'can', 'present', 'rd', 'so', 'clear', 'always', 'fo', 'but', 'available', 'inc', 'knows', 'found', 'may', 'bn', 'cc', 'own', 'bill', 'second', 'get', 'number', 'consequently', 'know', 'again', 'beings', 'kp', 'downs', 'puts', 'arise', 'seriously', 'one', 'a', 'therefore', 'if', 'anyone', 'say', 'higher', 'pages', 'was', 'things', 'pm', 'thanx', 'goods', 'consider', 'normally', 'part', 'provides', 'whereby', 'couldnt', 'grouped', 'latest', 'pt', 'behind', 'didn', 'gm', 'non', 'still', 'usually', 'almost', 'has', 'buy', 'rw', 'thatve', 'thereupon', 'unlikely', 'ng', 'neverless', 'began', 'viz', 'least', 'further', 'mustve', 'problems', 'provided', 'felt', 'somethan', 'll', 'doing', 'g', 'less', 'owing', 'presented', 'important', 'kg', 'much', 'amidst', 'anything', 'bt', 'secondly', 'sm', 'here', 'alone', 'de', 'homepage', 'well', 'other', 'somehow', 'himse', 'its', 'keys', 'line', 'ly', 'tt', 'd', 'truly', 'mk', 'regarding', 'whim', 'shall', 'tz', 'gl', 'added', 'order', 'tries', 'hers', 'thoroughly', 'whyd', 'eight', 'ordering', 'tj', 'meantime', 'bs', 'jm', 'getting', 'throug', 'interested', 'si', 'wants', 'awfully', 'where', 'just', 'wouldve', 'etal', 'kw', 'given', 'into', 'believe', 'looks', 'merely', 'plus', 'np', 'related', 'someone', 'ended', 'want', 'haven', 'theirs', 'itll', 'towards', 'u', 'bb', 'na', 'sn', 'won', 'twice', 'fully', 'he', 'whoever', 'til', 'him', 'gets', 'shouldnt', 'cant', 'm', 'wasnt', 'beginning', 'ci', 'sr', 'upwards', 'beforehand', 'ba', 'herein', 'relatively', 'ml', 'whatll', 'outside', 'using', 'downing', 'begins', 'elsewhere', 'like', 'something', 'fact', 'none', 'sb', 'apart', 'ten', 'ending', 'mm', 'near', 'finds', 'mostly', 'billion', 'following', 'see', 'seem', 'specified', 'wholl', 'ie', 'otherwise', 'became', 'ga', 'widely', 'downed', 'knew', 'ls', 'willing', 'above', 'asked', 'rather', 'side', 'thin', 'ordered', 'thoughts', 'does', 'very', 'research', 'thereto', 'quickly', 'wouldnt', 'etc', 'than', 'whilst', 'sometime', 'ug', 'face', 'groups', 'il', 'strongly', 'showing', 'cy', 'not', 'tried', 'uses', 'fewer', 'whereupon', 'good', 'afterwards', 'us', 'microsoft', 'seven', 'work', 'ltd', 'meanwhile', 'member', 'please', 'then', 'wherever', 'who', 'howll', 'whither', 'msie', 'neverf', 'therere', 'htm', 'cu', 'hows', 'whereas', 'ai', 'edu', 'presents', 'saying', 'seeming', 'kind', 'lk', 'tc', 'aside', 'thank', 'do', 'general', 'is', 'successfully', 'today', 'org', 'ye', 'tip', 'often', 'wasn', 'in', 'containing', 'points', 'jo', 'uucp', 'indicate', 'and', 'cannot', 'gotten', 'ao', 'im', 'done', 'ive', 'move', 'nine', 'despite', 'ones', 'since', 'sixty', 'ru', 'bd', 'havent', 'top', 'name', 'forth', 'bv', 'big', 'mv', 'pe', 'seeing', 'sv', 'her', 'therein', 'long', 'various', 'ahead', 'backs', 'arent', 'presenting', 'sy', 'system', 'bi', 'myself', 'hello', 'mainly', 'netscape', 'youd', 'seems', 'ends', 'join', 'becoming', 'minus', 'those', 'though', 'should', 'come', 'causes', 'everything', 'to', 'l', 'clearly', 'h', 'z', 'eleven', 'vs', 'either', 'sincere', 'affecting', 'works', 'mc', 'mean', 'currently', 'another', 'pa', 'everybody', 'hr', 'information', 'whatd', 'making', 'could', 'across', 'bm', 'asking', 'hasnt', 'hed', 'his', 'kn', 'lc', 'amongst', 'put', 'suggest', 'used', 'yourselves', 'whole', 'parted', 'smallest', 'away', 'high', 'newest', 'be', 'think', 'thinks', 'ways', 'yt', 'young', 'brief', 'immediate', 'length', 'miss', 'md', 'mz', 'our', 'latterly', 'ed', 'forward', 'sufficiently', 'youve', 'amid', 'unlike', 'zero', 'dk', 'lr', 'changes', 'bottom', 'anymore', 'different', 'v', 'way', 'greater', 'dj', 'same', 'seventy', 'shouldn', 'shows', 'hereupon', 'va', 'heres', 'shown', 'few', 'cr', 'anyhow', 'eg', 'page', 'sa', 'man', 'gn', 'mp', 'right', 'liked', 'newer', 'hu', 'directly', 'significant', 'together', 'nowhere', 'up', 'beside', 'biol', 'az', 'vols', 'usefulness', 'ok', 'on', 'slightly', 'recent', 'turned', 'lt', 'wont', 'e', 'older', 'apparently', 'hk', 'worked', 'they', 'opening', 'maybe', 'ord', 'aint', 'kept', 'corresponding', 'evermore', 'st', 'ee', 'opens', 'kz', 'auth', 'gu', 'wells', 'mg', 'pointed', 'needs', 'during', 'http', 'lv', 'primarily', 'took', 'some', 'down', 'shouldve', 'low', 'says', 'thought', 'go', 'qv', 'ae', 'an', 'else', 'somewhat', 'turns', 'omitted', 'wherein', 'sub', 'fifty', 'hn', 'lately', 'alongside', 'whomever', 'don', 'too', 'gs', 'ua', 'wonder', 'after', 'abst', 'hid', 'thereof', 'thus', 'backwards', 'obviously', 'yours', 'place', 'gt', 'what', 'without', 'someday', 'j', 'definitely', 'oughtnt', 'cg', 'que', 'needing', 'test', 'below', 'describe', 'fi', 'nothing', 'fj', 'follows', 'possible', 'gov', 'considering', 'particularly', 'dm', 'cn', 'ro', 'hither', 'asks', 'vg', 'great', 'best', 'interest', 'nevertheless', 'overall', 'tr', 'year', 'pn', 'twas', 'mightnt', 'dz', 'fill', 'turn', 'no', 'keep', 'py', 'ourselves', 'six', 'them', 'did', 'br', 'via', 'gf', 'empty', 'hi', 'dont', 'o', 'affected', 'ke', 'versus', 'greetings', 'keeps', 'ii', 'werent', 'gmt', 'followed', 'soon', 'reasonably', 'such', 'allows', 'tm', 'y', 'hereafter', 'until', 'shed', 'uy', 'bw', 'whod', 'mo', 'unfortunately', 'aren', 'once', 'ignored', 'lower', 'mt', 'example', 'himself', 'cm', 'herself', 'this', 'off', 'theyve', 'seconds', 'tn', 'you', 'proud', 'cl', 'www', 'dear', 'trying', 'kh', 'thru', 'ne', 'pw', 'arpa', 'due', 'ag', 'going', 'likely', 'wanting', 'rooms', 'all', 'contain', 'hm', 'showns', 'theyll', 'cases', 'because', 'gb', 'looking', 'fairly', 'inasmuch', 'null', 'sh', 'numbers', 'fr', 'group', 'begin', 'besides', 'bh', 'end', 'nu', 'take', 'nc', 'cry', 'room', 'usefully', 'uz', 'amount', 'the', 'cmon', 'weren', 'differently', 'oh', 'tf', 'interesting', 'full', 'said', 'when', 'point', 'stop', 'gave', 'invention', 'km', 'n', 'itse', 'novel', 'it', 'inner', 'pk', 'bg', 'au', 'anywhere', 'also', 'made', 'have', 'tg', 'obtained', 'placed', 'beginnings', 'nos', 'many', 'shant', 'hasn', 'mh', 'za', 'html', 'wed', 'ableabout', 'qa', 'free', 'gives', 'x', 'cf', 'three', 'mightve', 'twenty', 'large', 'we', 'resulted', 'thing', 'aw', 'fx', 'similarly', 'specifically', 'welcome', 'while', 'open', 'iq', 'thereby', 'next', 'ws', 'er', 'never', 'backed', 'throughout', 'amoungst', 'make', 'gy', 'cd', 'mr', 'q', 'anyways', 'id', 'appropriate', 'sorry', 'possibly', 'com', 'onto', 'cx', 'gp', 'ours', 'use', 'five', 'parts', 'site', 'wanted', 'necessary', 'twelve', 'couldve', 'nearly', 'whenever', 'furthered', 'came', 'theyd', 'affects', 'underneath', 'r', 'opposite', 'cz', 'under', 'gone', 'serious', 'must', 'obtain', 'self', 'somewhere', 'thence', 'ring', 'zm', 'thereafter', 'noone', 'others', 'as', 'certain', 'fm', 'perhaps', 'before', 'fify', 'sl', 'pl', 'comes', 'theres', 'from', 'ad', 'except', 'whom', 'accordance', 'adj', 'differ', 'ah', 'inward', 'for', 'howd', 'neednt', 't', 'every', 'indicated', 'lets', 'p', 'according', 'kr', 'largely', 'try', 'ff', 'will', 'sees', 'went', 'wf', 'ms', 'ki', 'isn', 'gi', 'pointing', 'taking', 'et', 'moreover', 'now', 'thick', 'useful', 'certainly', 'likewise', 'gh', 'beyond', 'nay', 'unless', 'ir', 'actually', 'respectively', 'taken', 'whether', 'width', 'poorly', 'substantially', 'lb', 'backing', 'lest', 'net', 'downwards', 'tis', 'against', 'only', 'youngest', 'whats', 'years', 'both', 'ask', 'nr', 'thoughh', 'turning', 'la', 'that', 'didnt', 'latter', 'were', 'whens', 'longest', 'okay', 'bz', 'gq', 'index', 'younger', 'course', 'accordingly', 'act', 'members', 'k', 'nd', 'pr', 'ht', 'adopted', 'help', 'sd', 'past', 'detail', 'places', 'anyway', 's', 'pp', 'specifying', 'thatll', 'enough', 'furthering', 'insofar', 'regards', 'thousand', 'tp', 'round', 'website', 'being', 'tell', 'thats', 'between', 're', 'fix', 'immediately', 'io', 'promptly', 'se', 'having', 'interests', 'seen', 'wheres', 'f', 'mn', 'mq', 'resulting', 'sometimes', 'approximately', 'vol', 'are', 'last', 'potentially', 'ma', 'fifteen', 'yu', 'might', 'hereby', 'whend', 'youll', 'vc', 'several', 'whereafter', 'associated', 'need', 'thanks', 'although', 'results', 'states', 'abroad', 'hell', 'inside', 'ky', 'fire', 'their', 'theyre', 'recently', 'gg', 'able', 'selves', 'upon', 'howbeit', 'needed', 'ph', 'whys', 'early', 'computer', 'exactly', 'sj', 'nf', 'web', 'around', 'necessarily', 'wish', 'really', 'click', 'eh', 'eighty', 'forever', 'je', 'whatever', 'or', 'by', 'with', 'importance', 'better', 'why', 'whence', 'first', 'unto', 'td', 'ninety', 'within', 'pg', 'farther', 'similar', 'nonetheless', 'couldn', 'parting', 'at', 'ck', 'thered', 'allow', 'cv', 'b', 'opened', 'greatest', 'significantly', 'saw', 'aq', 'let', 'concerning', 'had', 'makes', 'appreciate', 'noted', 'among', 'small', 'wouldn', 'somebody', 'most', 'themselves', 'whyll', 'grouping', 'sg', 'whose', 'bo', 'mine', 'oldest', 'everyone', 'readily', 'tk', 'everywhere', 'itd', 'mustnt', 'youre', 'call', 'af', 'doubtful', 'presumably', 'my', 'there', 'gr', 'notwithstanding', 'ec', 'sent', 'smaller', 'wherell', 'words', 'caption', 'however', 'value', 'sc', 'zr', 'hardly', 'would', 'co', 'furthermore', 'per', 'webpage', 'sup', 'hundred', 'mw', 'me', 'hopefully', 'jp', 'neither', 'particular', 'thou', 'problem', 'described', 'even', 'predominantly', 'sk', 'toward', 'out', 'maynt', 'ex', 'gw', 'million', 'myse', 'isnt', 'trillion', 'back', 'uk', 'pmid', 'four', 'seemed', 'tv', 'yet', 'bf', 'find', 'giving', 'briefly', 'becomes', 'contains', 'already', 'sides', 'along', 'furthers', 'doesnt', 'new', 'li', 'lu', 'hence', 'announce', 'little', 'indeed', 'ago', 'orders', 'reserved', 'su', 'sz', 'whenll', 'each', 'nor', 'vn', 'vu', 'copy', 'therell', 'areas', 'especially', 'mil', 'more', 'thirty', 'about', 'formerly', 'till', 'ran', 'th', 'undoing', 'thorough', 'am', 'showed', 'previously', 'ts', 'former', 'ge', 'section', 'highest', 'goes', 'half', 'world', 'third', 'any', 'date', 'look', 'forty', 'mill', 'whatve', 'ar', 'ref', 'over', 'text', 'whos', 'i', 'mu', 'refs', 'cause', 'how', 'quite', 'regardless', 'nl', 'these', 'tw', 'later', 'um', 'ought', 'home'}
    # fmt: on

    #
    # CONSTRUCTOR
    #

    def __init__(self, number_of_keywords: int = 10):
        """
        Initialize the GetKeywordsByPageRank class.

        This constructor sets the number of keywords to extract per page using
        the PageRank method. It ensures that the provided number is non-negative.

        :param number_of_keywords: The number of keywords to extract per page (default: 10).
                                   Must be a non-negative integer.
        """
        super().__init__()
        assert number_of_keywords >= 0
        self.__max_number_of_iterations: int = 128
        self.__number_of_keywords: int = number_of_keywords
        self.__window_size: int = 5

    #
    # PRIVATE
    #

    @staticmethod
    def __normalize_text(s: str) -> str:
        """Normalize text by converting to lowercase, removing punctuation, and stripping special characters."""
        import re

        s = s.lower()  # Convert to lowercase
        s = re.sub(r"\d+", "", s)  # Remove digits
        s = re.sub(r"[^\w\s]", "", s)  # Remove punctuation
        s = re.sub(r"\s+", " ", s).strip()  # Normalize whitespace
        return s

    @staticmethod
    def __text_rank(
        max_number_of_iterations: int,
        number_of_keywords: int,
        tokens: typing.List[str],
        window_size: int,
    ) -> typing.Dict[str, float]:

        # build co-occurence matrix
        co_occurence: typing.Dict[str, typing.Dict[str, float]] = {}
        for i in range(0, len(tokens)):
            for j in range(i - window_size, i + window_size):
                if j < 0:
                    continue
                if j >= len(tokens):
                    continue
                if i == j:
                    continue
                w0: str = tokens[i].upper()
                w1: str = tokens[j].upper()
                if len(w0) == 0:
                    continue
                if len(w1) == 0:
                    continue
                if w0 not in co_occurence:
                    co_occurence[w0] = {}
                co_occurence[w0][w1] = co_occurence[w0].get(w1, 0) + 1

        # eigenvalue algorithm
        import random

        prev_eigenvalue: typing.Dict[str, float] = {
            k: random.randint(1, 100) / 100 for k in co_occurence.keys()
        }
        for i in range(0, max_number_of_iterations):
            next_eigenvalue: typing.Dict[str, float] = {
                k: 0 for k in prev_eigenvalue.keys()
            }
            for k0, v0 in prev_eigenvalue.items():
                sum_v1s: float = sum(co_occurence.get(k0, {}).values())
                for k1, v1 in co_occurence.get(k0, {}).items():
                    next_eigenvalue[k1] += v0 * (v1 / sum_v1s)

            # calculate delta
            delta: float = 0
            for k, v in next_eigenvalue.items():
                delta += abs(v - prev_eigenvalue.get(k, 0))
            if delta < 10**-5:
                break

            # assign
            prev_eigenvalue = next_eigenvalue

        # return
        return dict(
            sorted(prev_eigenvalue.items(), key=lambda item: item[1], reverse=True)[
                :number_of_keywords
            ]
        )

    #
    # PUBLIC
    #

    def get_output(self) -> typing.Any:
        """
        Retrieve the aggregated results from the pipeline.

        This method should be overridden by subclasses to provide the specific output
        collected by the `Sink`. By default, it returns `None`, indicating that no
        aggregation or processing has been implemented.

        :return: The aggregated output from the pipeline, or `None` if not implemented.
        """
        text_per_page: typing.Dict[int, str] = super().get_output()

        # Normalize the text (convert to lowercase, remove punctuation, special characters, etc.).
        text_per_page = {
            k: GetKeywordsByPageRank.__normalize_text(v)
            for k, v in text_per_page.items()
        }

        # Tokenizes text by splitting on whitespace.
        # Assumes the text is already normalized (lowercased, punctuation removed).
        words_per_page: typing.Dict[int, typing.List[str]] = {
            k: v.split() for k, v in text_per_page.items()
        }

        # Remove common stopwords (e.g., "the," "is," "and," "of") to filter out unimportant words.
        words_per_page = {
            k: [x for x in v if x not in GetKeywordsByPageRank.ENGLISH_STOPWORDS]
            for k, v in words_per_page.items()
        }

        # Return
        return {
            k: GetKeywordsByPageRank.__text_rank(
                max_number_of_iterations=self.__max_number_of_iterations,
                number_of_keywords=self.__number_of_keywords,
                tokens=v,
                window_size=self.__window_size,
            )
            for k, v in words_per_page.items()
        }
