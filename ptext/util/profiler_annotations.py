import cProfile
import io
import pstats
from pstats import SortKey  # type: ignore [attr-defined]


def profile(func):
    def wrapper(*args, **kwargs):

        # setup profiler
        pr = cProfile.Profile()
        pr.enable()

        # execute function
        out_value = func(*args, **kwargs)

        # disable profiler
        pr.disable()
        s = io.StringIO()
        sortby = SortKey.CUMULATIVE
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())

        # return
        return out_value

    return wrapper
