from .tools import plot
from .utils import analysis, notify

notify.extend_finlab()
plot.extend_finlab()
analysis.extend_finlab()

__version__ = "0.1.3.dev1"


def main() -> None:
    pass
