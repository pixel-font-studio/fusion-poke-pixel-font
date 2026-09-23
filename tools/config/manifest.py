from tools.config import path_define
from tools.config.options import LanguageFlavor

SCOPE_MAPPING_FILE_PATHS = {
    'common': [
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('2E80-2EFF CJK Radicals Supplement.yaml'),
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('2F00-2FDF Kangxi Radicals.yaml'),
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('F900-FAFF CJK Compatibility Ideographs.yaml'),
    ],
    'other': [
        path_define.CONFIGS_MAPPINGS_DIR.joinpath('0080-00FF Latin-1 Supplement.yaml'),
    ],
}

LANGUAGE_FLAVOR_TO_FONT_NAME: dict[LanguageFlavor, str] = {
    'latin': 'latin',
    'zh_hans': 'zh-Hans',
    'zh_hant': 'zh-Hant',
    'zh_hk': 'zh-HK',
    'zh_tw': 'zh-TW',
    'ja': 'ja',
    'ko': 'ko',
}

LICENSE_CONFIGS = {
    'ark-pixel': [
        'OFL.txt',
    ],
    'boutique-bitmap-9x9': [
        'OFL.txt',
    ],
    'cubic-11': [
        'OFL.txt',
    ],
    'galmuri': [
        'LICENSE.txt',
    ],
}
