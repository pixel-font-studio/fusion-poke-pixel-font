from tools.config import paths
from tools.config.options import LanguageFlavor

SCOPE_MAPPING_FILE_PATHS = {
    'common': [
        paths.CONFIGS_MAPPINGS_DIR.joinpath('common', '2E80-2EFF CJK Radicals Supplement.yaml'),
        paths.CONFIGS_MAPPINGS_DIR.joinpath('common', '2F00-2FDF Kangxi Radicals.yaml'),
        paths.CONFIGS_MAPPINGS_DIR.joinpath('common', 'F900-FAFF CJK Compatibility Ideographs.yaml'),
    ],
    'other': [
        paths.CONFIGS_MAPPINGS_DIR.joinpath('other', '0080-00FF Latin-1 Supplement.yaml'),
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
