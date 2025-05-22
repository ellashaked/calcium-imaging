import itertools
from typing import List

import plotly.express as px


def _get_color_iterator(palette_name='Plotly'):
    """
    Returns an infinite iterator over the given Plotly color palette.

    Args:
        palette_name (str): Name of the palette from plotly.express.colors.qualitative.
                            Defaults to 'Plotly'.

    Returns:
        Iterator[str]: Infinite color iterator.
    """
    palette = getattr(px.colors.qualitative, palette_name, None)
    if palette is None:
        raise ValueError(f"Unknown palette name '{palette_name}'. Check plotly.express.colors.qualitative for options.")
    return itertools.cycle(palette)


def get_n_colors_from_palette(n: int, palette_name: str = "Plotly") -> List[str]:
    color_iter = _get_color_iterator(palette_name)
    return [next(color_iter) for _ in range(n)]
