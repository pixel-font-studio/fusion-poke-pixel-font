from collections.abc import Callable
from functools import cache
from pathlib import Path

import pytest
from pixel_font_knife.cmap.context import CmapContext

from tools.configs import options
from tools.configs.options import FontSize, GlyphScope


@pytest.fixture(scope='session')
def load_cmap_context() -> Callable[[Path, FontSize, GlyphScope], CmapContext]:
    @cache
    def load(glyphs_dir: Path, font_size: FontSize, glyph_scope: GlyphScope) -> CmapContext:
        return CmapContext.load(
            glyphs_dir.joinpath(str(font_size), 'cmap', glyph_scope),
            allowed_flavors=options.LANGUAGE_FLAVORS,
        )

    return load
