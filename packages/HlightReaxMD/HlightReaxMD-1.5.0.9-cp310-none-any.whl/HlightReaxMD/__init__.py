__version__ = '1.5.0.9'
__author__ = 'W.-Y.Li, RFUE'
__package__ = 'HlightReaxMD'
__description__ = (
    'A package designed for analyzing ReaxFF molecular dynamics data and displacement cascade processes.'
    )
__citation__ = 'W.-Y.Li, 2025, JCTC.'
__citation_url__ = 'https://vone/svn/hlightreaxmd_test/'
__codeurl__ = 'https://gitee.com/zai-xia/HlightReaxMD'
from mpi4py import MPI
import sys
from .log import logg
_package_initialized = False


def display_banner():
    print(
        ' __  __   ___                __      __    ____                                     ____      '
        )
    print(
        "/\\ \\/\\ \\ /\\_ \\    __        /\\ \\    /\\ \\__/\\  _`\\                           /'\\_/`\\/\\  _`\\    "
        )
    print(
        '\\ \\ \\_\\ \\\\//\\ \\  /\\_\\     __\\ \\ \\___\\ \\ ,_\\ \\ \\_\\ \\     __     __     __  _/\\      \\ \\ \\/\\ \\  '
        )
    print(
        " \\ \\  _  \\ \\ \\ \\ \\/\\ \\  /'_ `\\ \\  _ `\\ \\ \\/\\ \\ ,  /   /'__`\\ /'__`\\  /\\ \\/'\\ \\ \\__\\ \\ \\ \\ \\ \\ "
        )
    print(
        '  \\ \\ \\ \\ \\ \\_\\ \\_\\ \\ \\/\\ \\_\\ \\ \\ \\ \\ \\ \\ \\_\\ \\ \\\\ \\ /\\  __//\\ \\_\\.\\_\\/>  </\\ \\ \\_/\\ \\ \\ \\_\\ \\'
        )
    print(
        '   \\ \\_\\ \\_\\/\\____\\\\ \\_\\ \\____ \\ \\_\\ \\_\\ \\__\\\\ \\_\\ \\_\\ \\____\\ \\__/.\\_\\/\\_/\\_\\\\ \\_\\\\ \\_\\ \\____/'
        )
    print(
        '    \\/_/\\/_/\\/____/ \\/_/\\/___,\\ \\/_/\\/_/\\/__/ \\/_/\\/ /\\/____/\\/__/\\/_/\\//\\/_/ \\/_/ \\/_/\\/___/ '
        )
    print(
        '                          /\\____/                                                         '
        )
    print(
        f'                          \\_/__/    {__package__} v {__version__} made by {__author__}            '
        )
    print()
    print(__description__)
    print('=' * 100)


def _show_banner():
    global _package_initialized
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    if rank == 0 and not _package_initialized:
        display_banner()
        _package_initialized = True


_show_banner()
from .hlightreaxmd import HlightReaxMD
from .findspecies import FindSpecies
from .drawpng import DrawPNG
from .collect import Collect
from .analysis import Analysis
from .reaction import RecognizeReaction
from .cascade import CascadeAnalysis
