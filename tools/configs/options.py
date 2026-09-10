from typing import Literal, get_args

type FontSize = Literal[
    10,
    12,
]
FONT_SIZES = list[FontSize](get_args(FontSize.__value__))

type LanguageFlavor = Literal[
    'latin',
    'zh_hans',
    'zh_hant',
    'ja',
    'ko',
]
LANGUAGE_FLAVORS = list[LanguageFlavor](get_args(LanguageFlavor.__value__))

type LanguageFileFlavor = Literal[
    'latin',
    'zh_cn',
    'zh_hk',
    'zh_tw',
    'zh_tr',
    'ja',
    'ko',
]
LANGUAGE_FILE_FLAVORS = list[LanguageFileFlavor](get_args(LanguageFileFlavor.__value__))
