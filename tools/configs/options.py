from typing import Literal, get_args

type FontSize = Literal[
    10,
    12,
]
FONT_SIZES = list[FontSize](get_args(FontSize.__value__))

type GlyphScope = Literal[
    'common',
    'monospaced',
    'proportional',
    'narrow',
]
GLYPH_SCOPES = list[GlyphScope](get_args(GlyphScope.__value__))

type LanguageFlavor = Literal[
    'latin',
    'zh_hans',
    'zh_hant',
    'zh_hk',
    'zh_tw',
    'ja',
    'ko',
]
LANGUAGE_FLAVORS = list[LanguageFlavor](get_args(LanguageFlavor.__value__))
