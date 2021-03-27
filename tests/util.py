from pathlib import Path


def get_log_dir() -> Path:
    p: Path = Path(__file__).parent
    while "logs" not in [x.name for x in p.iterdir()]:
        p = p.parent
    return Path(p, "logs")


def get_output_dir() -> Path:
    p: Path = Path(__file__).parent
    while "output" not in [x.name for x in p.iterdir()]:
        p = p.parent
    return Path(p, "output")
