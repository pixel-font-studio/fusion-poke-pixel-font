from typing import Literal, get_args

type FontSize = Literal[
    10,
    12,
]
font_sizes = list[FontSize](get_args(FontSize.__value__))

type LanguageFlavor = Literal[
    'latin',
    'zh_hans',
    'zh_hant',
    'ja',
    'ko',
]
language_flavors = list[LanguageFlavor](get_args(LanguageFlavor.__value__))

type LanguageFileFlavor = Literal[
    'latin',
    'zh_cn',
    'zh_hk',
    'zh_tw',
    'zh_tr',
    'ja',
    'ko',
]
language_file_flavors = list[LanguageFileFlavor](get_args(LanguageFileFlavor.__value__))
