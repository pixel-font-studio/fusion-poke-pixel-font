from pixel_font_knife import glyph_mapping_util

from tools.configs import path_define, options
from tools.configs.dump import DumpConfig
from tools.configs.fallback import FallbackConfig
from tools.configs.font import FontConfig
from tools.configs.upgrade import UpgradeConfig

VERSION = '2026.09.01'

UPGRADE_CONFIGS = UpgradeConfig.load()

DUMP_CONFIGS = DumpConfig.load()

FALLBACK_CONFIGS = FallbackConfig.load()

FONT_CONFIGS = {font_size: FontConfig.load(font_size) for font_size in options.FONT_SIZES}

MAPPINGS = [
    glyph_mapping_util.load_mapping(path_define.MAPPINGS_DIR.joinpath('0080-00FF Latin-1 Supplement.yaml')),
    glyph_mapping_util.load_mapping(path_define.MAPPINGS_DIR.joinpath('2E80-2EFF CJK Radicals Supplement.yaml')),
    glyph_mapping_util.load_mapping(path_define.MAPPINGS_DIR.joinpath('2F00-2FDF Kangxi Radicals.yaml')),
]

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
