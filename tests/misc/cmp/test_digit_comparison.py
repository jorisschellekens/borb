import random
import time
import unittest


class TestDigitComparison(unittest.TestCase):
    @staticmethod
    def is_digit_001(c: str) -> bool:
        return c in "0123456789+-."

    @staticmethod
    def is_digit_002(c: str) -> bool:
        return ("0" <= c <= "9") or c == "+" or c == "-" or c == "."

    is_digit_003 = set("0123456789+-.").__contains__

    @staticmethod
    def random_digit_string(N: int) -> str:
        return "".join(
            [
                random.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ.+-")
                for _ in range(0, N)
            ]
        )

    def test_digit_comparison_by_array(self):
        for i in [10 ** x for x in range(0, 6)]:

            is_digit_001_time_avg = 0
            is_digit_002_time_avg = 0
            is_digit_003_time_avg = 0
            for j in range(0, 10):
                s = TestDigitComparison.random_digit_string(i)

                # time is_digit_003
                is_digit_003_time = time.time()
                is_digit_003_count = 0
                for c in s:
                    is_digit_003_count += (
                        1 if TestDigitComparison.is_digit_003(c) else 0
                    )
                is_digit_003_time = time.time() - is_digit_003_time

                # time is_digit_001
                is_digit_001_time = time.time()
                is_digit_001_count = 0
                for c in s:
                    is_digit_001_count += (
                        1 if TestDigitComparison.is_digit_001(c) else 0
                    )
                is_digit_001_time = time.time() - is_digit_001_time

                # time is_digit_002
                is_digit_002_time = time.time()
                is_digit_002_count = 0
                for c in s:
                    is_digit_002_count += (
                        1 if TestDigitComparison.is_digit_002(c) else 0
                    )
                is_digit_002_time = time.time() - is_digit_002_time

                assert is_digit_001_count == is_digit_002_count
                assert is_digit_001_count == is_digit_003_count

                # update avg
                is_digit_001_time_avg += is_digit_001_time
                is_digit_002_time_avg += is_digit_002_time
                is_digit_003_time_avg += is_digit_003_time

            is_digit_001_time_avg /= 10
            is_digit_002_time_avg /= 10
            is_digit_003_time_avg /= 10

            print(
                "n: %d, is_digit_001: %f, is_digit_002: %f, is_digit_003: %f"
                % (
                    i,
                    is_digit_001_time_avg,
                    is_digit_002_time_avg,
                    is_digit_003_time_avg,
                )
            )
